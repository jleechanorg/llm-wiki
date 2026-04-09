"""Unit tests for campaign_utils DEFAULT_TEST_EMAIL behavior."""

from unittest.mock import MagicMock, patch

from testing_mcp.lib import campaign_utils


def test_collect_route_stream_events_uses_default_email_when_none():
    """When user_email is None, X-Test-User-Email header is set to DEFAULT_TEST_EMAIL."""
    mock_client = MagicMock()
    mock_client._base_url = "http://localhost:8001"

    with patch(
        "testing_mcp.lib.campaign_utils.urllib.request.urlopen"
    ) as mock_urlopen, patch(
        "testing_mcp.lib.campaign_utils.urllib.request.Request"
    ) as mock_request:
        mock_resp = MagicMock()
        mock_resp.readline.side_effect = [b"", b""]
        mock_urlopen.return_value.__enter__.return_value = mock_resp

        campaign_utils.collect_route_stream_events(
            mock_client,
            user_id="test-user",
            campaign_id="camp-123",
            user_input="hello",
            user_email=None,
        )

        mock_request.assert_called_once()
        call_kwargs = mock_request.call_args[1]
        headers = call_kwargs.get("headers", {})
        assert headers.get("X-Test-User-Email") == campaign_utils.DEFAULT_TEST_EMAIL


def test_post_streaming_request_uses_default_email_when_none():
    """When user_email is None, X-Test-User-Email header is set to DEFAULT_TEST_EMAIL."""
    mock_client = MagicMock()
    mock_client._base_url = "http://localhost:8001"

    with patch(
        "testing_mcp.lib.campaign_utils.urllib.request.urlopen"
    ) as mock_urlopen, patch(
        "testing_mcp.lib.campaign_utils.urllib.request.Request"
    ) as mock_request:
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.read.return_value = b"{}"
        mock_urlopen.return_value.__enter__.return_value = mock_resp

        campaign_utils.post_streaming_request(
            mock_client,
            user_id="test-user",
            campaign_id="camp-123",
            user_input="hello",
            user_email=None,
        )

        mock_request.assert_called_once()
        call_kwargs = mock_request.call_args[1]
        headers = call_kwargs.get("headers", {})
        assert headers.get("X-Test-User-Email") == campaign_utils.DEFAULT_TEST_EMAIL


def test_collect_route_stream_events_respects_explicit_email():
    """When user_email is provided, it is used (no default override)."""
    mock_client = MagicMock()
    mock_client._base_url = "http://localhost:8001"

    with patch(
        "testing_mcp.lib.campaign_utils.urllib.request.urlopen"
    ) as mock_urlopen, patch(
        "testing_mcp.lib.campaign_utils.urllib.request.Request"
    ) as mock_request:
        mock_resp = MagicMock()
        mock_resp.readline.side_effect = [b"", b""]
        mock_urlopen.return_value.__enter__.return_value = mock_resp

        campaign_utils.collect_route_stream_events(
            mock_client,
            user_id="test-user",
            campaign_id="camp-123",
            user_input="hello",
            user_email="custom@test.com",
        )

        mock_request.assert_called_once()
        call_kwargs = mock_request.call_args[1]
        headers = call_kwargs.get("headers", {})
        assert headers.get("X-Test-User-Email") == "custom@test.com"
