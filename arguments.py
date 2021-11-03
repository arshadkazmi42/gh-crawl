import sys
import random


DEFAULT_QUERY = 'github.com'


class Arguments:

    def __init__(self):
        
        self.args = sys.argv
        
        self.organization = None
        self.github_tokens = None
        self.search_query = None

        self.init()

    
    def init(self):

        self.format_organization()
        self.format_github_tokens()
        self.format_search_query()
        

    def format_organization(self):

        if len(self.args) < 2:
            raise Exception('Organzation / Username missing')

        self.organization = self.args[1]

    
    def format_github_tokens(self):

        if len(self.args) < 3:
          return

        self.github_tokens = self.args[2]
        self.github_tokens = self.github_tokens.split(',')


    def format_search_query(self):

        if len(self.args) < 4:
            self.search_query = DEFAULT_QUERY
            return

        self.search_query = self.args[3]


    def get_organization(self):

        self.organization


    def get_github_token(self):

        return random.choice(self.github_tokens)

    
    def get_search_query(self):

        self.search_query