import re
import os
import shutil
import uuid

import gzip
import sys
import certifi
import urllib3

import json
import argparse

from bs4 import BeautifulSoup

def parseArgs():
    parser = argparse.ArgumentParser(description='Package downloader. Now only from packages.debian.org', usage='%(prog)s -p tmux aptitude vim -d stable -P /dir', add_help=False)
    parser.add_argument('-p', '--package', nargs='*', dest='packageName', help='package name list, use: -p libmsgpack-dev aptitude tmux')
    parser.add_argument('-d', '--distro', nargs='*', dest='packageDistrib', help='dist, use: -d sid. FYI: all for all, jessie, oldstable, stretch, stable, buster, testing, sid, unstable')
    parser.add_argument('-P', '--path', action='store', dest='path', default='/tmp', help='Files saving path, default: /tmp', metavar="FILE")
    subparsers = parser.add_subparsers()
    parser_link = subparsers.add_parser('link', parents=[parser], help='Get links, without downloading')
    parser_link.set_defaults(func=link)
    parser_dl = subparsers.add_parser('dl', parents=[parser], help='Download packages')
    parser_dl.set_defaults(func=dl)
    parser_deps = subparsers.add_parser('deps', parents=[parser], help='Get dependencies list')
    parser_deps.set_defaults(func=deps)
    return parser.parse_args()

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

def downloadFile(url, targetFile):
    with http.request('GET', url, preload_content=False) as r, \
    open(targetFile, 'wb') as out_file:
        shutil.copyfileobj(r, out_file)
    return

def getFileFromURL(path, distrib, package):

    url = 'https://packages.debian.org/' + distrib + '/amd64/' + package + '/download'

    for url in getLink(url, distrib, package):

        fileName = str(re.compile(package+'_.*').findall(url)).strip('\"\"\'\'[]')
        targetFile = path + '/' + fileName

        if os.path.isfile(targetFile):
            print('[!!!] File exists')
        else:
            print('[...] Downloading %s' % fileName)
            downloadFile(url, targetFile)
            print('[+++] Download %s to %s complete' % (fileName, path))

def getDependenciesFromDSC():
    return

def getRepoPackagesFile(distrib, arch, comp):
    filename = str(uuid.uuid4())
    targetFile = '/tmp/' + filename
#    http://ftp.ru.debian.org/debian/dists/sid/main/binary-amd64/Packages
    url = 'http://ftp.ru.debian.org/debian/dists/' + distrib + '/' + comp + '/binary-' + arch + '/Packages.gz'
    downloadFile(url, targetFile)

    return

def dl(args):
    if checkLinkStatus('https://packages.debian.org') == 200:

        if args.packageDistrib == ['all']:
            packageDistrib = ['jessie', 'stretch', 'stretch-backports', 'buster', 'sid']
        else:
            packageDistrib = args.packageDistrib

        for package in args.packageName:
            for distrib in packageDistrib:
                getFileFromURL(args.path, distrib, package)

def link(args):
    print('John Snow')

def deps(args):
    print('Aegon?')

def main():
    args = parseArgs()
    try:
        args.func(args)
    except AttributeError:
        print('You know hothing!')
