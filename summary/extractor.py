# coding: utf-8
import re
import parser
import cluster
import urllib, urllib2
from lxml.html import fromstring, tostring
from html import drop_tree, drop_ignore_tag
from char import detect_encoding, decode_entities, to_unicode

# extraction of main content which garbage has been removed
class Article(object):
    
    def __init__(self, html):
        self.html = html
    
    def __repr__(self):
        name = self.__class__.__name__
        if len(content) > 40:
            return '<%s content=\'%s\'>' % (name, content[:40] + '...')
        return '<%s content=\'%s\'>' % (name, content[:40])
    
    @property
    def body(self):
        dom = fromstring(self.html)
        drop_ignore_tag(dom)
        return to_unicode(tostring(dom.body))
    
    @property
    def guessed_title(self):
        pass
    
    @property
    def guessed_text(self):
        content = self.content.strip()
        if content != u'':
            text = fromstring(content).text_content()
            return to_unicode(text)
        return u''
    
    @property
    def guessed_content(self):
        sects = parser.decompose(self.body)
        clusts = cluster.lbcluster(sects)
        clusts.sort(cmp=lambda a,b: cmp(b.points, a.points))
        best = clusts[0]
        return decode_entities(best.body)
    
    @property
    def guessed_digest(self):
        pass
    
    @property
    def guessed_images(self):
        pass


# function for fetching URLs for many schemes using a variety of different protocols.
# instead of an 'http:', we can use 'ftp:', 'file:', etc.
def extract(html = None, uri = None, config = {}):
    data = html
    if data is None and uri is not None:
        try:
            response = urllib.urlopen(uri)
            data = response.read()
        except urllib2.HTTPError, e:
            print 'The server couldn\'t fulfill the request.'
            print 'Error code: ', e.code
            print 'Reason: ', e.reason
            return None
        except urllib2.URLError, e:
            print 'We failed to reach a server.'
            print 'Error code: ', e.code
            print 'Reason: ', e.reason
            return None
        except IOError, e:
            print 'We failed to fetch local file.'
            print 'Error code: ', e.code
            print 'Reason: ', e.reason
            return None
    return Article(data)
