import unittest

from marmiton.extract_id_from_url import extract_id_from_url


class TestExtractIdFromUrl(unittest.TestCase):
    """Unit tests for the extract_id_from_url function"""

    def test_extract_id_from_valid_url(self):
        """Test with a valid URL containing an ID"""
        url = "https://assets.afcdn.com/recipe/20170607/67372_w300h300.webp"
        self.assertEqual(extract_id_from_url(url), "67372")
        url = "https://assets.afcdn.com/recipe/20200815/789012_w300h300.png"
        self.assertEqual(extract_id_from_url(url), "789012")

    def test_extract_id_from_placeholder_url(self):
        """Test with a placeholder URL"""
        url = (
            "https://assets.afcdn.com/recipe/20100101/ingredient_default_w300h300.webp"
        )
        self.assertIsNone(extract_id_from_url(url))

    def test_extract_id_from_empty_string(self):
        """Test with an empty string"""
        self.assertIsNone(extract_id_from_url(""))

    def test_extract_id_from_none(self):
        """Test with None"""
        self.assertIsNone(extract_id_from_url(None))

    def test_extract_id_from_invalid_url_format(self):
        """Test with a URL that doesn't match the pattern"""
        url = "https://example.com/image.jpg"
        self.assertIsNone(extract_id_from_url(url))

    def test_extract_id_from_url_without_webp(self):
        """Test with a URL without webp extension"""
        url = "https://assets.afcdn.com/recipe/20170607/67372_w300h300.jpg"
        self.assertIsNone(extract_id_from_url(url))

    def test_extract_id_from_url_without_supported_extension(self):
        """Test with a URL without supported extension (jpg, gif, etc.)"""
        url = "https://assets.afcdn.com/recipe/20170607/67372_w300h300.gif"
        self.assertIsNone(extract_id_from_url(url))

    def test_extract_id_from_url_different_size(self):
        """Test with a URL having a different size"""
        url = "https://assets.afcdn.com/recipe/20170607/67372_w150h150.webp"
        self.assertIsNone(extract_id_from_url(url))
        url = "https://assets.afcdn.com/recipe/20170607/67372_w150h150.png"
        self.assertIsNone(extract_id_from_url(url))

    def test_extract_id_from_url_with_letters_in_id(self):
        """Test with a URL containing letters in the ID (should not match)"""
        url = "https://assets.afcdn.com/recipe/20170607/abc123_w300h300.webp"
        self.assertIsNone(extract_id_from_url(url))
        url = "https://assets.afcdn.com/recipe/20170607/abc123_w300h300.png"
        self.assertIsNone(extract_id_from_url(url))

    def test_extract_id_from_url_with_query_params(self):
        """Test with a URL containing query parameters (should not match due to ?v=1)"""
        url = "https://assets.afcdn.com/recipe/20170607/67372_w300h300.webp?v=1"
        self.assertIsNone(
            extract_id_from_url(url)
        )
        url = "https://assets.afcdn.com/recipe/20170607/67372_w300h300.png?v=1"
        self.assertIsNone(
            extract_id_from_url(url)
        )

    def test_extract_id_from_url_case_sensitivity(self):
        """Test case sensitivity (Should not be case sensitive)"""
        url = "https://assets.afcdn.com/recipe/20170607/67372_w300h300.WEBP"
        self.assertEqual(
            extract_id_from_url(url), "67372"
        )
        url = "https://assets.afcdn.com/recipe/20200815/345678_w300h300.PNG"
        self.assertEqual(extract_id_from_url(url), "345678")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
