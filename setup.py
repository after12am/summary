import sys
sys.path.append('./summary')
sys.path.append('./test')

from distutils.core import setup
from setuptools import setup

description = """\
Extractor to get main content from the web page.
 - guessed title of main content
 - guessed main content
 - guessed summarization
 - candidate of main image

Install
sudo easy_install summary

Usages
visit at https://github.com/after12am/summary
"""

setup(
    name = "summary",
    packages = ["summary"],
    version = "0.2.0",
    install_requires = ["chardet", "lxml", "nltk", "numpy", "networkx"],
    description = "Extractor to get main content from the web page.",
    long_description = description,
    author = "Satoshi Okami",
    author_email = "me.after.12am@gmail.com",
    license = "MIT License",
    url = "https://github.com/after12am/summary",
    download_url = "https://github.com/after12am/summary/archive/master.zip",
    keywords = ["summary", "extract", "scraping", "web"],
    classifiers = [
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        "Operating System :: MacOS",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet"
    ],
    test_suite = 'testrunner'
)