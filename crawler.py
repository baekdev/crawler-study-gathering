from urllib.request import urlopen
from bs4 import BeautifulSoup
from github import Github, Issue
import datetime
from pytz import timezone
from dateutil.parser import parse
import os

KST = timezone('Asia/Seoul')
today = datetime.datetime.now(KST)

def isDateInRange(created_at):
    suffix_KST = '.000001+09:00'
    created_at = parse(created_at + suffix_KST)
    yesterday = today - datetime.timedelta(1)
    return today > created_at and created_at > yesterday

site = 'https://okky.kr'
res = urlopen(site + '/articles/gathering?offset=0&max=20&sort=id&order=desc')
soup = BeautifulSoup(res, 'html.parser')
article_list = soup.select('#list-article ul > li.list-group-item')
issue_body = ''

for row in article_list:
    title = row.select('h5 > a')[0]
    published_at = row.select('div.date-created span.timeago')[0].get_text()
    item = published_at + " " +  str(title).replace('href="','href="' + site).replace("\n", "").replace('  ', '').strip() + '<br/>\n'
    if '마감' not in str(title) and isDateInRange(published_at):
        issue_body += item
    else: 
        print('[filtered] ', item)

print('----------------------------------------------------------------------')

issue_title = "스터디 모집 글 모음(%s)" % (today.strftime("%Y년 %m월 %d일 %H시"))
print(issue_title)
print(issue_body)

GITHUB_TOKEN = os.environ['GITHUB_TOKEN']
REPO_NAME = "crawler-study-gathering"
repo = Github(GITHUB_TOKEN).get_user().get_repo(REPO_NAME)
if issue_body != '' and REPO_NAME == repo.name:
    res = repo.create_issue(title=issue_title, body=issue_body)
    print(res)
