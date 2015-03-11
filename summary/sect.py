# encoding: utf-8
import re
from html.regx import drop_tree, find_tag
from html import unicoded_text_content

# block level section
class block(object):
    
    def __init__(self, body):
        self.body = body
    
    def __repr__(self):
        return '<%s body=\'%s\'>' % (self.__class__.__name__, self.body)
    
    @property
    def text(self):
        # return tags removed text
        return unicoded_text_content(self.body)
    
    @property
    def a_droped_text(self):
        droped = drop_tree(drop_tree(self.body, 'a'), '\s')
        if len(droped) == 0:
            return u''
        return unicoded_text_content(droped)
    
    @property
    def num_of_a(self):
        # return number of a tree
        return len(find_tag(self.body, 'a'))


# non block level section
class empty(block):
    
    def __init__(self):
        block.__init__(self, u'')
    
    def __repr__(self):
        return '<%s>' % self.__class__.__name__
