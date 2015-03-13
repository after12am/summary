# encoding: utf-8
from lxml.html import fromstring
from lxml.etree import ParserError, XMLSyntaxError

# return unicoded text which HTML tags are removed
def text_content(html):
    try:
        dom = fromstring(html)
        if dom is not None:
            return unicode(dom.text_content().strip())
    except ParserError, e:
        # asserted in case of being “</nav>” content
        pass
    except XMLSyntaxError, e:
        pass
    return u''

