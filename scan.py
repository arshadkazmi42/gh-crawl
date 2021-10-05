from github_crawl import GithubCrawl


github_crawl = GithubCrawl()
github_crawl.start()

print("Processed in %s minutes" % github_crawl.get_elapsed_minutes())