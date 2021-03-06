import time

from arguments import Arguments
from request import Request
from sleep import Sleep


class RequestProcess:

    def __init__(self, url):
        
        self.request = Request(url)

        self.arguments = Arguments()
        self.sleep = Sleep()

    
    def get(self, headers=None, timeout=None):

        if not headers:
            headers = self.format_request_headers()

        response = self.request.get(headers, timeout)

        if response.status_code == 429:

            if self.is_wait_limit(response):

                return self.get(headers, timeout)

        if response.status_code == 403:

            self.print_error_message(response)

            if self.is_github_ratelimit(response):

                return self.get(headers, timeout)

        return response


    def format_request_headers(self):

        headers = {}
        github_token = self.arguments.get_github_token()

        if github_token:
            headers['Authorization'] = f'token {github_token}'

        return headers


    def is_wait_limit(self, response):

        sleep_time = None

        if 'Retry-After' in response.headers:

            sleep_time = int(response.headers['Retry-After'])

        self.sleep.start(sleep_time)

        return False


    def is_github_ratelimit(self, response):

        if 'X-RateLimit-Remaining' in response.headers:

            limit_remaining = int(response.headers['X-RateLimit-Remaining'])
            
            if limit_remaining == 0 and 'X-RateLimit-Reset' in response.headers:

                reset_time = int(response.headers['X-RateLimit-Reset'])
                current_time = int(time.time())
                sleep_time = reset_time - current_time + 1

                return self.sleep.start(sleep_time)
                        
        return False


    def print_error_message(self, response):

        error_resopnse = response.json()

        if 'message' in error_response:
            
            print(error_resopnse['message'])
