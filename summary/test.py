# -*- coding: utf-8 -*-
import urllib, sys
from extractor import extract

urls = [
    # japanese site
    'http://www.gizmodo.jp/2012/09/post_10869.html',
    'http://labs.cybozu.co.jp/blog/nakatani/2007/09/web_1.html',
    # english site
    'http://capturevision.wordpress.com/2009/08/05/music-visualizer-progress/',
    'http://www.dasprinzip.com/prinzipiell/2012/04/03/shaders-in-their-natural-habitat-episode-1/',
    'http://www.generatorx.no/20101217/abstrakt-abstrakt-jorinde-voigt/?utm_source=feedburner&utm_medium=feed&utm_campaign=Feed%3A+generatorx+%28Generator.x%3A+Generative+strategies+in+art+%26+design%29'
]

def extract_test(url):
    try:
        print '==========' * 12 + '\n'
        print url, '\n'
        res = extract(urllib.urlopen(url).read())
        print '[Title]'
        print res['title'] + '\n'
        print '[Content]'
        print res['body'] + '\n'
        if len(res['img']):
            print '[Images]'
            for img in res['img']:
                print img['src']
            print '\n'
    except:
        print sys.exc_info()[0], sys.exc_info()[1]

def main():
    for url in urls:
        extract_test(url)

if __name__ == '__main__': main()