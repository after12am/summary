# -*- coding: utf-8 -*-
import sys
import re
import lxml.html
from lxml.etree import ParserError
import copy
from charset import force_unicode, htmlentity2unicode

script_regx = re.compile('<script.*?/script>', re.DOTALL)
noscript_regx = re.compile('<noscript.*?/noscript>', re.DOTALL)
style_regx = re.compile('<style.*?/style>', re.DOTALL)
iframe_regx = re.compile('<iframe.*?/iframe>', re.DOTALL)
select_regx = re.compile('<select.*?/select>', re.DOTALL)
comment_regx = re.compile('<!--.*?-->', re.DOTALL)

class _HTML(object):
    
    def __init__(self, document):
        self.threshold = 100
        self.min_length = 80
        self.continuous_factor = 1.62
        self.document = self.clean(force_unicode(document))
    
    def clean(self, document):
        # remove unnecessary tags from document
        document = htmlentity2unicode(document)
        # remove ignore tags
        document = script_regx.sub('', document)
        document = noscript_regx.sub('', document)
        document = style_regx.sub('', document)
        document = iframe_regx.sub('', document)
        document = select_regx.sub('', document)
        document = comment_regx.sub('', document)
        return document
    
    def extract(self):
        # extract main content from document
        dom = lxml.html.fromstring(self.document)
        blocks = self.divide_into_blocks(dom)
        # sort by score
        candidate = { 'body': None, 'score': 0, 'html': None }
        for b in self.analyse(blocks):
            if candidate['score'] < b['score']:
                candidate = b
        return candidate
    
    def divide_into_blocks(self, dom):
        # divide into layout blocks
        result = []
        content = ''
        for e in list(dom.xpath('body')[0]):
            content += lxml.html.tostring(e)
        # extract div content
        match = re.compile('<div.*?>|</div>|<h.>|</h.>', re.DOTALL).split(content);
        for m in match:
            # ignore content has only white spaces
            if len(re.compile('\s').sub('', m)) > 0:
                try:
                    b = _Block(m)
                except ParserError:
                    result.append(_Empty())
                else:
                    result.append(b)
            else:
                # we can not ignore empty block
                # has to influence distance of layout block
                result.append(_Empty())
        return result
    
    def analyse(self, blocks):
        # score each layout block and sort by their score
        factor = 1.0
        continuous = 1.0
        body = ''
        score = 0
        html = ''
        candidate = []
        # calculate score
        for b in blocks:
            if len(body) > 0:
                continuous /= self.continuous_factor
            if len(b.text) == 0:
                continue
            if len(b.reduced_text) == 0:
                continue
            b.calculate(factor, continuous)
            if b.score1 > self.threshold:
                body += b.text
                html += b.html
                score += b.score1
                continuous = self.continuous_factor
            elif b.score > self.threshold:
                candidate.append({ 'body': body, 'score': score, 'html': html })
                body = b.text
                html = b.html
                score = b.score
                continuous = self.continuous_factor
        candidate.append({ 'body': body, 'score': score, 'html': html })
        return candidate

class _Empty(object):
    
    def __init__(self):
        # represent for empty block
        self.html = ""
        self.text = ""
        self.reduced_text = ""
        self.score = 0
        self.score1 = 0

class _Block(object):
    
    def __init__(self, html):
        # represent for div and h1-h5 block
        self.decay_factor = 0.73
        dom = lxml.html.fromstring(html)
        self.html = html
        self.text = dom.text_content()
        self.reduced_text = self.reduce_text(dom)
        self.score = 0
        self.score1 = 0
    
    def reduce_text(self, dom):
        # remove links
        dom = copy.deepcopy(dom)
        a_list = dom.xpath('//a')
        a_count = len(a_list)
        try:
            for a in a_list:
                a.drop_tree()
        except AssertionError:
            pass
        # At least link-removed content has to have 20 charactors.
        if len(re.compile('\s').sub('', dom.text_content())) < 20 * a_count:
            return ""
        if is_collection_of_links(self):
            return ""
        return dom.text_content()
    
    def calculate(self, factor, continuous):
        # calculate score
        self.score = len(self.reduced_text) * factor
        factor *= self.decay_factor
        rate = not_body_rate(self)
        if rate > 0:
            self.score *= (0.72 ** rate)
        self.score1 = self.score * continuous

# we expect you to override in response to necessary.
# but need customize not necessarily.
def is_collection_of_links(block):
    # whether this layout block is a collection of links.
    return False

# we expect you to override in response to necessary.
# but need customize not necessarily.
def not_body_rate(block):
    # not_body_rate() takes account of not_body_rate.
    # return value has to be float or integer.
    return 0

def extract(document):
    html = _HTML(document)
    candidate = html.extract()
    return candidate

def extract_img(document):
    # get candidate block
    b = extract(document)
    dom = lxml.html.fromstring(b['html'])
    candidate = []
    for e in dom.xpath('//img'):
        candidate.append({'src': e.get('src'), 'alt': e.get('alt'), 'width': e.get('width'), 'height': e.get('height')});
    return candidate

def main():
    doc = '''
    <!DOCTYPE HTML>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title></title>
    </head>
    <body>
        <div>
            <img src="sample.jpeg"/>
            These portable speakers are made from laser-cut wood, fabric, veneer, and electronics. They are powered by three AAA batteries and compatible with any standard audio jack (e.g. on an iPhone, iPod, or laptop).
            <p>The speakers are an experiment in open-source hardware applied to consumer electronics. By making their original design files freely available online, in a way that's easy for others to modify, I hope to encourage people to make and modify them. In particular, I'd love to see changes or additions that I didn't think about and to have those changes shared publicly for others to use or continue to modify. The speakers have been designed to be relatively simple and cheap in the hopes of facilitating their production by others.</p>
        </div>
        <div>separator</div>
        <p>The speakers aren't yet available as a kit, but you can download the files and make them for yourself.</p>
        <div>Use 6mm (1/4") plywood. For the veneer, 1 9/16" edging backed with an iron-on adhesive is ideal (like this one from Rockler), but anything should work if you cut it to that width. Pick whatever fabric you like. For the electronic components, see the bill-of-materials above. You'll also need two-conductor speaker wire, available at Radio Shack.</div>
    </body>
    </html>
    '''
    print extract(doc)
    print extract_img(doc)

if __name__ == '__main__': main()