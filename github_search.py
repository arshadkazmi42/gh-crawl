API = 'https://api.github.com/search/code?o=desc&q='
SEARCH_QUERY = 'org%3A{}+"{}"&type=Code&page='


class GithubSearch:

    def __init__(self, user, query):

        self.url = self.format_url(user, query)


    def format_url(self, user, query):

        searchQuery = SEARCH_QUERY.format(user, query)
        return f'{API}{searchQuery}'


    def result_total_pages(self):
