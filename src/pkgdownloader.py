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
    parser.add_argument('-a', '--arch', nargs='*', dest='packageArch', default='amd64', help='package arch list, use: -a amd64 i386 arm64, default amd64')
    parser.add_argument('-p', '--package', nargs='*', dest='packageName', help='package name list, use: -p libmsgpack-dev aptitude tmux')
    parser.add_argument('-d', '--distro', nargs='*', dest='packageDistrib', help='dist, use: -d sid. FYI: all for all, jessie, oldstable, stretch, stable, buster, testing, sid, unstable')
    parser.add_argument('-P', '--path', action='store', dest='path', default='/tmp', help='Files saving path, default: /tmp', metavar="FILE")
    subparsers = parser.add_subparsers()
    parser_link = subparsers.add_parser('link', parents=[parser], help='Get links, without downloading')
    parser_link.set_defaults(act=link)
    parser_dl = subparsers.add_parser('dl', parents=[parser], help='Download packages')
    parser_dl.set_defaults(act=dl)
    parser_deps = subparsers.add_parser('deps', parents=[parser], help='Get dependencies list')
    parser_deps.set_defaults(act=deps)
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

def getLink(distrib, package, arch):
    url = 'https://packages.debian.org/' + distrib + '/' + arch + '/' + package + '/download'
    print('[...] Finding links for %s from %s' % (package, distrib))
    r = http.request('GET', url)
    soup = BeautifulSoup(r.data, 'html.parser')
    for link in soup.find_all('a', attrs={'href': re.compile('^http://ftp.ru')}):
        print('[ + ] For %s link find' % distrib)
        return link.get('href')

def downloadFile(link, targetFile):
    if os.path.isfile(targetFile):
        print('[!!!] File %s exists' % targetFile)
    else:
        print('[...] Downloading %s' % targetFile)
        with http.request('GET', link, preload_content=False) as r, \
        open(targetFile, 'wb') as out_file:
            shutil.copyfileobj(r, out_file)
            print('[+++] Download %s complete' % targetFile)

def getRepoPackagesFile(distrib, arch, comp):
    filename = str(uuid.uuid4())
    targetFile = '/tmp/' + filename + '.gz'
    url = 'http://ftp.ru.debian.org/debian/dists/' + distrib + '/' + comp + '/binary-' + arch + '/Packages.gz'
    downloadFile(url, targetFile)
    return targetFile

def packageDistribList(args):
    if args.packageDistrib == ['all']:
        packageDistrib = ['jessie', 'stretch', 'stretch-backports', 'buster', 'sid']
    else:
        packageDistrib = args.packageDistrib
    return packageDistrib

def dl(args):
    linksArray = []
    for package in args.packageName:
        for distrib in packageDistribList(args):
            link = getLink(distrib, package)
            if link:
                linksArray.append(link)
            else:
                print('[ ! ] Link for %s from %s not found' % (package, distrib))

    for link in linksArray:
        fileName = str(re.compile('[^/]*_.*').findall(link)).strip('\"\"\'\'[]')
        targetFile = args.path + '/' + fileName
        downloadFile(link, targetFile)

def link(args):
    linksArray = []
    for package in args.packageName:
        for distrib in packageDistribList(args):
            for arch in args.packageArch:
                link = getLink(distrib, package, arch)
                if link:
                    linksArray.append(link)
                else:
                    print('[ - ] Links not found')

    for link in linksArray:
        print(link)

def deps(args):

    print(getRepoPackagesFile(args.packageDistrib, 'amd64', 'main'))

def main():
    args = parseArgs()

    try:
        args.act(args)
    except AttributeError:
        print('You know hothing!')
