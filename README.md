Package downloader

INSTALL:
git clone git@github.com:Koodt/pkgdownloader.git
pip install pkgdownloader

UNINSTALL:
pip uninstall pkgdownloader

USAGE:
pkgdownload -p tmux aptitude vim -d stable -P /folder/to/save

-p, --package - multiply package list: tmux vim aptitude glibc6
-P, --path    - path to save packages: /folder/to/save, default /tmp
-d, --distro  - distrib: jessie, oldstable, stretch, stable, buster, testing, sid, unstable
