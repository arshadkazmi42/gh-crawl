from multiprocessing.pool import ThreadPool as Pool

from arguments import Arguments
from fyle import Fyle
from github_response_parser import GithubResponseParser
from github_search import GithubSearch
from process_timer import ProcessTimer
from request_process import RequestProcess
from search_content import SearchContent


DEFAULT_QUERY = 'github.com'
MAX_THREADS = 5
START_PAGE_NUMBER = 1


class GithubCrawl:

    def __init__(self):

        self.arguments = Arguments()
        self.organization = self.arguments.get_organization()
        self.query = DEFAULT_QUERY

        self.fyle = Fyle()
        self.process_timer = ProcessTimer()
        self.github_search = GithubSearch(self.organization, self.query)


    def get_elapsed_minutes(self):

        return self.process_timer.get_elapsed_minutes()


    def start(self):
        
        self.total_pages = self.github_search.result_total_pages()
        self.url = self.github_search.get_url()

        for page_number in range(START_PAGE_NUMBER, self.total_pages):
    
            print(f'\n\nProcessing: {self.url}\nPage number: {page_number}\n')

            self.process_page(page_number)


    def process_page(self, page_number):

        results = self.github_search.page_result(page_number)

        pool = Pool(MAX_THREADS)

        for result in results:
            pool.apply_async(self.search_content, (result,))

        pool.daemon = True
        pool.close()
        pool.join()


    def search_content(self, result):

        if self.is_archived(result):
            return None

        url = result.get_item_url()
        request_process = RequestProcess(url)
        response = request_process.get()

        github_response_parser = GithubResponseParser(response)
        content = github_response_parser.get_page_content()

        search_content = SearchContent(content)
        search_content.extract_urls()


    def is_archived(self, result):

        repository_url = result.get_repository_url()

        if not repository_url:
            return False

        request_process = RequestProcess(repository_url)

        response = request_process.get()
        github_response_parser = GithubResponseParser(response)

        return github_response_parser.get_archived_information()
