# coding: utf-8
import re
import defs
import parser
import cluster
import urllib
import lxml.html
from char import detect_encoding, decode_entities

def fetch(uri):
    try:
        response = urllib.urlopen(uri)
        return response.read()
    except HTTPError, e:
        print 'The server couldn\'t fulfill the request.'
        print 'Error code: ', e.code
        print 'Reason: ', e.reason
    except URLError, e:
        print 'We failed to reach a server.'
        print 'Error code: ', e.code
        print 'Reason: ', e.reason
    except IOError, e:
        print 'We failed to fetch local file.'
        print 'Error code: ', e.code
        print 'Reason: ', e.reason
    return None

def drop_body_tag(body):
    body = lxml.html.tostring(body)
    return re.compile(r'<body>|</body>').sub(u'', body)

def highscore(clusts):
    clusts.sort(cmp=lambda a,b: cmp(b.score, a.score))
    return clusts[0]

def extract(html = None, uri = None, config = {}):
    
    data = html or fetch(uri = uri)
    if data is None:
        return False
    
    if type(data) is str:
        encoding = detect_encoding(data)
        data     = unicode(data, encoding, 'replace')
    
    dom = lxml.html.fromstring(data)
    
    for tag in defs.ignore_tags:
        for e in dom.xpath('//%s' % tag):
            e.drop_tree()
    
    body = drop_body_tag(dom.body)
    sections = parser.decompose(body)
    clusts = cluster.lbcluster(sections)
    best = highscore(clusts)
    
    # &lt;b&gt;bold&lt;/b&gt;
    return decode_entities(best.text)
