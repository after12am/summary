# encoding: utf-8
import re
from lxml.html import fromstring

class Section(object):
    
    TYPE_EMPTY = u'empty'
    TYPE_BLOCK = u'block'
    
    def __init__(self, type, body):
        self.type = type
        self.body = body
    
    def __repr__(self):
        if len(self.body) > 40:
            return u'<%s [%s]>' % (self.type, self.body[:40] + '...')
        return u'<%s [%s]>' % (self.type, self.body[:40])
    
    @property
    def a_droped(self):
        droped = re.compile(r'<a.*?>.*?</a>', re.DOTALL).sub(u'', self.body)
        droped = re.compile('\s').sub(u'', droped)
        if len(droped) == 0:
            return u''
        return unicode(fromstring(droped).text_content())
    
    @property
    def text(self):
        droped = self.a_droped
        if len(droped) == 0:
            return u''
        return fromstring(droped).text_content().strip()
    
    @property
    def num_of_a(self):
        return len(re.compile(r'<a.*?>.*?</a>', re.DOTALL).findall(self.body))


def decompose(body):
    """
        Return tokens which are decomposed from HTML document according to block elements
    """
    match = []
    hx = u''
    for m in [m for m in re.compile(r'<div.*?>|</div>|<(h[1-6]).*?>|</(h[1-6])>', re.DOTALL).split(body.strip()) if m]:
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
    sections = []
    for m in match:
        # ignore content has only white spaces
        if len(re.compile(r'\s').sub(u'', m)) > 0:
            sections.append(Section(
                Section.TYPE_BLOCK, 
                m.strip()
            ))
        # we can not ignore empty paragraph
        # has to influence distance of layout block
        else:
            sections.append(Section(
                Section.TYPE_EMPTY, 
                u''
            ))
    return sections


# alias of decompose
parse = decompose
