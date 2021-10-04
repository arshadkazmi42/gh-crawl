import base64
import re


DECODE_FORMAT = 'utf-8'
# TODO Make it configurable
# URL_REGEX = r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9]{1,6}\b([-a-zA-Z0-9@:%_\+.~#?&\/=]*)'
URL_REGEX = r'https?:\/\/(www\.)?github.com\b([-a-zA-Z0-9@:%_\+.~#?&\/=]*)'
DELIMITER = '\n'


class SearchContent:

    def __init__(self, content):

        self.content = self.decode_base64(content)
        self.matches = []


    def decode_base64(self, content):

        try:
            return base64.b64decode(content).decode(DECODE_FORMAT) 
        except Exception as e:
            return None


    def extract_urls(self):

        for iterator in re.finditer(URL_REGEX, self.content):

            url = iterator.group()
            if url not in self.matches:

                self.matches.append(url)

        return self.matches


    def get_matches_string(self):

        if len(self.matches) == 0:
            return None

        return DELIMITER.join(self.matches)