"""Some helper functions for making requests to HTTP API"""

import re
import string
from unidecode import unidecode

PUNCTUATION_REGEX = re.compile('[%s]' % re.escape(string.punctuation))


def clean_string(s):
    """
    Remove punctuations, parentheses, and unidecode so that the string can be sent throught the Elsevier's API code
    """
    tmp_str = ' '.join(re.findall('(\w+|[0-9]+)',
                                  unidecode(PUNCTUATION_REGEX.sub(' ', s.replace(')', '').replace('(', ''))))).\
        lower()
    tmp_str = re.sub(r'\b(or|and)\b', '', tmp_str)
    return tmp_str