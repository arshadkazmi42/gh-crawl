import base64
import re


from arguments import Arguments
from fyle import Fyle


DECODE_FORMAT = 'utf-8'
# TODO Make it configurable
# URL_REGEX = r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9]{1,6}\b([-a-zA-Z0-9@:%_\+.~#?&\/=]*)'
URL_REGEX_START = r'https?:\/\/(www\.)?'
URL_REGEX_END = r'\b([-a-zA-Z0-9@:%_\+.~#?&\/=]*)'
DELIMITER = '\n'


class SearchContent:

    def __init__(self, content):

        self.fyle = Fyle()
        self.arguments = Arguments()

        self.search_query = self.arguments.get_search_query()
        self.regex = self.format_regex()

        self.content = self.decode_base64(content)
        self.matches = []


    def format_regex(self):
        
        return URL_REGEX_START + self.search_query + URL_REGEX_END


    def decode_base64(self, content):

        try:
            return base64.b64decode(content).decode(DECODE_FORMAT) 
        except Exception as e:
            print(e)
            return None


    def extract_urls(self):

        for iterator in re.finditer(self.regex, self.content):

            url = iterator.group()
            if url not in self.matches:

                print(f'Found {url}')
                self.fyle.write(url)
                self.matches.append(url)

        return self.matches


    def get_matches_string(self):

        if len(self.matches) == 0:
            return None

        return DELIMITER.join(self.matches)