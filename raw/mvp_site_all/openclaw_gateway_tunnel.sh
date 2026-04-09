#!/bin/bash
#
# Start a public Tailscale Funnel to expose local OpenClaw gateway.
# Creates a stable HTTPS URL like https://<machine-name>.<tailnet>.ts.net.
# Automatically installs Tailscale if needed, starts the daemon, logs in, and configures Funnel.
#
# Usage:
#   scripts/openclaw_tailscale_tunnel.sh
#   scripts/openclaw_tailscale_tunnel.sh --port 18789

set -euo pipefail

# launchd jobs start with a minimal PATH; include Homebrew locations explicitly.
export PATH="/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/usr/local/sbin:/usr/bin:/bin:/usr/sbin:/sbin:${PATH:-}"

# Use mktemp for log directory when not explicitly set
if [[ -n "${OPENCLAW_TUNNEL_LOG_DIR:-}" ]]; then
  LOG_DIR="${OPENCLAW_TUNNEL_LOG_DIR}"
else
  LOG_DIR="$(mktemp -d -t openclaw-tunnel.XXXXXX)"
fi
trap 'printf "❌ Unexpected error on line %s\n" "${LINENO}" >&2' ERR

PORT=18789
WAIT=0
CHECK_GATEWAY=1
VERBOSE=0
DOCTOR_ONLY=0
export GITHUB_TOKEN="${GITHUB_TOKEN:-}"
SCRIPT_URL_FILE=~/.openclaw/openclaw_gateway_tunnel_url.txt
# Set to the socket path when tailscaled is started via the user-space fallback;
# empty means use the system default socket.
TAILSCALE_SOCKET_PATH=""
TAILSCALE_BIN=""
OS="$(uname -s)"

log() {
  if (( VERBOSE )); then
    echo "$@" >&2
  fi
}

info() {
  echo "$@" >&2
}

error() {
  echo "❌ $*" >&2
}

write_url_file() {
  local url="$1"
  local output_file="${2:-}"
  if [[ -n "${output_file}" ]]; then
    mkdir -p "$(dirname "${output_file}")"
    printf "%s\n" "${url}" >"${output_file}"
  fi
}

# Wrapper that passes --socket when tailscaled was started with a custom socket path.
tailscale_cmd() {
  if [[ -z "${TAILSCALE_BIN}" ]]; then
    error "tailscale CLI path is not resolved."
    exit 5
  fi
  if [[ -n "${TAILSCALE_SOCKET_PATH}" ]]; then
    "${TAILSCALE_BIN}" --socket="${TAILSCALE_SOCKET_PATH}" "$@"
  else
    "${TAILSCALE_BIN}" "$@"
  fi
}

resolve_tailscale_bin() {
  # Prefer explicit binary locations used by Homebrew installs on macOS.
  for candidate in \
    "${TAILSCALE_BIN:-}" \
    "/opt/homebrew/bin/tailscale" \
    "/usr/local/bin/tailscale" \
    "$(command -v tailscale 2>/dev/null || true)"; do
    if [[ -n "${candidate}" && -x "${candidate}" ]]; then
      TAILSCALE_BIN="${candidate}"
      return 0
    fi
  done
  TAILSCALE_BIN=""
  return 1
}

doctor_fail() {
  local reason="$1"
  local next_command="$2"
  # Collapse newlines to keep each value on a single line (preserves KEY=VALUE protocol)
  local reason_single="${reason//$'\n'/ }"
  local next_command_single="${next_command//$'\n'/ }"
  cat <<EOF
DOCTOR_STATUS=not_ready
DOCTOR_REASON=${reason_single}
DOCTOR_NEXT_COMMAND=${next_command_single}
EOF
  exit 2
}

require_port() {
  if ! [[ "${PORT}" =~ ^[0-9]+$ ]]; then
    error "--port must be a number."
    exit 2
  fi
  if (( PORT < 1 || PORT > 65535 )); then
    error "--port must be between 1 and 65535."
    exit 2
  fi
}

ensure_health() {
  local endpoint="http://127.0.0.1:${PORT}/health"
  local health_err
  if ! health_err="$(curl -fsS "$endpoint" 2>&1)"; then
    error "Local gateway check failed: unable to reach ${endpoint}"
    [[ -n "${health_err}" ]] && echo "   curl output: ${health_err}"
    echo "   Start OpenClaw first so localhost:${PORT} is serving the gateway."
    exit 3
  fi
}

run_doctor() {
  if ! resolve_tailscale_bin; then
    if [[ "$OS" == "Darwin" ]]; then
      doctor_fail \
        "tailscale CLI is not installed." \
        "brew install tailscale"
    elif [[ "$OS" == "Linux" ]]; then
      doctor_fail \
        "tailscale CLI is not installed." \
        "curl -fsSL https://tailscale.com/install.sh | sh"
    else
      doctor_fail \
        "tailscale CLI is not installed on unsupported OS: ${OS}." \
        "Install from https://tailscale.com/download"
    fi
  fi

  local ts_daemon_out
  if ! ts_daemon_out="$(tailscale_cmd status 2>&1)"; then
    if [[ "$OS" == "Darwin" ]]; then
      doctor_fail \
        "tailscaled is not running or not reachable: ${ts_daemon_out}" \
        "sudo tailscaled --socket=/var/run/tailscale/tailscaled.sock"
    else
      doctor_fail \
        "tailscaled is not running or not reachable: ${ts_daemon_out}" \
        "sudo systemctl start tailscaled"
    fi
  fi

  local ts_status_out
  if ! ts_status_out="$(tailscale_cmd status --json 2>&1)"; then
    doctor_fail \
      "tailscale status --json failed: ${ts_status_out}" \
      "tailscale status --json"
  fi
  if ! grep -q '"BackendState": *"Running"' <<<"${ts_status_out}"; then
    doctor_fail \
      "tailscale is installed but not authenticated/connected." \
      "tailscale up"
  fi

  if (( CHECK_GATEWAY )); then
    local gateway_health_out
    if ! gateway_health_out="$(curl -fsS "http://127.0.0.1:${PORT}/health" 2>&1)"; then
      doctor_fail \
        "local OpenClaw gateway is not reachable on localhost:${PORT}: ${gateway_health_out}" \
        "openclaw gateway status"
    fi
  fi

  local ts_funnel_out
  if ! ts_funnel_out="$(tailscale_cmd funnel status 2>&1)"; then
    doctor_fail \
      "tailscale funnel status failed: ${ts_funnel_out}" \
      "tailscale funnel reset"
  fi
  if grep -q "(tailnet only)" <<<"${ts_funnel_out}"; then
    doctor_fail \
      "tailscale is connected but only tailnet-only Serve routing is configured." \
      "tailscale funnel --bg ${PORT}"
  fi

  cat <<EOF
DOCTOR_STATUS=ready
DOCTOR_REASON=all_checks_passed
DOCTOR_NEXT_COMMAND=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/$(basename "${BASH_SOURCE[0]}") --port ${PORT}
EOF
}

install_tailscale() {
  info "Installing Tailscale..."

  case "$OS" in
    Darwin)
      # Install via Homebrew when available. launchd jobs should not try to
      # self-install tools because they run in restricted environments.
      if command -v brew >/dev/null 2>&1; then
        info "Installing Tailscale via Homebrew..."
        brew install tailscale
      else
        error "Homebrew not found in PATH. Install Tailscale manually from https://tailscale.com/download"
        exit 5
      fi
      return 0
      ;;
    Linux)
      info "Installing Tailscale via install script..."
      local _install_script
      _install_script="$(mktemp -t tailscale-install.XXXXXX.sh)"
      trap 'rm -f "${_install_script}"' RETURN
      curl -fsSL https://tailscale.com/install.sh -o "${_install_script}"
      chmod +x "${_install_script}"
      "${_install_script}"
      rm -f "${_install_script}"
      return 0
      ;;
    *)
      error "Unsupported OS: $OS"
      error "Visit https://tailscale.com/download to install manually"
      exit 5
      ;;
  esac
}

start_tailscaled() {
  case "$OS" in
    Darwin)
      # On macOS, either start the daemon OR use the GUI app - not both (avoids socket conflicts)
      if ! pgrep -x tailscaled >/dev/null 2>&1; then
        info "Starting Tailscale..."
        # Prefer the GUI app if installed (handles auth automatically)
        if [ -f "/Applications/Tailscale.app/Contents/MacOS/Tailscale" ]; then
          open -a Tailscale
          sleep 3
        else
          # Fallback: start daemon directly
          if sudo -n true 2>/dev/null; then
            sudo tailscaled --socket=/var/run/tailscale/tailscaled.sock &
          else
            error "Cannot start tailscaled without a password prompt. Open Tailscale.app first or pre-authenticate sudo."
            exit 5
          fi
          sleep 2
        fi
      fi
      ;;
    Linux)
      # On Linux, try to start via systemd or directly
      if ! pgrep -x tailscaled >/dev/null 2>&1; then
        info "Starting Tailscale daemon..."
        # Try user systemd first
        if command -v systemctl >/dev/null 2>&1; then
          if ! systemctl --user start tailscaled; then
            info "Note: systemctl --user start tailscaled failed; will try direct daemon start."
          fi
        fi
        # Fallback: start directly with user-accessible socket path.
        # Record the socket path so subsequent tailscale_cmd calls target the same daemon.
        if ! pgrep -x tailscaled >/dev/null 2>&1; then
          if [[ -n "${XDG_RUNTIME_DIR:-}" ]]; then
            TAILSCALE_SOCKET_PATH="${XDG_RUNTIME_DIR}/tailscale.sock"
          else
            local tailscale_socket_dir
            tailscale_socket_dir="$(mktemp -d -t openclaw-tailscale-sock.XXXXXX)"
            chmod 700 "${tailscale_socket_dir}"
            TAILSCALE_SOCKET_PATH="${tailscale_socket_dir}/tailscale.sock"
            trap "rm -rf '${tailscale_socket_dir}'" EXIT
          fi
          nohup tailscaled --socket="${TAILSCALE_SOCKET_PATH}" >"${LOG_DIR}/tailscaled.out" 2>"${LOG_DIR}/tailscaled.err" &
          sleep 2
        fi
      fi
      ;;
  esac

  # Wait for daemon to be ready (use tailscale_cmd so we target the correct socket)
  local attempts=10
  local n=0
  while (( n < attempts )); do
    if tailscale_cmd status >/dev/null 2>&1; then
      return 0
    fi
    sleep 1
    n=$((n + 1))
  done

  return 1
}

login_tailscale() {
  info "Starting Tailscale login..."
  info ""
  info "IMPORTANT: Complete authentication in the browser/window that opens."
  info "After logging in, this script will continue automatically."
  info ""

  # Run tailscale up - it will open browser for authentication
  tailscale_cmd up

  # Wait for connection
  local attempts=60
  local n=0
  while (( n < attempts )); do
    local ts_login_out
    # Failure expected while login is in progress; poll until BackendState=Running
    ts_login_out="$(tailscale_cmd status --json 2>&1)" || true
    if grep -q '"BackendState": *"Running"' <<<"${ts_login_out}"; then
      info "Tailscale connected!"
      return 0
    fi
    sleep 2
    n=$((n + 1))
  done

  error "Tailscale login timed out. Please run 'tailscale up' manually and try again."
  exit 4
}

ensure_tailscale() {
  # Check if tailscale is installed
  if ! resolve_tailscale_bin; then
    install_tailscale
    resolve_tailscale_bin || {
      error "tailscale CLI still not available after install attempt."
      exit 5
    }
  fi

  # Single status --json call: if it fails, the daemon isn't running
  local ts_ensure_out
  if ! ts_ensure_out="$(tailscale_cmd status --json 2>&1)"; then
    info "Tailscale daemon not running. Starting..."
    if ! start_tailscaled; then
      error "Failed to start Tailscale daemon. Please start it manually and try again."
      error "On macOS: sudo tailscaled --socket=/var/run/tailscale/tailscaled.sock"
      error "On Linux: systemctl --user start tailscaled"
      exit 5
    fi
    # Re-check after starting daemon
    if ! ts_ensure_out="$(tailscale_cmd status --json 2>&1)"; then
      error "tailscale status --json failed after daemon start: ${ts_ensure_out}"
      return 1
    fi
  fi

  # Check if logged in
  if ! grep -q '"BackendState": *"Running"' <<<"${ts_ensure_out}"; then
    login_tailscale
  fi

  info "Tailscale is ready!"
}

get_tailscale_url() {
  # Derive the Tailscale HTTPS URL from the machine's DNSName in tailscale status.
  # This is reliable regardless of what tailscale funnel prints to stdout.
  local status_json dns_name
  # Use 2>/dev/null to discard stderr (version warnings), only capture JSON to stdout
  if ! status_json="$(tailscale_cmd status --json 2>/dev/null)"; then
    error "tailscale status --json failed"
    return 1
  fi
  dns_name="$(printf '%s' "${status_json}" | python3 -c 'import json,sys; d=json.load(sys.stdin); print((d.get("Self") or {}).get("DNSName","").rstrip("."))' 2>/dev/null)" || return 1
  if [[ -n "${dns_name}" ]]; then
    echo "https://${dns_name}"
    return 0
  fi
  return 1
}

usage() {
  cat <<'EOF'
Usage:
  scripts/openclaw_tailscale_tunnel.sh [options]

Options:
  --port <n>             Local OpenClaw gateway port (default: 18789)
  --wait                 Keep this script attached (Ctrl-C to stop tunnel)
  --skip-gateway-check   Skip localhost health check before tunneling
  --doctor               Run prerequisite checks and exit
  --verbose              Enable verbose output
  -h, --help             Show this help text

This script:
  1. Installs Tailscale if not already installed
  2. Starts the Tailscale daemon if not running
  3. Logs you in (opens browser) if not already authenticated
  4. Sets up Tailscale Funnel to expose your local OpenClaw gateway publicly
  5. Outputs a stable public Tailscale HTTPS URL

The URL persists across reboots - Tailscale re-applies the Funnel rule automatically.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --port)
      if [[ $# -lt 2 ]]; then
        error "--port requires a value."
        exit 2
      fi
      PORT="$2"
      shift 2
      ;;
    --wait)
      WAIT=1
      shift
      ;;
    --skip-gateway-check)
      CHECK_GATEWAY=0
      shift
      ;;
    --doctor)
      DOCTOR_ONLY=1
      shift
      ;;
    --verbose)
      VERBOSE=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      error "Unknown argument: $1"
      usage
      exit 2
      ;;
  esac
done

require_port
mkdir -p "${LOG_DIR}"

if (( DOCTOR_ONLY )); then
  run_doctor
  exit 0
fi

if (( CHECK_GATEWAY )); then
  ensure_health
fi

# Ensure Tailscale is installed and running
ensure_tailscale

# Set up Tailscale Funnel
LOG_DIR_TAILSCALE="${LOG_DIR}/tailscale"
mkdir -p "${LOG_DIR_TAILSCALE}"
serve_log="${LOG_DIR_TAILSCALE}/funnel.log"

info "Setting up Tailscale Funnel on port ${PORT}..."
info "Log will be written to: ${serve_log}"

# Check if already funneling the desired port
if ! serve_status_out="$(tailscale_cmd funnel status 2>&1)"; then
  error "tailscale funnel status failed: ${serve_status_out}"
  exit 6
fi
if grep -q "127.0.0.1:${PORT}" <<<"${serve_status_out}"; then
  if grep -q "(tailnet only)" <<<"${serve_status_out}"; then
    info "Existing tailnet-only route detected for port ${PORT}; replacing it with Funnel..."
    ts_reset_err=""
    if ! ts_reset_err="$(tailscale_cmd funnel reset 2>&1)"; then
      echo "${ts_reset_err}" >>"${serve_log}"
      error "tailscale funnel reset failed: ${ts_reset_err}"
      error "Check log for details: ${serve_log}"
      exit 6
    fi
    echo "${ts_reset_err}" >>"${serve_log}"
    
    ts_serve_err=""
    if ! ts_serve_err="$(tailscale_cmd funnel --bg "http://127.0.0.1:${PORT}" 2>&1)"; then
      echo "${ts_serve_err}" >>"${serve_log}"
      error "tailscale funnel failed: ${ts_serve_err}"
      error "Check log for details: ${serve_log}"
      exit 6
    fi
    echo "${ts_serve_err}" >>"${serve_log}"
  else
    info "Tailscale Funnel already configured for port ${PORT}"
  fi
else
  # If a different port is already configured, check if it's safe to reset.
  # Count all Tailscale routes (|-- lines in status output).
  # Reset only if 0 routes (clean slate) or 1 route (our previous instance).
  # Skip reset if multiple routes exist to preserve unrelated mappings.
  if grep -q "127.0.0.1:" <<<"${serve_status_out}"; then
    route_count="$(grep -c '^|--' <<<"${serve_status_out}" || echo 0)"
    if (( route_count > 1 )); then
      error "Multiple Tailscale routes detected."
      error "Cannot safely reset without removing unrelated Funnel/Serve mappings."
      error "Remove conflicting routes manually: tailscale funnel status"
      error "Then re-run this script."
      exit 6
    fi
    # 0 or 1 route - safe to reset
    info "Existing Tailscale route detected for a different port."
    info "⚠️  WARNING: Resetting Tailscale Funnel config. This clears the existing route on this node."
    info "Resetting funnel config to configure port ${PORT}..."
    ts_reset_err=""
    if ! ts_reset_err="$(tailscale_cmd funnel reset 2>&1)"; then
      echo "${ts_reset_err}" >>"${serve_log}"
      error "tailscale funnel reset failed: ${ts_reset_err}"
      error "Check log for details: ${serve_log}"
      exit 6
    fi
    echo "${ts_reset_err}" >>"${serve_log}"
  fi

  # Apply new Funnel rule. tailscale funnel configures the public proxy
  # (it does not print the URL to stdout).
  # Capture stderr first to preserve error message for diagnostics.
  ts_serve_err=""
  if ! ts_serve_err="$(tailscale_cmd funnel --bg "http://127.0.0.1:${PORT}" 2>&1)"; then
    # Write output to log file for debugging, but show error to user immediately
    echo "${ts_serve_err}" >>"${serve_log}"
    error "tailscale funnel failed: ${ts_serve_err}"
    error "Check log for details: ${serve_log}"
    exit 6
  fi
  # Command succeeded - log the success output (if any) for debugging
  echo "${ts_serve_err}" >>"${serve_log}"
fi

if ! final_status_out="$(tailscale_cmd funnel status 2>&1)"; then
  error "tailscale funnel status failed after setup: ${final_status_out}"
  exit 6
fi
if ! grep -q "127.0.0.1:${PORT}" <<<"${final_status_out}"; then
  error "tailscale funnel setup did not retain proxy mapping for port ${PORT}."
  error "Current funnel status: ${final_status_out}"
  exit 6
fi
if grep -q "(tailnet only)" <<<"${final_status_out}"; then
  error "tailscale reported only a tailnet-only route after Funnel setup."
  error "Current funnel status: ${final_status_out}"
  exit 6
fi

# Derive the tunnel URL from tailscale status (DNSName), not from funnel output.
TUNNEL_URL="$(get_tailscale_url)" || {
  error "Failed to derive Tailscale URL from 'tailscale status --json'."
  error "Verify Tailscale is connected: tailscale status"
  exit 6
}

mkdir -p "${SCRIPT_URL_FILE%/*}"
write_url_file "${TUNNEL_URL}" "${SCRIPT_URL_FILE}"

cat <<EOF

✅ Tailscale Funnel ready!
   tailscale url: ${TUNNEL_URL}
   log: ${serve_log}
   saved to: ${SCRIPT_URL_FILE}

EOF

echo "Use this URL in WorldArchitect settings:"
echo "  openclawGatewayUrl=${TUNNEL_URL}"
echo ""
echo "The URL is stable and will persist after reboot."
echo "To stop: tailscale funnel reset"
echo ""

if (( WAIT )); then
  cleanup_wait_mode() {
    echo ""
    echo "Stopping Tailscale Funnel..."
    if ! cleanup_status_out="$(tailscale_cmd funnel status 2>&1)"; then
      info "⚠️  Warning: unable to read tailscale funnel status during cleanup: ${cleanup_status_out}"
      exit 0
    fi
    if grep -q "127.0.0.1:${PORT}" <<<"${cleanup_status_out}"; then
      # Count all configured routes (|-- lines in status output).
      # If only one route is present (ours), reset is safe.
      # If multiple routes exist, skip the reset to avoid removing unrelated mappings.
      local route_count
      route_count="$(grep -c '^|--' <<<"${cleanup_status_out}" || echo 0)"
      if (( route_count > 1 )); then
        info "⚠️  Multiple Tailscale routes detected — skipping 'reset' to protect unrelated mappings."
        info "   Remove the OpenClaw route manually after reviewing: tailscale funnel status"
      else
        info "⚠️  WARNING: Resetting Tailscale Funnel config. This clears the OpenClaw route."
        if ! tailscale_cmd funnel reset; then
          info "⚠️  Warning: tailscale funnel reset failed — remove manually with: tailscale funnel reset"
        fi
      fi
    fi
    exit 0
  }
  trap cleanup_wait_mode INT TERM
  echo "Keeping script attached (no live log streaming). Press Ctrl-C to stop."
  while :; do sleep 3600; done
else
  echo "Tunnel is running in background."
  echo "To stop manually: tailscale funnel reset"
fi
