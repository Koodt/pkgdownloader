#!/usr/bin/python3

import re

import sys
import certifi
import urllib3

import json
import argparse

from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description='Debian package downloader')
parser.add_argument('-p', '--package', nargs='*', dest='packageName', help='package name list, use: -p libmsgpack-dev aptitude tmux')
parser.add_argument('-d', '--distro', action='store', dest='packageDistrib', help='dist, use: -d sid. FYI: jessie, stretch, buster, sid')
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

def getLink(packageName, packageDistrib):
    r = http.request('GET', 'https://packages.debian.org/' + packageDistrib + '/amd64/' + packageName + '/download')
    soup = BeautifulSoup(r.data, 'html.parser')
    for link in soup.find_all('a', attrs={'href': re.compile("^http://ftp.ru")}):
        if checkLinkStatus(link.get('href')) == 200:
            print(link.get('href'))

def main():
    if checkLinkStatus('https://packages.debian.org') == 200:
        for package in args.packageName:
            getLink(package, args.packageDistrib)
