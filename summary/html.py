# encoding: utf-8
import re
import defs

# removes the tag, but keeps its children and text
def drop_tag(html, tag):
    if tag == u'body':
        return re.compile(r'<%s.*?>|</%s>' % (tag, tag)).sub(u'', html)
    else:
        # not implemented except body tag
        pass


# removes element from the tree, including its children and text
def drop_tree(dom, tag):
    for e in dom.xpath('%s' % tag):
        e.drop_tree()


# removes ignore elements with drop_tree()
def drop_ignore_trees(dom):
    for tag in defs.ignore_tags:
        drop_tree(dom, tag)

