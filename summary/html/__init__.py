# encoding: utf-8
from lxml.html import fromstring
from lxml.etree import ParserError, XMLSyntaxError

# return unicoded text which HTML tags are removed
def text_content(html):
    try:
        return unicode(fromstring(html).text_content().strip())
    except ParserError, e:
        # asserted in case of being “</nav>” content
        return u''
    except XMLSyntaxError, e:
        return u''