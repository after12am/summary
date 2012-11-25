# -*- coding: utf-8 -*-
import urllib, sys
from extractor import extract

def main():
    
    # japanese site
    
    try:
        uri = 'http://www.gizmodo.jp/2012/09/post_10869.html'
        print uri, '\n'
        res = extract(urllib.urlopen(uri).read())
        print 'Title: ', res['title'], '\n'
        print 'Content: ', res['body'], '\n'
        print 'Images: ', res['img'], '\n'
    except:
        print sys.exc_info()[0], sys.exc_info()[1]
    
    try:
        uri = 'http://labs.cybozu.co.jp/blog/nakatani/2007/09/web_1.html'
        print uri, '\n'
        res = extract(urllib.urlopen(uri).read())
        print 'Title: ', res['title'], '\n'
        print 'Content: ', res['body'], '\n'
        print 'Images: ', res['img'], '\n'
    except:
        print sys.exc_info()[0], sys.exc_info()[1]
    
    # english site
    
    try:
        uri = 'http://capturevision.wordpress.com/2009/08/05/music-visualizer-progress/'
        print uri, '\n'
        res = extract(urllib.urlopen(uri).read())
        print 'Title: ', res['title'], '\n'
        print 'Content: ', res['body'], '\n'
        print 'Images: ', res['img'], '\n'
    except:
        print sys.exc_info()[0], sys.exc_info()[1]
    
    try:
        uri = 'http://www.dasprinzip.com/prinzipiell/2012/04/03/shaders-in-their-natural-habitat-episode-1/'
        print uri, '\n'
        res = extract(urllib.urlopen(uri).read())
        print 'Title: ', res['title'], '\n'
        print 'Content: ', res['body'], '\n'
        print 'Images: ', res['img'], '\n'
    except:
        print sys.exc_info()[0], sys.exc_info()[1]
    
    try:
        uri = 'http://www.generatorx.no/20101217/abstrakt-abstrakt-jorinde-voigt/?utm_source=feedburner&utm_medium=feed&utm_campaign=Feed%3A+generatorx+%28Generator.x%3A+Generative+strategies+in+art+%26+design%29'
        print uri, '\n'
        res = extract(urllib.urlopen(uri).read())
        print 'Title: ', res['title'], '\n'
        print 'Content: ', res['body'], '\n'
        print 'Images: ', res['img'], '\n'
    except:
        print sys.exc_info()[0], sys.exc_info()[1]

if __name__ == '__main__': main()