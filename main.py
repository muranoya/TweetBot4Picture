# coding: utf-8

import re
import os
import time
import sys
import getpass
import urllib.request
from urllib.request import build_opener, HTTPCookieProcessor, urlopen, Request
from urllib.parse   import urlencode
from http.cookiejar import CookieJar

#### Options
# Traveling interval (specify with second)
# If you specify value is too small,
# you may be banned from twitter.com.
SLEEPING_TIME = 10


ENCODING = "UTF-8"
WEB_ENCODING = "UTF-8"

def post_request(url, data):
    return Request(url, urlencode(data).encode(ENCODING))

def read_accounts():
    exe_dir = os.path.dirname(os.path.abspath(__file__))
    lists_file = exe_dir + "/lists.txt"
    account_list = []
    if not os.path.exists(lists_file):
        print("lists.txt doesn't exist!")
        sys.exit()
    with open(lists_file, "r") as f:
        for line in f.readlines():
            account_list.append(line.replace("\n", "").replace("\r", "").strip())
    return account_list

def download_file(opener, url, account):
    exe_dir = os.path.dirname(os.path.abspath(__file__))
    save_dir = exe_dir + "/Download/" + account
    filename = url.rsplit("/", 1)[1]
    save_path = save_dir + "/" + filename
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    if not os.path.exists(save_path):
        print("Download: " + url)
        with opener.open(url) as res:
            if res.code != 200:
                print("Download failed. " + url)
                sys.exit()
            with open(save_dir + "/" + filename, "bw") as f:
                f.write(res.read())

def twitter_login(username, password):
    cookie = CookieJar()
    opener = build_opener(HTTPCookieProcessor(cookie))
    with opener.open("https://twitter.com/login") as res:
        print("https://twitter.com/login " + str(res.code))
        page = res.read().decode(WEB_ENCODING)

    p = re.compile(r'<input type="hidden" value=".+" name="authenticity_token">')
    re_m = p.search(page).group()
    p = re.compile(r'value=".+"')
    re_m = p.search(re_m).group()
    auth_tk = re_m[7:47]

    post_data = {
        "session[username_or_email]": username,
        "session[password]": password,
        "authenticity_token": auth_tk,
        "scribe_log": "",
        "redirect_after_login": "",
    }
    print("login...")
    with opener.open(post_request("https://twitter.com/sessions", post_data)) as res:
        if res.code == 200:
            print("login success")
        else:
            print("login failed! (response " + str(res.code) + ")")
            sys.exit()
        page = res.read().decode(WEB_ENCODING)
    return opener

print("Press Ctrl-c to terminate this program.")
alist = read_accounts()

print("Twitter Username:")
twitter_username = input()
twitter_password = getpass.getpass()
opener = twitter_login(twitter_username, twitter_password)

p = re.compile(r'data-image-url=".+"')
while True:
    for account in alist:
        if len(account) == 0:
            continue
        print("Search pictures in " + account)
        with opener.open("https://twitter.com/" + account) as res:
            if res.code != 200:
                print("Page loading failed! (@" + account + ")")
                sys.exit()
            page = res.read().decode(WEB_ENCODING)
        for imgs in p.finditer(page):
            img_url = imgs.group().replace("data-image-url=", "").replace('"', "")
            download_file(opener, img_url, account)
        time.sleep(SLEEPING_TIME)

