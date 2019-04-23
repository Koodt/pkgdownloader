#!/usr/bin/python3

import re
import shutil

import sys
import certifi
import urllib3

import json
import argparse

from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description='Package downloader. Now only from packages.debian.org', usage='%(prog)s -p tmux aptitude vim -d stable')
parser.add_argument('-p', '--package', nargs='*', dest='packageName', help='package name list, use: -p libmsgpack-dev aptitude tmux')
parser.add_argument('-d', '--distro', action='store', dest='packageDistrib', help='dist, use: -d sid. FYI: jessie, oldstable, stretch, stable, buster, testing, sid, unstable')
parser.add_argument('-P', '--path', action='store', dest='path', default='/tmp', help='Files saving path', metavar="FILE")
args = parser.parse_args()

if len(sys.argv) < 2:
    parser.print_help()
    sys.exit()

http = urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED',
        ca_certs=certifi.where())

def checkLinkStatus(myURL):
    r = http.request('GET', myURL)
    return r.status

def getLink(url):
    linksArray = []
    r = http.request('GET', url)
    soup = BeautifulSoup(r.data, 'html.parser')
    for link in soup.find_all('a', attrs={'href': re.compile('^http://ftp.ru')}):
        if checkLinkStatus(link.get('href')) == 200:
            linksArray.append(link.get('href'))
    return linksArray

def getFileFromURL(url, path, package):
    for url in getLink(url):
        with http.request('GET', url, preload_content=False) as r, \
        open(path + '/' + str(re.compile(package+'_.*').findall(url)).strip('\"\"\'\'[]'), 'wb') as out_file:
            shutil.copyfileobj(r, out_file)

def main():
    if checkLinkStatus('https://packages.debian.org') == 200:
        for package in args.packageName:
            url = 'https://packages.debian.org/' + args.packageDistrib + '/amd64/' + package + '/download'
            getFileFromURL(url, args.path, package)
