# encoding: utf-8
import re

def find_tag(html, tag):
    return re.compile(r'<%s.*?>.*?</%s>' % (tag, tag), re.DOTALL).findall(html)


# removes the tag, but keeps its children and text
def drop_tag(html, tag):
    if tag == u'body':
        return re.compile(r'<%s.*?>|</%s>' % (tag, tag)).sub(u'', html)
    else:
        # not implemented except body tag
        pass


# removes element from the tree, including its children and text
def drop_tree(html, tag):
    if tag == '\s':
        regx = re.compile(r'\s', re.DOTALL)
    else:
        regx = re.compile(r'<%s.*?>.*?</%s>' % (tag, tag), re.DOTALL)
    return regx.sub(u'', html)
