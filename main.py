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
# Traveling interval (specify with second).
# If you specify value is too small,
# you may be banned from twitter.com.
SLEEPING_TIME = 10
# Specify size option for download image.
# If you want to specify no option, you should set
# empty string.
# If download failed with this option, 
# program tries again with no option.
IMG_URL_SUFFIX = "orig"


ENCODING = "UTF-8"
WEB_ENCODING = "UTF-8"

def error_exit(msg):
    print(msg)
    print("Press enter-key to exit this program")
    input()
    sys.exit()

def post_request(url, data):
    return Request(url, urlencode(data).encode(ENCODING))

def read_accounts():
    exe_dir = os.path.dirname(os.path.abspath(__file__))
    lists_file = exe_dir + "/lists.txt"
    if not os.path.exists(lists_file):
        error_exit("lists.txt doesn't exist!")

    account_list = []
    with open(lists_file, "r") as f:
        for line in f.readlines():
            account = line.strip().replace("\n", "").replace("\r", "")
            if len(account) > 0:
                account_list.append(account)
    return account_list

def download_file(opener, url, account):
    exe_dir = os.path.dirname(os.path.abspath(__file__))
    save_dir = exe_dir + "/Download/" + account
    filename = url.rsplit("/", 1)[1]
    save_path = save_dir + "/" + filename

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    if os.path.exists(save_path):
        return

    if IMG_URL_SUFFIX:
        opt_url = url + ":" + IMG_URL_SUFFIX
    else:
        opt_url = url

    print("Download: " + opt_url)
    with opener.open(opt_url) as res:
        if res.code == 200:
            with open(save_dir + "/" + filename, "bw") as f:
                f.write(res.read())
        else:
            print("Download failed: " + opt_url)
            print("Download with no option: " + url)
            with opener.open(url) as res2:
                if res2.code == 200:
                    with open(save_dir + "/" + filename, "bw") as f:
                        f.write(res2.read())
                else:
                    print("Download failed: " + url)

def twitter_login(username, password):
    # Get a cookie
    cookie = CookieJar()
    opener = build_opener(HTTPCookieProcessor(cookie))
    with opener.open("https://twitter.com/login") as res:
        if res.code == 200:
            print("https://twitter.com/login " + str(res.code))
            page = res.read().decode(WEB_ENCODING)
        else:
            error_exit("Can't load https://twitter.com/login")

    # search an authenticity_token
    p = re.compile(r'<input type="hidden" value=".+" name="authenticity_token">')
    re_m = p.search(page).group()
    p = re.compile(r'value=".+"')
    re_m = p.search(re_m).group()
    auth_tk = re_m[7:47]

    # login to twitter.com without Twitter API
    print("login...")
    post_data = {
        "session[username_or_email]": username,
        "session[password]": password,
        "authenticity_token": auth_tk,
        "scribe_log": "",
        "redirect_after_login": "",
    }
    with opener.open(post_request("https://twitter.com/sessions", post_data)) as res:
        if res.code == 200:
            print("login success")
        else:
            error_exit("login failed! (response " + str(res.code) + ")")
        page = res.read().decode(WEB_ENCODING)
    return opener

print("Press Ctrl-c to terminate this program.")

alist = read_accounts()
if len(alist) == 0:
    error_exit("lists.txt is empty!")

print("Twitter Username:")
twitter_username = input()
twitter_password = getpass.getpass()
opener = twitter_login(twitter_username, twitter_password)

p = re.compile(r'data-image-url=".+"')
while True:
    for account in alist:
        print("Search pictures in @" + account)
        with opener.open("https://twitter.com/" + account) as res:
            if res.code != 200:
                error_exit("Page loading failed! (@" + account + "). Did you typo account name?")
            page = res.read().decode(WEB_ENCODING)

        for imgs in p.finditer(page):
            img_url = imgs.group().replace("data-image-url=", "").replace('"', "")
            download_file(opener, img_url, account)
        time.sleep(SLEEPING_TIME)

