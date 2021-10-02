from request_process import RequestProcess


class GithubSearchResult:

    def __init__(self, search_result):

        self.search_result = search_result

    
    def is_archived(self):

        if self.has_respoitory_url(self):

            repository_url = self.search_result['repository']['url']
            request_process = RequestProcess(repository_url)

            response = request_process.get()

            # repo = _get_url_result(repo_url, gh_token)

            # if repo and 'archived' in repo:
            #     _print(f'{repo["name"]} => Archieved => {str(repo["archived"])}')
            #     return repo['archived']

            # return False

        return False


    def has_respoitory_url(self):

        if 'repository' not in self.search_result:
            return False

        if 'url' not in self.search_result['repository']:
            return False

        return True