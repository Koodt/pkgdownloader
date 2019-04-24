#!/usr/bin/python3

import re
import shutil

import sys
import certifi
import urllib3

import json
import argparse

from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description='Package downloader. Now only from packages.debian.org', usage='%(prog)s -p tmux aptitude vim -d stable -P /dir')
parser.add_argument('-p', '--package', nargs='*', dest='packageName', help='package name list, use: -p libmsgpack-dev aptitude tmux')
parser.add_argument('-d', '--distro', nargs='*', dest='packageDistrib', help='dist, use: -d sid. FYI: all for all, jessie, oldstable, stretch, stable, buster, testing, sid, unstable')
parser.add_argument('-P', '--path', action='store', dest='path', default='/tmp', help='Files saving path, default: /tmp', metavar="FILE")
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

def getLink(url, distrib, package):
    print('[...] Finding links for %s from %s' % (package, distrib))
    linksArray = []
    r = http.request('GET', url)
    soup = BeautifulSoup(r.data, 'html.parser')
    for link in soup.find_all('a', attrs={'href': re.compile('^http://ftp.ru')}):
        if checkLinkStatus(link.get('href')) == 200:
            print('[!!!] For %s link find' % distrib)
            linksArray.append(link.get('href'))
    return linksArray

def getFileFromURL(path, distrib, package):
    url = 'https://packages.debian.org/' + distrib + '/amd64/' + package + '/download'
    for url in getLink(url, distrib, package):
        fileName = str(re.compile(package+'_.*').findall(url)).strip('\"\"\'\'[]')
        print('[...] Downloading %s' % fileName)
        with http.request('GET', url, preload_content=False) as r, \
        open(path + '/' + fileName, 'wb') as out_file:
            shutil.copyfileobj(r, out_file)
        print('[+++] Download %s to %s complete' % (fileName, path))

def getDependenciesFromDSC():
    return

def main():
    if checkLinkStatus('https://packages.debian.org') == 200:
        if args.packageDistrib == ['all']:
            packageDistrib = ['jessie', 'stretch', 'stretch-backports', 'buster', 'sid']
        else:
            packageDistrib = args.packageDistrib
        for package in args.packageName:
            for distrib in packageDistrib:
                getFileFromURL(args.path, distrib, package)
