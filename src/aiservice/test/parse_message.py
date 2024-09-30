import unittest

from src.aiservice.main.utils import MessageParser


class TestMessageParser(unittest.TestCase):
    def test_custom_message(self):
        """
        Test case where the message is a custom message.
        """
        parser = MessageParser()
        message = "INR 294.99 spent on ICICI Bank Card XX7003 on 23-Apr-24 at TW Coffee Kora. Avl Lmt: INR 43,266.15. To dispute,call 18002662/SMS BLOCK 7003 to 9215676766"

        self.assertTrue(parser.parse_message(message))


    def test_parse_message_with_keywords(self):
        """
        Test cases where the message contains financial keywords.
        """
        parser = MessageParser()

        self.assertTrue(parser.parse_message("Please transfer the money to my account"))
        self.assertTrue(parser.parse_message("The account balance was credited"))
        self.assertTrue(parser.parse_message("Did you withdraw the deposit?"))
        self.assertTrue(parser.parse_message("Transaction completed successfully"))

    def test_parse_message_without_keywords(self):
        """
        Test cases where the message does not contain any financial keywords.
        """
        parser = MessageParser()

        self.assertFalse(parser.parse_message("Hello, how are you today?"))
        self.assertFalse(parser.parse_message("I love programming in Python"))
        self.assertFalse(parser.parse_message("The weather is nice and sunny"))

    def test_parse_message_with_mixed_case_keywords(self):
        """
        Test case where keywords are mixed case, testing case insensitivity.
        """
        parser = MessageParser()

        self.assertTrue(parser.parse_message("Your ACCOUNT has been Credited"))
        self.assertTrue(parser.parse_message("Please SEND the money"))

    def test_parse_message_partial_keywords(self):
        """
        Test case to ensure partial words that match keywords are not falsely identified.
        """
        parser = MessageParser()

        self.assertFalse(parser.parse_message("The banker is here"))
        self.assertTrue(parser.parse_message("The transaction was transacted"))
        self.assertTrue(parser.parse_message("I transferred my balance to another bank"))



class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
