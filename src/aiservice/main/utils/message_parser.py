import re

class MessageParser:
    @staticmethod
    def parse_message(message: str)->bool:
        """
        parse_message: This function takes a message string and returns True if the message is a palindrome
        :param message: str
        :return: bool
        """

        words_to_search = ['bank','transfer','send','money','account','credit','credited','debit','debited','account','balance','withdraw','deposit','transaction']
        message = message.lower()
        pattern = re.compile(r'\b(' + '|'.join(words_to_search) + r')\b', re.IGNORECASE)
        return bool(re.search(pattern, message))