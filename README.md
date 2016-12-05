# TweetBot4Picture
This is a dedicated web crawler for pictures which are uploaded in twitter.
TweetBot4Picture monitors twitter accounts and automatically downloads pictures.

## Features
* Don't have to get Twitter API key.
  * This program accesses Twitter.com with HTTPS.
* Can monitor private accounts.
  * Your twitter account must follow the private accounts.

## How to use
You edit lists.txt and append accounts which you want to monitor, such as following:
    TwitterJP
    kantei
    muraoka_
lists.txt includes only twitter account (doesn't include @).
Write only one twitter account per line.

### On Windows
1. Download and Install Python3 [Download Python | Python.org](https://www.python.org/downloads/)
1. Move to a TweetBot4Picture directory.
1. Edit lists.txt
1. Run Python3
  1. ex. Run cmd.exe and type python.exe main.py
  1. If you don't add Python to the PATH environment, you specify full path of python.

### On *nix
1. Install Python3
1. Edit lists.txt
1. $ python3 main.py

