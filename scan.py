from github_crawl import GithubCrawl


START_SIZE = 0
PAGE_SIZE = 200
MAX_SIZE = 2000

START_SIZE_LARGE = 2000
PAGE_SIZE_LARGE = 1000
MAX_SIZE_LARGE = 400000


for start in range(START_SIZE, MAX_SIZE, PAGE_SIZE):

    print(f'\nProcessing for page size: {start} - {start + PAGE_SIZE}')
    github_crawl = GithubCrawl(start, start + PAGE_SIZE)
    github_crawl.start()

for start in range(START_SIZE_LARGE, MAX_SIZE_LARGE, PAGE_SIZE_LARGE):

    print(f'\nProcessing for page size: {start} - {start + PAGE_SIZE_LARGE}')
    github_crawl = GithubCrawl(start, start + PAGE_SIZE_LARGE)
    github_crawl.start()

print('\nProcessed in %s minutes\n' % github_crawl.get_elapsed_minutes())