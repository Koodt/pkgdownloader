Package downloader

## INSTALL:

git clone git@github.com:Koodt/pkgdownloader.git

pip install pkgdownloader

## UNINSTALL:

pip uninstall pkgdownloader

## USAGE:

### Download tmux, aptitude, vim from Stable distribution to /srv

pkgdownload -p tmux aptitude vim -d stable -P /srv

### Download tmux from all distribution to default dir

pkgdownload -p tmux -d all

-p, --package - alone or multiply package list: tmux vim aptitude glibc6


-d, --distro  - alone or multiply distrib: jessie, oldstable, stretch, stable, buster, testing, sid, unstable
                all - for all distribution

-P, --path    - path to save packages: /folder/to/save, default /tmp
