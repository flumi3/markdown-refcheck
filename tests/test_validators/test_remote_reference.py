"""Tests for remote reference validation."""

from unittest import mock

from refcheck.validators import is_valid_remote_reference


class TestIsValidRemoteReference:
    """Tests for is_valid_remote_reference function."""

    def test_valid_remote_reference_200(self, mock_http_success):
        """Test valid remote reference with 200 status code."""
        result = is_valid_remote_reference("https://www.example.com")
        assert result is True
        mock_http_success.assert_called_once_with(
            "https://www.example.com", timeout=5, verify=False
        )

    def test_valid_remote_reference_301(self, mock_http_301):
        """Test valid remote reference with 301 redirect."""
        result = is_valid_remote_reference("https://www.example.com")
        assert result is True

    def test_invalid_remote_reference_404(self, mock_http_404):
        """Test invalid remote reference with 404 status code."""
        result = is_valid_remote_reference("https://www.example.com/missing")
        assert result is False

    def test_invalid_remote_reference_500(self):
        """Test invalid remote reference with 500 server error."""
        with mock.patch("requests.head") as mock_request:
            mock_response = mock.Mock()
            mock_response.status_code = 500
            mock_request.return_value = mock_response

            result = is_valid_remote_reference("https://www.example.com/error")
            assert result is False

    def test_remote_reference_timeout(self, mock_http_timeout):
        """Test remote reference that times out."""
        result = is_valid_remote_reference("https://slow.example.com")
        assert result is False

    def test_remote_reference_connection_error(self, mock_http_connection_error):
        """Test remote reference with connection error."""
        result = is_valid_remote_reference("https://unreachable.example.com")
        assert result is False

    def test_remote_reference_ssl_error(self, mock_http_ssl_error):
        """Test remote reference with SSL certificate error."""
        result = is_valid_remote_reference("https://invalid-ssl.example.com")
        assert result is False

    def test_remote_reference_general_exception(self):
        """Test remote reference with general exception."""
        with mock.patch("requests.head") as mock_request:
            mock_request.side_effect = Exception("Unexpected error")

            result = is_valid_remote_reference("https://error.example.com")
            assert result is False

    def test_remote_reference_http_url(self, mock_http_success):
        """Test remote reference with HTTP (not HTTPS)."""
        result = is_valid_remote_reference("http://www.example.com")
        assert result is True
        mock_http_success.assert_called_once_with("http://www.example.com", timeout=5, verify=False)

    def test_remote_reference_with_path(self, mock_http_success):
        """Test remote reference with URL path."""
        result = is_valid_remote_reference("https://www.example.com/path/to/page")
        assert result is True

    def test_remote_reference_with_query_params(self, mock_http_success):
        """Test remote reference with query parameters."""
        result = is_valid_remote_reference("https://www.example.com?param=value")
        assert result is True

    def test_remote_reference_with_fragment(self, mock_http_success):
        """Test remote reference with URL fragment."""
        result = is_valid_remote_reference("https://www.example.com#section")
        assert result is True

    def test_remote_reference_timeout_value(self):
        """Test that timeout is set to 5 seconds."""
        with mock.patch("requests.head") as mock_request:
            mock_response = mock.Mock()
            mock_response.status_code = 200
            mock_request.return_value = mock_response

            is_valid_remote_reference("https://www.example.com")

            # Check that timeout=5 was passed
            _, kwargs = mock_request.call_args
            assert kwargs["timeout"] == 5

    def test_remote_reference_verify_disabled(self):
        """Test that SSL verification is disabled."""
        with mock.patch("requests.head") as mock_request:
            mock_response = mock.Mock()
            mock_response.status_code = 200
            mock_request.return_value = mock_response

            is_valid_remote_reference("https://www.example.com")

            # Check that verify=False was passed
            _, kwargs = mock_request.call_args
            assert kwargs["verify"] is False

    def test_remote_reference_status_code_boundary(self):
        """Test status code boundary (399 is valid, 400 is invalid)."""
        with mock.patch("requests.head") as mock_request:
            # Test 399 - should be valid
            mock_response = mock.Mock()
            mock_response.status_code = 399
            mock_request.return_value = mock_response
            result = is_valid_remote_reference("https://www.example.com")
            assert result is True

            # Test 400 - should be invalid
            mock_response.status_code = 400
            result = is_valid_remote_reference("https://www.example.com")
            assert result is False

    def test_remote_reference_multiple_calls(self, mock_http_success):
        """Test making multiple remote reference checks."""
        urls = [
            "https://example1.com",
            "https://example2.com",
            "https://example3.com",
        ]

        for url in urls:
            result = is_valid_remote_reference(url)
            assert result is True

        assert mock_http_success.call_count == 3
