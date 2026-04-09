import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# Add project root to path
sys.path.insert(0, os.getcwd())

from mvp_site import constants, intent_classifier


class TestIntentClassifierContext(unittest.TestCase):
    """Test context-aware classification logic."""

    @patch("mvp_site.intent_classifier.TextEmbedding")
    def test_classifier_concatenation(self, mock_embedding_cls):
        """Verify that context is concatenated with input text before embedding."""
        # Setup mock model
        mock_model = MagicMock()
        mock_embedding_cls.return_value = mock_model

        # Mock embed result
        import numpy as np

        mock_embedding = np.zeros(384)
        mock_model.embed.return_value = iter([mock_embedding])

        # Get classifier instance and force ready
        classifier = intent_classifier.LocalIntentClassifier.get_instance()
        classifier.model = mock_model
        classifier.ready = True
        classifier.anchor_embeddings = {
            constants.MODE_CHARACTER: np.random.rand(1, 384)
        }

        # Test classification with context
        text = "Hello"
        context = "The merchant smiles at you."

        classifier.predict(text, context=context)

        # Verify model.embed was called with concatenated string
        # Expected: Last AI text + separator + User text
        # (Using last 500 chars)
        expected_input = f"{context}\n\nUSER ACTION: {text}"
        mock_model.embed.assert_called_with([expected_input])

    @patch("mvp_site.intent_classifier.TextEmbedding")
    def test_classifier_context_truncation(self, mock_embedding_cls):
        """Verify that long context is truncated to last 500 characters."""
        # Setup mock model
        mock_model = MagicMock()
        mock_embedding_cls.return_value = mock_model

        # Mock embed result
        import numpy as np

        mock_embedding = np.zeros(384)
        mock_model.embed.return_value = iter([mock_embedding])

        # Get classifier instance and force ready
        classifier = intent_classifier.LocalIntentClassifier.get_instance()
        classifier.model = mock_model
        classifier.ready = True

        # Test classification with very long context
        text = "Hi"
        long_context = "A" * 1000 + "B" * 500

        classifier.predict(text, context=long_context)

        # Verify model.embed was called with truncated string
        # embed called with: ([text],) -> args[0] is the list of texts
        # call_args object from mock is (args, kwargs)
        args, _ = mock_model.embed.call_args
        text_arg = args[0][0]  # First arg (list), first element (string)

        self.assertEqual(len(text_arg), 500 + len("\n\nUSER ACTION: ") + len(text))
        self.assertTrue(text_arg.startswith("B" * 500))
        self.assertTrue(text_arg.endswith("USER ACTION: Hi"))


if __name__ == "__main__":
    unittest.main()
