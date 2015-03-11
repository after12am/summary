# encoding: utf-8
import defs

# removes element from the tree, including its children and text
def drop_tree(dom, tag):
    for e in dom.xpath('%s' % tag):
        e.drop_tree()


# removes ignore elements with drop_tree()
def drop_ignore_trees(dom):
    for tag in defs.ignore_tags:
        drop_tree(dom, tag)
