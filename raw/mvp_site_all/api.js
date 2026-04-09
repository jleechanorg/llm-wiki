/* global firebase */
// Clock skew detection and compensation system
let clockSkewOffset = 0; // Detected clock skew in milliseconds
let clockSkewDetected = false;

// Centralized request timeout (mirrors scripts/timeout_config.sh exports so
// browser calls stay aligned with backend and Cloud Run limits)
const REQUEST_TIMEOUT_MS =
  Number(
    typeof window !== "undefined" &&
      typeof window.REQUEST_TIMEOUT_MS !== "undefined"
      ? window.REQUEST_TIMEOUT_MS
      : undefined,
  ) || 600000;

// Health checks should stay fast to avoid masking backend outages
const HEALTH_CHECK_TIMEOUT_MS = 5000;

/**
 * Detect and compensate for clock skew between client and server
 */
async function detectClockSkew() {
  try {
    console.log("🕐 Detecting clock skew...");
    const clientTimeStart = Date.now();
    const response = await fetch("/api/time", {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    });
    const clientTimeEnd = Date.now();

    if (response.ok) {
      const data = await response.json();
      const serverTime = data.timestamp_ms;
      const clientTimeAtRequest = clientTimeStart;
      const estimatedServerTime =
        serverTime - (clientTimeEnd - clientTimeStart) / 2;

      // Calculate clock skew (positive means client is ahead, negative means behind)
      clockSkewOffset = clientTimeAtRequest - estimatedServerTime;
      clockSkewDetected = true;

      if (Math.abs(clockSkewOffset) > 500) {
        console.log(
          `🕐 Clock skew detected: ${clockSkewOffset}ms (client ${clockSkewOffset > 0 ? "ahead" : "behind"})`,
        );
      }
    }
  } catch (error) {
    console.warn("⚠️ Could not detect clock skew:", error);
  }
}

/**
 * Apply clock skew compensation to token timing
 */
async function applyClockSkewCompensation() {
  // If we have detected clock skew and client is behind, wait before token generation
  if (clockSkewDetected && clockSkewOffset < 0) {
    const waitTime = Math.abs(clockSkewOffset) + 500; // Add 500ms buffer
    console.log(
      `⏱️ Applying clock skew compensation: waiting ${waitTime}ms before token generation`,
    );
    await new Promise((resolve) => setTimeout(resolve, waitTime));
  }
}

/**
 * Handle clock skew errors with enhanced detection and compensation
 */
async function handleClockSkewError(errorData) {
  if (errorData.error_type === "clock_skew" && errorData.server_time_ms) {
    const clientTime = Date.now();
    const serverTime = errorData.server_time_ms;
    const detectedSkew = clientTime - serverTime;

    // Update our clock skew offset with the server's measurement
    clockSkewOffset = detectedSkew;
    clockSkewDetected = true;

    console.log(`🔄 Updated clock skew from server error: ${detectedSkew}ms`);

    // Additional compensation delay for severe skew
    if (Math.abs(detectedSkew) > 2000) {
      await new Promise((resolve) =>
        setTimeout(resolve, Math.abs(detectedSkew) + 1000),
      );
    }
  } else if (!clockSkewDetected) {
    // Fallback: detect clock skew if we haven't already
    await detectClockSkew();
  }
}

// Initialize clock skew detection when the API module loads
if (typeof window !== "undefined") {
  detectClockSkew().catch((error) => {
    console.warn("Could not perform initial clock skew detection:", error);
  });
}

async function fetchApi(path, options = {}, retryCount = 0) {
  const startTime = performance.now();

  // Extract and normalize timeout handling while preserving any caller-provided signal
  const {
    signal: externalSignal,
    timeout: requestedTimeoutMs,
    ...restOptions
  } = options;
  const timeoutMs =
    typeof requestedTimeoutMs === "number"
      ? requestedTimeoutMs
      : REQUEST_TIMEOUT_MS;
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

  if (externalSignal) {
    if (externalSignal.aborted) {
      controller.abort(externalSignal.reason);
    } else {
      externalSignal.addEventListener(
        "abort",
        () => controller.abort(externalSignal.reason),
        {
          once: true,
        },
      );
    }
  }

  // Authentication flow
  let defaultHeaders = { "Content-Type": "application/json" };
  const tokenManager = window.authTokenManager;
  let forceRefresh = retryCount > 0;
  if (typeof options.forceRefresh === "boolean") {
    forceRefresh = options.forceRefresh;
  }

  // Check for test mode bypass before requiring Firebase user
  const isTestMode =
    window.testAuthBypass?.enabled ||
    window._testModeParams?.enabled ||
    (new URLSearchParams(window.location.search).get("test_mode") === "true" &&
      ["localhost", "127.0.0.1", "[::1]"].includes(window.location.hostname));

  if (!isTestMode) {
    const user = tokenManager?.getCurrentUser
      ? tokenManager.getCurrentUser()
      : firebase.auth().currentUser;
    if (!user) {
      console.error(
        "🔴 fetchApi: User not authenticated - firebase.auth().currentUser is null",
      );
      console.error("🔴 fetchApi: Path was:", path);
      throw new Error("User not authenticated");
    }

    // Apply clock skew compensation before token generation
    await applyClockSkewCompensation();
  }

  // Get fresh token, forcing refresh on retries to handle clock skew
  try {
    const authHeaders = tokenManager?.getAuthHeaders
      ? await tokenManager.getAuthHeaders(forceRefresh)
      : {
          Authorization: `Bearer ${await firebase.auth().currentUser.getIdToken(forceRefresh)}`,
        };

    defaultHeaders = { ...defaultHeaders, ...authHeaders };
  } catch (tokenError) {
    console.error("🔴 fetchApi: Failed to get auth token:", tokenError);
    console.error("🔴 fetchApi: forceRefresh was:", forceRefresh);
    throw tokenError;
  }

  const config = {
    ...restOptions,
    signal: controller.signal,
    headers: { ...defaultHeaders, ...options.headers },
  };

  console.log(
    `📤 fetchApi: Starting request to ${path} (timeout: ${timeoutMs}ms)`,
  );

  let response;
  try {
    response = await fetch(path, config);
    console.log(
      `📥 fetchApi: Response received from ${path} - status: ${response.status}`,
    );
  } catch (fetchError) {
    console.error("🔴 fetchApi: Fetch failed:", fetchError);
    console.error("🔴 fetchApi: Error name:", fetchError.name);
    console.error("🔴 fetchApi: Error message:", fetchError.message);
    console.error("🔴 fetchApi: Path was:", path);
    clearTimeout(timeoutId);
    throw fetchError;
  } finally {
    clearTimeout(timeoutId);
  }

  const duration = ((performance.now() - startTime) / 1000).toFixed(2);
  console.log(`⏱️ fetchApi: Request to ${path} completed in ${duration}s`);

  if (!response.ok) {
    console.error(
      `🔴 fetchApi: HTTP error ${response.status} ${response.statusText} for ${path}`,
    );
    let errorPayload = {
      message: `HTTP Error: ${response.status} ${response.statusText}`,
      traceback: `Status code ${response.status} indicates a server-side problem. Check the Cloud Run logs for details.`,
    };
    let jsonError = {};
    try {
      // Attempt to parse the body as JSON, it might contain our detailed error
      jsonError = await response.json();
      errorPayload.message = jsonError.error || errorPayload.message;
      errorPayload.traceback = jsonError.traceback || errorPayload.traceback;
    } catch (e) {
      // The response was not JSON. The server likely sent a plain HTML error page.
      console.error("Failed to parse error response as JSON.", e);
    }

    // Enhanced clock skew error handling with server synchronization
    if (response.status === 401 && retryCount < 2) {
      const isClockSkewError =
        errorPayload.message.includes("Token used too early") ||
        errorPayload.message.includes("clock") ||
        errorPayload.message.includes("time");

      if (isClockSkewError) {
        console.log(
          `🔄 Clock skew detected, retrying with fresh token (attempt ${retryCount + 1}/2)`,
        );

        // Handle clock skew errors with enhanced compensation
        await handleClockSkewError(jsonError);

        // Additional delay for severe clock skew
        const baseDelay = 1000;
        const skewDelay =
          clockSkewDetected && Math.abs(clockSkewOffset) > 1000
            ? Math.abs(clockSkewOffset)
            : 0;
        const totalDelay = baseDelay + skewDelay;

        if (skewDelay > 0) {
          console.log(
            `⏱️ Adding ${skewDelay}ms delay for clock skew compensation`,
          );
        }

        await new Promise((resolve) => setTimeout(resolve, totalDelay));
        return fetchApi(path, options, retryCount + 1);
      }

      // Fallback: refresh the ID token on generic 401 responses and retry once
      try {
        console.log(
          "🔁 401 received. Refreshing Firebase ID token and retrying request.",
        );
        const user = firebase.auth().currentUser;
        if (user) {
          await user.getIdToken(true);
          // Pass forceRefresh: true explicitly to ensure next attempt uses fresh headers
          return fetchApi(
            path,
            { ...options, forceRefresh: true },
            retryCount + 1,
          );
        }
      } catch (refreshError) {
        console.error("Token refresh after 401 failed:", refreshError);
      }
    }

    // Throw an object that our UI knows how to render.
    const error = new Error(errorPayload.message);
    error.traceback = errorPayload.traceback;
    error.errorType = jsonError.error_type;
    error.status = response.status;

    // Attach rate limit reset info if present
    if (
      jsonError.reset_time_hourly ||
      jsonError.reset_time_window ||
      jsonError.reset_time_daily
    ) {
      error.resetTime =
        jsonError.reset_time_hourly ||
        jsonError.reset_time_window ||
        jsonError.reset_time_daily;
      error.resetType = jsonError.reset_time_daily ? "daily" : "window";
    }

    throw error;
  }

  let data;
  try {
    data = await response.json();
    console.log(`✅ fetchApi: Successfully parsed JSON response from ${path}`);
  } catch (jsonError) {
    console.error("🔴 fetchApi: Failed to parse response as JSON:", jsonError);
    console.error("🔴 fetchApi: Response status was:", response.status);
    console.error(
      "🔴 fetchApi: Response headers:",
      Object.fromEntries(response.headers.entries()),
    );
    throw new Error("Failed to parse server response as JSON");
  }
  return { data, duration };
}

// RESILIENCE: Health check function to detect backend issues
async function checkBackendHealth() {
  const controller = new AbortController();
  const timeoutId = setTimeout(
    () => controller.abort(),
    HEALTH_CHECK_TIMEOUT_MS,
  );

  try {
    const response = await fetch("/api/health", {
      method: "GET",
      signal: controller.signal,
    });
    return response.ok;
  } catch (error) {
    console.warn("Backend health check failed:", error);
    return false;
  } finally {
    clearTimeout(timeoutId);
  }
}

// RESILIENCE: Connection status monitoring
let connectionStatus = {
  online: navigator.onLine,
  backendHealthy: true,
  lastCheck: Date.now(),
};

// Monitor network status with named handlers
const handleOnline = () => {
  connectionStatus.online = true;
  console.log("🌐 Network connection restored");
};

const handleOffline = () => {
  connectionStatus.online = false;
  console.log("📡 Network connection lost - switching to offline mode");
};

let networkListenersAttached = false;

function detachNetworkStatusListeners() {
  if (!networkListenersAttached) {
    return;
  }
  window.removeEventListener("online", handleOnline);
  window.removeEventListener("offline", handleOffline);
  networkListenersAttached = false;
}

function attachNetworkStatusListeners() {
  if (networkListenersAttached) {
    return;
  }
  window.addEventListener('online', handleOnline);
  window.addEventListener('offline', handleOffline);
  networkListenersAttached = true;
}

attachNetworkStatusListeners();
window.addEventListener('beforeunload', detachNetworkStatusListeners);

// RESILIENCE: Get connection status for UI decisions
function getConnectionStatus() {
  return {
    ...connectionStatus,
    canCreateCampaigns:
      connectionStatus.online && connectionStatus.backendHealthy,
    canViewCachedCampaigns: true, // Always true - we can show cached data
  };
}
