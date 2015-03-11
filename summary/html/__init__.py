# encoding: utf-8
from lxml.html import fromstring

# return unicoded text which HTML tags are removed
def unicoded_text_content(html):
    return unicode(fromstring(html).text_content().strip())

# return str text which HTML tags are removed
def text_content():
    return fromstring(html).text_content().strip()
