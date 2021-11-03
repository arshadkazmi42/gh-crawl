import base64
import re


from arguments import Arguments
from fyle import Fyle


HTTP = 'http'
GIT_PROTOCOL = 'git://'
HTTPS_PROTOCOL = 'https://'
RAW_GITHUB_URL = 'https://raw.githubusercontent.com'
GITHUBB_URL = 'https://github.com'

DECODE_FORMAT = 'utf-8'
# TODO Make it configurable
ALL_URLS_SEARCH=True
URL_REGEX = r'(https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9]{1,6}|github.com)\b([-a-zA-Z0-9@:%_\+.~#?&\/=]*)'
URL_REGEX_START = r'(git|https?):\/\/(www\.)?'
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
        
        if ALL_URLS_SEARCH:
            return self.format_full_url_regex()

        return self.format_custom_url_regex()
        

    def format_custom_url_regex(self):

        return URL_REGEX_START + re.escape(self.search_query) + URL_REGEX_END


    def format_full_url_regex(self):

        return URL_REGEX


    def decode_base64(self, content):

        try:
            return base64.b64decode(content).decode(DECODE_FORMAT) 
        except Exception as e:
            print(e)
            return None


    def extract_urls(self):

        if GIT_PROTOCOL in self.content:
            self.content = self.content.replace(GIT_PROTOCOL, HTTPS_PROTOCOL)

        for iterator in re.finditer(self.regex, self.content):

            url = iterator.group()
            if url not in self.matches:

                url = self.format_url(url)

                print(f'Found {url}')
                self.fyle.write(url)
                self.matches.append(url)

        return self.matches


    def get_matches_string(self):

        if len(self.matches) == 0:
            return None

        return DELIMITER.join(self.matches)

    
    def format_url(url):

        if not url.startswith(HTTP):
            url = f'{HTTPS_PROTOCOL}{url}'

        if url.startswith(RAW_GITHUB_URL):
            url = url.replace(RAW_GITHUB_URL, GITHUBB_URL)

        return url
