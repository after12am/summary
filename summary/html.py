# encoding: utf-8
import re
import defs

def drop_tag(html, tag):
    if tag == u'body':
        return re.compile(r'<%s.*?>|</%s>' % (tag, tag)).sub(u'', html)
    else:
        # not implemented for non body tag
        pass

def drop_tree(dom, tag):
    for e in dom.xpath('//%s' % tag):
        e.drop_tree()


def drop_ignore_tag(dom):
    for tag in defs.ignore_tags:
        drop_tree(dom, tag)

