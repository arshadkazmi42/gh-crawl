# gh-crawl
Crawl all the urls from github organization / user public github repositories

## Install Dependencies

```
$ pip install -r requirements.txt
```

## Usage

```
$ python scan.py {Github Username} {Github Token (Optional)}
```

## Example

```
$ python scan.py bugcrowd

```

## Notes

1. All processing logs will be stored in `{GITHUB_USERNAME}_process.txt` file
2. All links will be stored in `{GITHUB_USERNAME}_output.txt` file
3. All broken links will be storeg in `{GITHUB_USERNAME}_broken.txt` file
