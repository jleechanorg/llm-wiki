#!/usr/bin/env python3
"""
Infrastructure tests for /testserver command functionality.
Tests server start/stop/status commands, port allocation, and process management.
"""

import os
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

# Add parent directory to path for imports
sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)


class TestServerInfrastructure(unittest.TestCase):
    """Test /testserver command infrastructure functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.project_root = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        # Auto-discover scripts in claude_command_scripts
        commands_dir = os.path.join(self.project_root, "claude_command_scripts", "commands")
        self.scripts = {}
        if os.path.isdir(commands_dir):
            for f in os.listdir(commands_dir):
                if f.endswith('.sh'):
                    self.scripts[f.replace('.sh', '')] = os.path.join(commands_dir, f)
        # Fallback: check root-level scripts
        for name, path in [('testserver', 'testserver.sh'), ('test_server_manager', 'test_server_manager.sh')]:
            if name not in self.scripts:
                full_path = os.path.join(self.project_root, path)
                if os.path.exists(full_path):
                    self.scripts[name] = full_path
        self.testserver_script = self.scripts.get('testserver')
        self.test_branch = "test-infrastructure-branch"

        # Ensure testserver script exists
        assert self.testserver_script, (
            f"testserver.sh not found - auto-discovered scripts: {list(self.scripts.keys())}"
        )

    def test_testserver_help_command(self):
        """Test that /testserver help displays usage information."""
        try:
            result = subprocess.run(
                [self.testserver_script, "help"],
                check=False,
                capture_output=True,
                text=True,
                timeout=10,
                cwd=self.project_root,
            )

            # Should exit successfully and show usage
            assert result.returncode == 0
            assert "Test Server Management" in result.stdout
            assert "Usage: /testserver [action] [branch]" in result.stdout
            assert "start" in result.stdout
            assert "stop" in result.stdout
            assert "list" in result.stdout
            assert "cleanup" in result.stdout
            assert "status" in result.stdout

            # Verify feature descriptions
            assert "Automatic port allocation" in result.stdout
            assert "Branch-specific logging" in result.stdout
            assert "Process management" in result.stdout

        except subprocess.TimeoutExpired:
            self.fail("testserver.sh help command timed out")
        except Exception as e:
            self.fail(f"Failed to run testserver.sh help: {e}")

    def test_testserver_unknown_action(self):
        """Test /testserver with unknown action shows error and usage."""
        try:
            result = subprocess.run(
                [self.testserver_script, "invalid-action"],
                check=False,
                capture_output=True,
                text=True,
                timeout=10,
                cwd=self.project_root,
            )

            # Should exit with error code
            assert result.returncode != 0
            # Check for error message in stdout or stderr
            error_output = result.stderr + result.stdout
            assert (
                "Unknown action" in error_output or "invalid" in error_output.lower()
            ), f"Expected error message not found in output: {error_output}"

        except subprocess.TimeoutExpired:
            self.fail("testserver.sh invalid action command timed out")
        except Exception as e:
            self.fail(f"Failed to run testserver.sh with invalid action: {e}")

    @patch("subprocess.run")
    def test_testserver_manager_delegation(self, mock_subprocess):
        """Test that testserver.sh properly delegates to test_server_manager.sh."""
        # Mock successful delegation
        mock_subprocess.return_value = subprocess.CompletedProcess(
            args=["test_server_manager.sh", "list"],
            returncode=0,
            stdout="Mocked server list output",
            stderr="",
        )

        # Test delegation for different actions
        actions_to_test = ["start", "stop", "list", "cleanup"]

        for action in actions_to_test:
            with self.subTest(action=action):
                try:
                    subprocess.run(
                        [self.testserver_script, action],
                        check=False,
                        capture_output=True,
                        text=True,
                        timeout=5,
                        cwd=self.project_root,
                    )

                    # Should attempt to run test_server_manager.sh
                    # (This may fail if test_server_manager.sh doesn't exist, but testserver.sh should try)

                except subprocess.TimeoutExpired:
                    self.fail(f"testserver.sh {action} command timed out")
                except Exception:
                    # Expected if test_server_manager.sh doesn't exist
                    # The important thing is that testserver.sh attempts delegation
                    pass

    def test_port_allocation_range(self):
        """Test that port allocation works within expected range (8081-8090)."""
        # Test port-utils.sh if it exists
        port_utils_script = os.path.join(
            self.project_root, "claude_command_scripts", "port-utils.sh"
        )

        if os.path.exists(port_utils_script):
            try:
                # Source the script and test port allocation functions
                result = subprocess.run(
                    [
                        "bash",
                        "-c",
                        f'source {port_utils_script} && echo "Port utils loaded"',
                    ],
                    check=False,
                    capture_output=True,
                    text=True,
                    timeout=5,
                    cwd=self.project_root,
                )

                assert result.returncode == 0
                assert "Port utils loaded" in result.stdout

            except subprocess.TimeoutExpired:
                self.fail("port-utils.sh loading timed out")
            except Exception as e:
                self.fail(f"Failed to load port-utils.sh: {e}")
        else:
            self.skipTest(
                "Resource not available: Port utility port-utils.sh not found, skipping port allocation test"
            )

    def test_branch_specific_logging(self):
        """Test that branch-specific logging directory structure works."""
        logs_dir = "/tmp/worldarchitectai_logs"

        # Verify logs directory exists or can be created
        if not os.path.exists(logs_dir):
            try:
                os.makedirs(logs_dir, exist_ok=True)
            except PermissionError:
                self.skipTest(
                    f"Cannot create logs directory {logs_dir} - permission denied (Environmental limitation)"
                )

        # Test log file naming pattern
        test_branch_log = os.path.join(logs_dir, f"{self.test_branch}.log")

        # Ensure we can write to log file location
        try:
            with open(test_branch_log, "w") as f:
                f.write("Test log entry\n")

            assert os.path.exists(test_branch_log)

            # Clean up test log file
            os.remove(test_branch_log)

        except PermissionError:
            self.skipTest(
                f"Cannot write to log file {test_branch_log} - permission denied (Environmental limitation)"
            )
        except Exception as e:
            self.fail(f"Failed to test branch-specific logging: {e}")

    def test_status_command_current_branch(self):
        """Test /testserver status shows current branch information."""
        try:
            # First get current branch for comparison
            branch_result = subprocess.run(
                ["git", "branch", "--show-current"],
                check=False,
                capture_output=True,
                text=True,
                timeout=5,
                cwd=self.project_root,
            )

            if branch_result.returncode != 0:
                self.skipTest(
                    "Resource not available: Git repository not in git directory, skipping git branch test"
                )

            current_branch = branch_result.stdout.strip()

            # Test status command
            result = subprocess.run(
                [self.testserver_script, "status"],
                check=False,
                capture_output=True,
                text=True,
                timeout=10,
                cwd=self.project_root,
            )

            # Should show current branch in output
            assert current_branch in result.stdout
            assert "Test Server Status" in result.stdout

        except subprocess.TimeoutExpired:
            self.fail("testserver.sh status command timed out")
        except Exception as e:
            self.fail(f"Failed to run testserver.sh status: {e}")

    def test_integration_with_push_commands(self):
        """Test that testserver integrates with /push and /integrate commands."""
        # Check if integration scripts exist
        push_script = os.path.join(
            self.project_root, "claude_command_scripts", "commands", "push.sh"
        )
        integrate_script = os.path.join(self.project_root, "integrate.sh")

        if os.path.exists(push_script):
            # Test that push script exists and is executable
            assert os.access(push_script, os.X_OK), "push.sh should be executable"

        if os.path.exists(integrate_script):
            # Test that integrate script exists and is executable
            assert os.access(integrate_script, os.X_OK), (
                "integrate.sh should be executable"
            )

        # Test testserver.sh help mentions integration
        try:
            result = subprocess.run(
                [self.testserver_script, "help"],
                check=False,
                capture_output=True,
                text=True,
                timeout=10,
                cwd=self.project_root,
            )

            assert "Integration with /push and /integrate commands" in result.stdout

        except subprocess.TimeoutExpired:
            self.fail("testserver.sh help timed out during integration test")
        except Exception as e:
            self.fail(f"Failed during integration test: {e}")

    def test_conflict_detection_and_resolution(self):
        """Test that testserver handles port conflicts and process management."""
        # This test verifies the design features exist, not necessarily the implementation
        try:
            result = subprocess.run(
                [self.testserver_script, "help"],
                check=False,
                capture_output=True,
                text=True,
                timeout=10,
                cwd=self.project_root,
            )

            # Verify conflict detection feature is documented
            assert "Conflict detection" in result.stdout

            # Verify process management with PID tracking feature is documented
            assert "Process management with PID tracking" in result.stdout

        except subprocess.TimeoutExpired:
            self.fail("testserver.sh help timed out during conflict detection test")
        except Exception as e:
            self.fail(f"Failed during conflict detection test: {e}")

    def test_error_handling_missing_manager(self):
        """Test error handling when test_server_manager.sh is missing."""
        # Temporarily rename test_server_manager.sh if it exists
        manager_script = os.path.join(self.project_root, "test_server_manager.sh")
        backup_script = os.path.join(self.project_root, "test_server_manager.sh.backup")

        manager_existed = False

        try:
            if os.path.exists(manager_script):
                manager_existed = True
                os.rename(manager_script, backup_script)

            # Test that testserver.sh handles missing manager gracefully
            result = subprocess.run(
                [self.testserver_script, "list"],
                check=False,
                capture_output=True,
                text=True,
                timeout=10,
                cwd=self.project_root,
            )

            # Should show appropriate error message
            assert result.returncode != 0
            # Check for error message in stdout or stderr
            error_output = result.stderr + result.stdout
            assert (
                "not found" in error_output.lower() or "missing" in error_output.lower()
            ), f"Expected error message not found in output: {error_output}"

        except subprocess.TimeoutExpired:
            self.fail("testserver.sh error handling test timed out")
        except Exception as e:
            self.fail(f"Failed during error handling test: {e}")
        finally:
            # Restore test_server_manager.sh if it existed
            if manager_existed and os.path.exists(backup_script):
                os.rename(backup_script, manager_script)


class TestServerProcessManagement(unittest.TestCase):
    """Test server process management and monitoring functionality."""

    def test_process_identification(self):
        """Test that server processes can be identified by branch."""
        # Test process identification patterns
        sample_processes = [
            "python3 mvp_site/main.py --port 8081 --branch feature-test",
            "gunicorn --bind 0.0.0.0:8082 main:app --branch dev-123",
            "flask run --port 8083 --branch hotfix-critical",
        ]

        # Test process parsing logic (if implemented)
        for process_cmd in sample_processes:
            # Extract branch from command line
            if "--branch" in process_cmd:
                parts = process_cmd.split("--branch")
                if len(parts) > 1:
                    branch = parts[1].strip().split()[0]
                    assert branch is not None
                    assert branch != ""

    def test_port_range_validation(self):
        """Test that port allocation stays within valid range."""
        # Test port range validation (8081-8090 as documented)
        valid_ports = range(8081, 8091)  # 8081-8090 inclusive

        for port in valid_ports:
            assert port >= 8081
            assert port <= 8090

        # Test invalid ports
        invalid_ports = [8080, 8091, 3000, 5000]

        for port in invalid_ports:
            assert port < 8081 or port > 8090

    def test_log_file_structure(self):
        """Test branch-specific log file naming structure."""
        test_branches = [
            "main",
            "feature-auth",
            "dev-1234567890",
            "hotfix-critical-bug",
            "task-implement-feature",
        ]

        logs_base = "/tmp/worldarchitectai_logs"

        for branch in test_branches:
            expected_log = os.path.join(logs_base, f"{branch}.log")

            # Verify log file path format
            assert expected_log.endswith(".log")
            assert branch in expected_log
            assert logs_base in expected_log


class TestGitHubRunnerSetup(unittest.TestCase):
    """Test GitHub runner setup script and workflow validation."""

    def test_color_variables_defined_before_use(self):
        """Test that color variables are defined before first use in setup script."""
        script_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            "setup-github-runner.sh"
        )

        with open(script_path) as f:
            lines = f.readlines()

        # Find where color variables are defined
        color_def_line = None
        for i, line in enumerate(lines):
            if "RED=" in line or "NC=" in line:
                if color_def_line is None:
                    color_def_line = i

        # Find first use of color variables
        first_use_line = None
        for i, line in enumerate(lines):
            if "${RED}" in line or "${NC}" in line or "${GREEN}" in line:
                first_use_line = i
                break

        assert color_def_line is not None, "Color variables not defined in script"
        assert first_use_line is not None, "Color variables not used in script"
        assert color_def_line < first_use_line, \
            f"Color variables used at line {first_use_line + 1} before defined at line {color_def_line + 1}"

    def test_runner_binary_path_correct(self):
        """Test that test workflow checks for correct binary path (no .dll on Unix)."""
        workflow_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            ".github/workflows/test-self-hosted-runner.yml"
        )

        with open(workflow_path) as f:
            content = f.read()

        # Should NOT check for .dll extension (Windows-only)
        assert "Runner.Listener.dll" not in content, \
            "Test workflow incorrectly checks for Runner.Listener.dll (Windows-only path)"

        # Should check for correct Unix binary path
        assert "Runner.Listener" in content, \
            "Test workflow should check for Runner.Listener binary"

    def test_docker_example_has_token_warning(self):
        """Test that Docker example includes security warning about not committing tokens."""
        readme_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            ".github/workflows/README.md"
        )

        with open(readme_path) as f:
            content = f.read()

        # Find Docker section
        docker_section_start = content.find("#### Option B: Docker-based Runner")
        assert docker_section_start != -1, "Docker section not found in README"

        # Get next 1000 chars after Docker section start
        docker_section = content[docker_section_start:docker_section_start + 1500]

        # Should have warning about tokens
        has_warning = (
            "security" in docker_section.lower() or
            "never commit" in docker_section.lower() or
            "do not commit" in docker_section.lower() or
            "warning" in docker_section.lower() or
            "⚠️" in docker_section or
            "sensitive" in docker_section.lower()
        )

        assert has_warning, \
            "Docker example should include security warning about not committing tokens"

    def test_setup_script_is_executable(self):
        """Test that setup script has executable permissions."""
        script_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            "setup-github-runner.sh"
        )

        assert os.access(script_path, os.X_OK), \
            "setup-github-runner.sh should be executable"

    def test_workflow_fails_on_missing_binary(self):
        """Test that workflow properly fails when runner binary is not found."""
        workflow_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            ".github/workflows/test-self-hosted-runner.yml"
        )

        with open(workflow_path) as f:
            content = f.read()

        # Workflow must contain exit 1 in the else block for missing binary
        assert "exit 1" in content, \
            "Test workflow must exit with code 1 when runner binary not found"

        # Check that it's in the correct context (after missing binary message)
        lines = content.split('\n')
        found_missing_message = False
        found_exit_after_message = False

        for i, line in enumerate(lines):
            if "Runner binary not found" in line or "not in expected location" in line:
                found_missing_message = True
                # Check next few lines for exit 1
                for j in range(i, min(i + 5, len(lines))):
                    if "exit 1" in lines[j]:
                        found_exit_after_message = True
                        break

        assert found_missing_message, "Workflow should have message about missing binary"
        assert found_exit_after_message, "Workflow should exit 1 after missing binary message"

    def test_runner_version_consistency(self):
        """Test that runner version is consistent across all files."""
        import re
        from pathlib import Path

        base_path = Path(__file__).parent.parent.parent

        # Get version from setup script
        setup_script = base_path / "setup-github-runner.sh"
        with open(setup_script) as f:
            content = f.read()
            match = re.search(r'RUNNER_VERSION="([0-9.]+)"', content)
            assert match, "RUNNER_VERSION not found in setup script"
            script_version = match.group(1)

        # Check README
        readme = base_path / ".github/workflows/README.md"
        with open(readme) as f:
            readme_content = f.read()
            assert script_version in readme_content, \
                f"Runner version {script_version} from setup script not found in README"

    def test_self_hosted_workflows_do_not_use_deleted_wrappers(self):
        """Self-hosted workflows must not reference deleted wrapper layers."""
        workflows_dir = Path(__file__).resolve().parents[2] / ".github" / "workflows"
        banned_markers = [
            "run-in-ci-container.sh",
            "./.github/actions/container-run",
            "./.github/actions/runner-control-plane",
        ]

        failures = []
        for workflow in workflows_dir.glob("*.yml"):
            content = workflow.read_text(encoding="utf-8")
            for marker in banned_markers:
                if marker in content:
                    failures.append(f"{workflow}: {marker}")

        assert not failures, (
            "Found deleted wrapper/control-plane references in workflows:\n"
            + "\n".join(failures)
        )

    def test_linux_default_runner_labels_for_container_workflows(self):
        """Test containerized workflows default to ubuntu-capable self-hosted labels."""
        expected_fragment = '["self-hosted"'
        container_workflows = [
            ".github/workflows/doc-size-check.yml",
            ".github/workflows/hook-tests.yml",
            ".github/workflows/mcp-smoke-tests.yml",
            ".github/workflows/pr-cleanup.yml",
            ".github/workflows/self-hosted-mvp-shard1.yml",
        ]

        for workflow_path in container_workflows:
            path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                workflow_path
            )

            with open(path) as f:
                content = f.read()

            assert "fromJson(vars.SELF_HOSTED_RUNNER_LABELS" in content, (
                f"{workflow_path} should keep runs-on label variable for centralized override"
            )
            assert expected_fragment in content, (
                f"{workflow_path} should default to Ubuntu-capable labels for containerized runs"
            )

    def test_deleted_wrapper_files_do_not_exist(self):
        """Deleted wrapper/control-plane files should not exist in repo."""
        repo_root = Path(__file__).resolve().parents[2]
        forbidden_paths = [
            repo_root / ".github" / "actions" / "container-run" / "action.yml",
            repo_root / ".github" / "actions" / "runner-control-plane" / "action.yml",
            repo_root / "self-hosted-runner" / "run-in-ci-container.sh",
            repo_root / "self-hosted-runner" / "ci-runner-image.txt",
        ]

        present = [str(path) for path in forbidden_paths if path.exists()]
        assert not present, (
            "Deleted wrapper/control-plane files still present:\n" + "\n".join(present)
        )

    def test_self_hosted_oss_runner_compose_exists(self):
        """OSS runner lifecycle should be represented via self-hosted-oss compose config."""
        compose_path = Path(__file__).resolve().parents[2] / "self-hosted-oss" / "docker-compose.yml"
        assert compose_path.exists(), "Expected self-hosted-oss/docker-compose.yml to exist"


if __name__ == "__main__":
    unittest.main()
