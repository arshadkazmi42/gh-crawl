from github_search_result_item import GithubSearchResultItem

GH_RESULTS_PER_PAGE = 30
GH_MAX_PAGES = 34


class GithubResponseParser:

    def __init__(self, response):

        self.response = response


    def get_search_pages_count(self):

        response = self.response.json()

        # If total results are less than the total results in one page
        # Return 2, since page_numbers starts with 1.
        # So it needs to do 1 iteration
        total_count = 2
        
        if response and 'total_count' in response:
            total_count = response['total_count']

        if total_count > GH_RESULTS_PER_PAGE:
            total_count = int(total_count / GH_RESULTS_PER_PAGE) + 1

        if total_count > GH_MAX_PAGES:
            return GH_MAX_PAGES

        return total_count


    def get_search_results(self):

        response = self.response.json()

        if 'items' not in response:
            return None

        return [GithubSearchResultItem(item) for item in response['items']]


    def get_page_content(self):

        response = self.response.json()

        if 'content' not in response:
            return None

        return response['content']

    
    def get_archived_information(self):

        response = self.response.json()

        if not response or 'archived' not in response:
            return None

        return response['archived']
