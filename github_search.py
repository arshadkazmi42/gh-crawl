from github_response_parser import GithubResponseParser
from request_process import RequestProcess
from sleep import Sleep


API = 'https://api.github.com/search/code?o=desc&q='
SEARCH_QUERY = 'org%3A{}+"{}"+NOT+filename:CHANGELOG.md+NOT+filename:Changelog&type=Code'


class GithubSearch:

    def __init__(self, user, query):

        self.url = self.format_url(user, query)
        self.sleep = Sleep()


    def format_url(self, user, query):

        searchQuery = SEARCH_QUERY.format(user, query)
        return f'{API}{searchQuery}'


    def get_url(self):

        return self.url


    def result_total_pages(self):

        request_process = RequestProcess(self.url)
        response = request_process.get()

        github_response_parser = GithubResponseParser(response)
        return github_response_parser.get_search_pages_count()


    def page_result(self, page_number):

        url = f'{self.url}&page={page_number}'

        request_process = RequestProcess(url)
        response = request_process.get()

        github_response_parser = GithubResponseParser(response)
        return github_response_parser.get_search_results()


    def page_content_result(self):

        request_process = RequestProcess(self.url)
        response = request_process.get()

        github_response_parser = GithubResponseParser(response)
        return github_response_parser.get_page_content()
