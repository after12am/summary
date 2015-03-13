# coding: utf-8
import re
import defs
import parser
import cluster
import urllib, urllib2
import digest
from cluster import lbttlscore
from lxml.html import fromstring, tostring
from html import text_content
from html.regx import drop_tree
from char import detect_encoding, decode_entities, to_unicode

# removes ignore elements with drop_tree()
def drop_ignore_trees(html):
    for tag in defs.ignore_tags:
        html = drop_tree(html, tag)
    dom = fromstring(html)
    # remove blogs comments
    for e in dom.cssselect("#comments,.comments"):
        e.drop_tree()
    return unicode(tostring(dom))


# extract body element except useless tags
def extract_normed_body(html):
    
    # Note
    #  - html.dom.drop_ignore_trees() can not except ignore tags in case of “summary/test/resources/html/music-visualizer-progress.html“
    
    # from html.dom import drop_tree, drop_ignore_trees
    # dom = fromstring(html)
    # dom = drop_ignore_trees(dom)
    # return to_unicode(tostring(dom.body))
    
    dom = fromstring(drop_ignore_trees(html))
    return to_unicode(tostring(dom.body))


class Article(object):
    
    def __init__(self, html, config = {}):
        self.html = html
        self.continuous_factor = 1.62
        self.decay_factor = .93
    
    # extracting title of main content
    @property
    def title(self):
        sects = parser.decompose(extract_normed_body(self.html))
        clusts = cluster.lbcluster(sects)
        # sorting cluster by their score
        clusts.sort(cmp=lambda a,b: cmp(b.points, a.points))
        # calcurate high score cluster
        best = clusts[0]
        if len(best.blocks) == 0:
            return False
        factor = 1.0
        continuous = 1.0
        bestmatch = [u'', 0]
        items = sects[:sects.index(best.blocks[0])]
        items.reverse()
        for b in items:
            if len(bestmatch[0]) > 0:
                continuous /= self.continuous_factor
            if len(b.text) == 0:
                continue
            factor *= self.decay_factor
            if lbttlscore(b, factor) * continuous > bestmatch[1]:
                bestmatch[0]  = b.text
                bestmatch[1] = lbttlscore(b, factor) * continuous
        return bestmatch[0]
    
    # extracting main content with tags
    @property
    def content(self):
        sects = parser.decompose(extract_normed_body(self.html))
        clusts = cluster.lbcluster(sects)
        # sorting cluster by their score
        clusts.sort(cmp=lambda a,b: cmp(b.points, a.points))
        best = clusts[0]
        if len(best.body) > 0:
            return decode_entities(best.body)
        return False
    
    # extracting main content without tags
    @property
    def text(self):
        content = self.content
        if type(content) == unicode and len(content) > 0:
            return text_content(content)
        return False
    
    # extracting summarization of content
    @property
    def digest(self):
        summarized = digest.summarize(self.text)
        return ''.join(summarized['top_n_summary'])
    
    # extracting content images
    @property
    def images(self):
        content = self.content
        data = fromstring(content)
        return [item.attrib for item in data.xpath('//img')]


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
            return False
        except urllib2.URLError, e:
            print 'We failed to reach a server.'
            print 'Error code: ', e.code
            print 'Reason: ', e.reason
            return False
        except IOError, e:
            print 'We failed to fetch local file.'
            print 'Error code: ', e.code
            print 'Reason: ', e.reason
            return False
    return Article(to_unicode(data))

