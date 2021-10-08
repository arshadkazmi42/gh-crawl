# gh-crawl
Crawl all the urls from github organization / user public github repositories

## Install Dependencies

> Requires Python 3+

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

> Note: Output will be printed to stdout and will be written to file name {GITHUB USERNAME}.txt


## Local `run.sh`

```
# $1: Github Username / Organization Name
# $2: Github Token (Optional)

python3 scan.py $1 {REPLACE_WITH_GITHUB_TOKEN}

# This is to find unavailable github accounts
# Requires https://github.com/arshadkazmi42/bash-scripts

cat $1.txt | awk -F[/] '{print $1"//"$3"/"$4}' | sort | uniq | xargs -I {} sh ../bash-scripts/curl/scan-broken.sh {}
```

