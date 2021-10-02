GH_RESULTS_PER_PAGE = 30
GH_MAX_PAGES = 34


class GithubResponseParser:

    def __init__(self, response):

        self.response = response


    def get_search_pages_count(self):

        result = self.response.json()

        # If total results are less than the total results in one page
        # Return 2, since page_numbers starts with 1.
        # So it needs to do 1 iteration
        total_count = 2
        
        if result and 'total_count' in result:
            total_count = result['total_count']

        if total_count > GH_RESULTS_PER_PAGE:
            total_count = int(total_count / GH_RESULTS_PER_PAGE) + 1

        if total_count > GH_MAX_PAGES:
            return GH_MAX_PAGES

        return total_count


    def get_search_results(self):

        search_results = self.response.json()

    
    # def get_archived_response(self):

    #     if repo and 'archived' in repo:
    #         _print(f'{repo["name"]} => Archieved => {str(repo["archived"])}')
    #         return repo['archived']
