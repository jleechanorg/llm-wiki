"""Tests for input_validation module."""

from mvp_site import input_validation


class TestValidateCampaignId:
    """Tests for validate_campaign_id."""

    def test_valid_uuid(self):
        assert input_validation.validate_campaign_id(
            "550e8400-e29b-41d4-a716-446655440000"
        )

    def test_valid_uuid_uppercase(self):
        assert input_validation.validate_campaign_id(
            "550E8400-E29B-41D4-A716-446655440000"
        )

    def test_valid_alphanumeric(self):
        assert input_validation.validate_campaign_id("my-campaign_123")

    def test_empty_string(self):
        assert not input_validation.validate_campaign_id("")

    def test_none(self):
        assert not input_validation.validate_campaign_id(None)

    def test_special_chars_rejected(self):
        assert not input_validation.validate_campaign_id("campaign/../etc")

    def test_spaces_rejected(self):
        assert not input_validation.validate_campaign_id("campaign with spaces")

    def test_sql_injection_rejected(self):
        assert not input_validation.validate_campaign_id("'; DROP TABLE campaigns;--")

    def test_too_long_rejected(self):
        assert not input_validation.validate_campaign_id("a" * 129)

    def test_max_length_accepted(self):
        assert input_validation.validate_campaign_id("a" * 128)


class TestValidateUserId:
    """Tests for validate_user_id."""

    def test_valid_uuid(self):
        assert input_validation.validate_user_id("550e8400-e29b-41d4-a716-446655440000")

    def test_valid_alphanumeric(self):
        assert input_validation.validate_user_id("user_123")

    def test_empty_string(self):
        assert not input_validation.validate_user_id("")

    def test_none(self):
        assert not input_validation.validate_user_id(None)

    def test_special_chars_rejected(self):
        assert not input_validation.validate_user_id("user@evil.com")

    def test_too_long_rejected(self):
        assert not input_validation.validate_user_id("u" * 129)


class TestSanitizeString:
    """Tests for sanitize_string."""

    def test_basic_string(self):
        assert input_validation.sanitize_string("hello world") == "hello world"

    def test_null_bytes_removed(self):
        assert input_validation.sanitize_string("hello\x00world") == "helloworld"

    def test_truncation(self):
        result = input_validation.sanitize_string("a" * 200, max_length=100)
        assert len(result) == 100

    def test_empty_string(self):
        assert input_validation.sanitize_string("") == ""

    def test_none(self):
        assert input_validation.sanitize_string(None) == ""

    def test_unicode_normalized(self):
        # e + combining acute accent -> single char
        result = input_validation.sanitize_string("e\u0301")
        assert result == "\u00e9"


class TestValidateRequestSize:
    """Tests for validate_request_size."""

    def test_small_payload(self):
        assert input_validation.validate_request_size({"key": "value"})

    def test_oversized_payload(self):
        large_data = {"key": "x" * (2 * 1024 * 1024)}
        assert not input_validation.validate_request_size(large_data)

    def test_custom_max_size(self):
        assert not input_validation.validate_request_size(
            {"key": "x" * 100}, max_size=10
        )

    def test_non_serializable(self):
        assert not input_validation.validate_request_size(object())


class TestValidateArraySize:
    """Tests for validate_array_size."""

    def test_valid_array(self):
        assert input_validation.validate_array_size([1, 2, 3])

    def test_oversized_array(self):
        assert not input_validation.validate_array_size(list(range(1001)))

    def test_custom_max(self):
        assert not input_validation.validate_array_size([1, 2, 3], max_size=2)

    def test_not_a_list(self):
        assert not input_validation.validate_array_size("not a list")


class TestValidateExportFormat:
    """Tests for validate_export_format."""

    def test_txt_valid(self):
        assert input_validation.validate_export_format("txt")

    def test_pdf_valid(self):
        assert input_validation.validate_export_format("pdf")

    def test_json_valid(self):
        assert input_validation.validate_export_format("json")

    def test_docx_valid(self):
        assert input_validation.validate_export_format("docx")

    def test_case_insensitive(self):
        assert input_validation.validate_export_format("TXT")
        assert input_validation.validate_export_format("PDF")

    def test_invalid_format(self):
        assert not input_validation.validate_export_format("exe")

    def test_empty_string(self):
        assert not input_validation.validate_export_format("")

    def test_none(self):
        assert not input_validation.validate_export_format(None)

    def test_non_string(self):
        assert not input_validation.validate_export_format(123)
