import unittest
from unittest.mock import patch, MagicMock
from src.aiservice.main.service import MessageService
from src.aiservice.main.entity import Expense


class TestMessageService(unittest.TestCase):
    def setUp(self):
        # Set up an instance of MessageService
        self.message_service = MessageService()

    @patch('src.aiservice.main.utils.MessageParser')
    @patch('src.aiservice.main.service.LLMService')
    def test_commons(self, mock_llm_service, mock_message_parser):
        # Test that the message service has a parser and LLM service
        mock_message_parser.parse_message.return_value = True

        # Create a mock Expense object
        mock_expense = Expense(amount=100.0, sender="John Doe", receiver="Jane Doe", date="2023-09-30")
        mock_llm_service.run.return_value = mock_expense

        # When the message contains relevant keywords, it should return the expected Expense
        result = self.message_service.process("INR 294.99 spent on ICICI Bank Card XX7003 on 23-Apr-24 at TW Coffee Kora. Avl Lmt: INR 43,266.15. To dispute,call 18002662/SMS BLOCK 7003 to 9215676766")
        self.assertEqual(result, mock_expense)

        # Verify that LLMService's run method is called once
        mock_llm_service.run.assert_called_once_with("INR 294.99 spent on ICICI Bank Card XX7003 on 23-Apr-24 at TW Coffee Kora. Avl Lmt: INR 43,266.15. To dispute,call 18002662/SMS BLOCK 7003 to 9215676766")

    @patch('src.aiservice.main.utils.MessageParser')
    @patch('src.aiservice.main.service.LLMService')
    def test_process_message_no_keywords(self, mock_llm_service, mock_message_parser):
        """
        Test when the message does not contain the required keywords
        """
        mock_message_parser.parse_message.return_value = False

        # When the parser returns False, the method should return None
        result = self.message_service.process("This is a random message")
        self.assertIsNone(result)

        # Verify that LLMService's run method is not called
        mock_llm_service.run.assert_not_called()

    @patch('src.aiservice.main.utils.MessageParser')
    @patch('src.aiservice.main.service.LLMService')
    def test_process_message_with_keywords(self, mock_llm_service, mock_message_parser):
        """
        Test when the message contains the required keywords
        """
        # Simulate the message having relevant keywords
        mock_message_parser.parse_message.return_value = True

        # Create a mock Expense object
        mock_expense = Expense(amount=100.0, sender="John Doe", receiver="Jane Doe", date="2023-09-30")
        mock_llm_service.run.return_value = mock_expense

        # When the message contains relevant keywords, it should return the expected Expense
        result = self.message_service.process("Transfer 100 dollars from John Doe to Jane Doe")
        self.assertEqual(result, mock_expense)

        # Verify that LLMService's run method is called once
        mock_llm_service.run.assert_called_once_with("Transfer 100 dollars from John Doe to Jane Doe")

    @patch('src.aiservice.main.utils.MessageParser')
    @patch('src.aiservice.main.service.LLMService')
    def test_process_message_llm_service_fails(self, mock_llm_service_class, mock_message_parser):
        """
        Test when the LLMService raises an exception or fails
        """
        # Create a mock instance of LLMService
        mock_llm_service_instance = mock_llm_service_class.return_value

        # Simulate the message having relevant keywords
        mock_message_parser.parse_message.return_value = True

        # Simulate LLMService throwing an exception when run is called
        mock_llm_service_instance.run.side_effect = Exception("LLM Service Failed")

        # The process method should raise the exception or handle it accordingly
        with self.assertRaises(Exception) as context:
            self.message_service.process("Transfer 100 dollars from John Doe to Jane Doe")

        # Verify the exception message if needed
        self.assertEqual(str(context.exception), "LLM Service Failed")

        # Verify that LLMService's run method was called once
        mock_llm_service_instance.run.assert_called_once_with("Transfer 100 dollars from John Doe to Jane Doe")


if __name__ == '__main__':
    unittest.main()
