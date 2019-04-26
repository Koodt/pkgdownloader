Package downloader

## INSTALL:

git clone git@github.com:Koodt/pkgdownloader.git

pip install pkgdownloader

## UNINSTALL:

pip uninstall pkgdownloader

## USAGE:

### Get link

pkgdownloader link -p cpp-8 -a arm64 -d sid

[...] Finding links for cpp-8 from sid

[ + ] For sid link find

http://ftp.ru.debian.org/debian/pool/main/g/gcc-8/cpp-8_8.3.0-6_arm64.deb

### Download package

pkgdownloader dl -p cpp-8 -a arm64 -d sid

[...] Finding links for cpp-8 from sid

[ + ] For sid link find

[...] Downloading /tmp/cpp-8_8.3.0-6_arm64.deb

[+++] Complete

### Get package dependencies

pkgdownloader deps -p cpp-8 -a arm64 -d sid

[...] Finding links for cpp-8 from sid

[ + ] For sid link find

[...] Downloading /tmp/c90c32c2-0e70-494f-86e3-69e3e41cce35.gz

[+++] Complete

#### Output

Dependencies for 'cpp-8:arm64' from 'sid':

gcc-8-base

libc6

libgmp10

libisl19

libmpfr6

zlib1g

/tmp/c90c32c2-0e70-494f-86e3-69e3e41cce35.gz and /tmp/c90c32c2-0e70-494f-86e3-69e3e41cce35.txt removed



### Download tmux, aptitude, vim from Stable distribution to /srv

pkgdownload dl -p tmux aptitude vim -d stable -P /srv

### Get link tmux from jessie distribution

pkgdownload link -p tmux -d jessie

### Show dependencies mc amd64 from sid

pkgdownload deps -p mc -a amd64 -d sid

### Arguments

link      - Get links, without downloading

dl        - Download packages

deps      - Get dependencies list

-p, --package - alone or multiply package list: tmux vim aptitude glibc6


-d, --distro  - alone or multiply distrib: jessie, oldstable, stretch, stable, buster, testing, sid, unstable
                all - for all distribution

-P, --path    - path to save packages: /folder/to/save, default /tmp


