# encoding: utf-8
import re
from lxml.html import fromstring

class section(object):
    
    def __init__(self, body):
        self.body = body
    
    def __repr__(self):
        return '<%s body=\'%s\'>' % (self.__class__.__name__, self.body)
    
    @property
    def a_droped_text(self):
        droped = re.compile(r'<a.*?>.*?</a>', re.DOTALL).sub(u'', self.body)
        droped = re.compile(r'\s').sub(u'', droped)
        if len(droped) == 0:
            return u''
        return unicode(fromstring(droped).text_content().strip())
    
    @property
    def num_of_a(self):
        return len(re.compile(r'<a.*?>.*?</a>', re.DOTALL).findall(self.body))


class block(section):
    pass


class empty(section):
    
    def __init__(self):
        section.__init__(self, u'')
    
    def __repr__(self):
        return '<%s>' % self.__class__.__name__
