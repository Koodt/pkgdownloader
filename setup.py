from setuptools import setup

setup(
    name='pkgdownloader',
    version='0.0.1',
    description='Package downloader',
    author='Koodt',
    author_email='k0dt@k0dt.ru',
    url="http://k0dt.ru/",
    install_requires=[
        "bs4",
        "urllib3",
        "certifi",
        "argparse",
    ],
    entry_points={
        "console_scripts": [
            "pkgdownloader = src.pkgdownloader:main"
        ]
    },
)
