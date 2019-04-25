Package downloader

## INSTALL:

git clone git@github.com:Koodt/pkgdownloader.git

pip install pkgdownloader

## UNINSTALL:

pip uninstall pkgdownloader

## USAGE:

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
