from github_crawl import GithubCrawl


github_crawl = GithubCrawl()
github_crawl.start()

print('\nProcessed in %s minutes\n' % github_crawl.get_elapsed_minutes())