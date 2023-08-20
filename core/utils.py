import re


DATETIME_NO_OFFSET_FORMAT = '%Y-%m-%dT%H:%M:%S.%f%z'


def simplify_string(char_string):
    """
    Formats a string by removing all spaces and setting
    all characters into lowercase.

        :param char_string: :type str:
            - The target string to format.
    """
    pattern = re.compile(r'\s+')
    return re.sub(pattern, '', char_string).lower()
