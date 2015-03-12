# encoding: utf-8
import re
from html.regx import drop_tree, find_tag
from html import text_content

# significant block section
class block(object):
    
    def __init__(self, body):
        self.body = body
    
    def __repr__(self):
        return '<%s body=\'%s\'>' % (self.__class__.__name__, self.body)
    
    @property
    def text(self):
        # return tags removed text
        return text_content(self.body)
    
    @property
    def a_droped_text(self):
        droped = drop_tree(drop_tree(self.body, 'a'), '\s')
        if len(droped) > 0:
            return text_content(droped)
        return u''
    
    @property
    def num_of_a(self):
        # return number of a tree
        return len(find_tag(self.body, 'a'))


# useless block section
class empty(block):
    
    def __init__(self):
        block.__init__(self, u'')
    
    def __repr__(self):
        return '<%s>' % self.__class__.__name__


class cluster(object):
    
    def __init__(self, blocks = [], points = 0):
        self.blocks = blocks if type(blocks) == list else [blocks]
        self.points = points
    
    @property
    def body(self):
        return '\n'.join([item.body for item in self.blocks])
    
    def append(self, block):
        self.blocks.append(block)
        return self
    
    def add_score(self, points):
        self.points += points
        return self

