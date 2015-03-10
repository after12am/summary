# encoding: utf-8
import re
from sect import block, empty
from html import drop_tag

def decompose(body):
    """
        Return decomposed sections from HTML document according to block level elements
    """
    # drop body tag if exist and strip
    body = drop_tag(body, u'body').strip()
    match = []
    hx = u''
    for m in [m for m in re.compile(r'<div.*?>|</div>|<(h[1-6]).*?>|</(h[1-6])>', re.DOTALL).split(body) if m]:
        _m = None
        if m:
            _m = re.compile(r'h[1-6]', re.DOTALL).match(m)
        if _m:
            if hx == u'':
                hx = u'<%s>' % _m.group()
            else:
                match.append(hx + u'</%s>' % _m.group())
                hx = u''
        elif hx:
            hx += m
        else:
            match.append(m)
    sects = []
    for m in match:
        # ignore content has only white spaces
        if len(re.compile(r'\s').sub(u'', m)) > 0:
            sects.append(block(m.strip()))
        # we can not ignore empty paragraph
        # has to influence distance of layout block
        else:
            sects.append(empty())
    return sects

# alias of decompose
parse = decompose