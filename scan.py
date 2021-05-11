import re
import requests
import base64
import json
import sys
import threading
from pathlib import Path
from datetime import datetime


URL_REGEX = r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9]{1,6}\b([-a-zA-Z0-9@:%_\+.~#?&\/=]*)'


GITHUB_SEARCH_API = 'https://api.github.com/search/code?q='
START_PAGE_NUMBER = 1
SEARCH_QUERY = 'user%3A{}+NOT+test+NOT+example+NOT+sample+NOT+mock+NOT+extension%3Ac+NOT+extension%3Acpp+NOT+extension%3Ah+NOT+extension%3Acctype=Code&page='
REQUEST_HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
GH_RESULTS_PER_PAGE = 30
GH_TOKEN = None
DEBUG = False



# HELPER FUNCTIONS

def _print(text):
    # TODO Add debug / verbose flag / accept from arg
    if DEBUG:
        print(text)

def _get_url(user):
    searchQuery = SEARCH_QUERY.format(user)
    _print(searchQuery)
    return f'{GITHUB_SEARCH_API}{searchQuery}'

def _get_github_username():
    args = sys.argv

    if len(args) < 2:
        _print('Missing username!')
        exit()

    return args[1]

def _get_gh_token():
    args = sys.argv

    _print(args)
    _print(len(args))

    if len(args) < 3:
        _print('Missing token')
        return

    return args[2]

def _check_rate_limit(response):
    if response.status_code == 403:
        if 'X-RateLimit-Reset' in response.headers:
            reset_time = int(response.headers['X-RateLimit-Reset'])
            current_time = int(time.time())
            sleep_time = reset_time - current_time + 1
            print(f'\n\nGitHub Search API rate limit reached. Sleeping for {sleep_time} seconds.\n\n')
            time.sleep(sleep_time)
            return True
    
    return False


def _is_broken_link(url):
    try:
        response = requests.head(url, headers=REQUEST_HEADERS, timeout=10)
        if response.status_code == 404:
            return True

        return False
    except Exception as e:
        _print(e)
        print(f'Error checking status code for {url}')
        return False


def _get_url_result(url, token):

    headers = {}    

    if not token and GH_TOKEN:
        token = GH_TOKEN

    if token:
        headers['Authorization'] = f'token {token}'

    _print(headers)

    response = requests.get(url, headers=headers)

    # if rate limit reached
    # Check and wait for x seconds
    if response.status_code == 403:
        if _check_rate_limit(response):
            response = requests.get(url)

    if response.status_code != 200:
        _print(f'Failed with error code {response.status_code}')
        return {}
        
    return response.json()

def _get_total_pages(url, gh_token):

    result = _get_url_result(f'{url}{START_PAGE_NUMBER}', gh_token)

    total_count = 1
    if 'total_count' in result:
        total_count = result['total_count']

    if total_count > GH_RESULTS_PER_PAGE:
        return int(total_count / GH_RESULTS_PER_PAGE) + 1

    # If total results are less than the total results in one page
    # Return 2, since page_numbers starts with 1.
    # So it needs to do 1 iteration
    return 2


def _decode_base_64(text): 
    return base64.b64decode(text).decode("utf-8") 


def _write_to_file(line, fname=None):
    filename = _get_github_username()
    if fname:
        filename = f'{filename}_{fname}.txt'
    else:
        filename = f'{filename}.txt'

    # check if line already present in file
    # do this only for broken
    if fname == 'broken' and _is_file_exists(filename):
        with open(filename) as f:
            file_content = f.read()
            if line in file_content:
                _print('\n\nLINE EXISTSS\n\n')
                return

    f = open(filename, 'a')
    f.write(f'{line}\n')  # python will convert \n to os.linesep
    f.close()

def _is_file_exists(file_path):
    fyle = Path(file_path)
    if fyle.is_file():
        return True
    return False

def _get_current_datetime():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def _search_content(url, content):

    _print(content)
    result = _decode_base_64(content)
    _print(str(result))

    print_line = f'[{_get_current_datetime()}] Scanning for {url}'
    print(print_line)
    _write_to_file(print_line, 'process')

    if 'example' not in url and 'test' not  in url and 'mock' not in url and 'sample' not in url:
        matches = [x.group() for x in re.finditer(URL_REGEX, result)]
        for i in range(0, len(matches)):
            matched_url = matches[i]
            _print(f'Processing {matched_url}')
            if _is_broken_link(matched_url):
                print_line = f'|-BROKEN-| {matched_url}'
                print(print_line)
                _write_to_file(matched_url, 'broken')
                _write_to_file(print_line, 'process')
            else:
                print_line = f'|---OK---| {matched_url}'
                print(print_line)
                _write_to_file(matched_url, 'output')
                _write_to_file(print_line, 'process')

def _is_archived(item, gh_token):
    if 'repository' in item and 'url' in item['repository']:
        repo_url = item['repository']['url']

        repo = _get_url_result(repo_url, gh_token)

        if 'archived' in repo:
            _print(f'{repo["name"]} => Archieved => {str(repo["archived"])}')
            return repo['archived']

        _print(f'{repo["name"]} => Archieved => False')
        return False

    return False

def _get_and_search_content(item, gh_token):

    if _is_archived(item, gh_token):
        return

    if 'url' in item:

        result = _get_url_result(item['url'], gh_token)
        html_url = item['html_url']

        if 'content' in result:
            _search_content(html_url, result['content'])

def run(url, page_number, gh_token):

    page_url = f'{url}{page_number}'
    print(page_url)
    result = _get_url_result(page_url, gh_token)

    if 'items' in result:
        items = result['items']

        for item in items:

            t1 = threading.Thread(target=_get_and_search_content, args=(item,gh_token))
            t1.daemon = True
            t1.start()
            t1.join()

# MAIN CODE

gh_token = _get_gh_token()

user = _get_github_username()

url = _get_url(user)

total_urls = 0
total_pages = _get_total_pages(url, gh_token)

for page_number in range(START_PAGE_NUMBER, total_pages):

    t = threading.Thread(target=run, args=(url, page_number, gh_token))
    t.daemon = True
    t.start()
    t.join()


