GITHUB_URL = 'https:/github.com'
GITHUB_PATH = '/blob/'
GITHUB_RAW_CONTENT_URL = 'https://raw.githubusercontent.com'
GITHUB_RAW_CONTENT_PATH = '/'


class GithubSearchResultItem:

    def __init__(self, search_result):

        self.search_result = search_result


    def has_respoitory_url(self):

        if 'repository' not in self.search_result:
            return False

        if 'url' not in self.search_result['repository']:
            return False

        return True


    def get_repository_url(self):

        if 'repository' not in self.search_result:
            return None

        if 'url' not in self.search_result['repository']:
            return None

        return self.search_result['repository']['url']


    def get_item_url(self):

        if 'url' not in self.search_result:
            return None

        return self.search_result['url']

    
    def get_html_url(self):

        if 'html_url' not in self.search_result:
            return None

        return self.search_result['html_url']

    
    def get_raw_content_url(self):
        
        html_url = self.get_html_url()
        if not html_url:
            return None

        html_url = html_url.replace(GITHUB_URL, GITHUB_RAW_CONTENT_URL)
        html_url = html_url.replace(GITHUB_PATH, GITHUB_RAW_CONTENT_PATH)

        return html_url