from urllib.request import urlopen
from bs4 import BeautifulSoup
from github import Github, Issue
import datetime
from pytz import timezone
import os

GITHUB_TOKEN = os.environ['GITHUB_TOKEN']
REPO_NAME = "crawler-study-gathering"

site = 'https://okky.kr'

res = urlopen(site + '/articles/gathering?offset=0&max=20&sort=id&order=desc')
soup = BeautifulSoup(res, 'html.parser')
article_list = soup.select('#list-article > div > ul > li.list-group-item')
issue_body = ''

KST = timezone('Asia/Seoul')
date = datetime.datetime.now(KST)
today = date.strftime("%Y-%m-%d")

for row in article_list:
    title = row.select('div > h5 > a')[0]
    published_at = row.select('div > div > div > div > span.timeago')[0].get_text()
    if '마감' not in str(title) and today in published_at:
        issue_body += published_at + " " +  str(title).replace('href="','href="' + site).replace("\n", "").replace('  ', '').strip() + '<br/>\n'

# ----------------------------------------------------------------------

issue_title = "스터디 모집 글 모음(%s)" % (date.strftime("%Y년 %m월 %d일 %H시"))
print(issue_title)
print(issue_body)

repo = Github(GITHUB_TOKEN).get_user().get_repo(REPO_NAME)
if issue_body != '' and REPO_NAME == repo.name:
    res = repo.create_issue(title=issue_title, body=issue_body)
    print(res)
