# encoding: utf-8
import urllib, urllib2

# function for fetching URLs for many schemes using a variety of different protocols.
# instead of an 'http:', we can use 'ftp:', 'file:', etc.
def read(html = None, uri = None, config = {}):
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
    return data

