# -*- coding: utf-8 -*-
import sys, re, copy
import lxml.html
from lxml.etree import ParserError
from charset import to_unicode, to_unicode_if_htmlentity

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
        self.decay_factor = 0.93
        self.document = self.clean(to_unicode(document))
    
    def clean(self, document):
        # remove unnecessary tags from document
        document = to_unicode_if_htmlentity(document)
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
        candidate = { 'title': None, 'body': None, 'score': 0, 'html': None }
        for b in self.analyse(blocks):
            if candidate['score'] < b['score']:
                candidate = b
        candidate['dom'] = dom
        return candidate
    
    def divide_into_blocks(self, dom):
        result = []
        content = ''
        for e in list(dom.xpath('body')[0]):
            content += lxml.html.tostring(e)
        # divide content into layout blocks
        match = [m for m in re.compile(r'<div.*?>|</div>|<(h.).*?>|</(h.)>', re.DOTALL).split(content) if m]
        new_match = []
        hx = ''
        for m in match:
            _m = None
            if m:
                _m = re.compile('h.', re.DOTALL).match(m)
            if _m:
                if hx == '':
                    hx = '<%s>' % _m.group()
                else:
                    new_match.append(hx + '</%s>' % _m.group())
                    hx = ''
            elif hx:
                hx += m
            else:
                new_match.append(m)
        match = new_match
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
        _blocks = []
        # calculate score of main content
        for b in blocks:
            if len(body) > 0:
                continuous /= self.continuous_factor
            if len(b.text) == 0:
                continue
            if len(b.reduced_text) == 0:
                continue
            factor *= self.decay_factor
            b.calculate_body_rate(factor, continuous)
            if b.score1 > self.threshold:
                body += b.text
                html += b.html
                score += b.score1
                _blocks.append(b)
                continuous = self.continuous_factor
            elif b.score > self.threshold:
                candidate.append({ 'body': body, 'score': score, 'html': html, 'blocks': _blocks })
                factor = 1.0
                body = b.text
                html = b.html
                score = b.score
                _blocks = [b]
                continuous = self.continuous_factor
        candidate.append({ 'body': body, 'score': score, 'html': html, 'blocks': _blocks })
        # calculate score of title
        for c in candidate:
            factor = 1.0
            continuous = 1.0
            title = ''
            score = 0
            if len(c['blocks']) and blocks.index(c['blocks'][0]) > 0:
                n = range(0, blocks.index(c['blocks'][0]) - 1)
                n.reverse()
                for b in [blocks[i] for i in n]:
                    if len(title) > 0:
                        continuous /= self.continuous_factor
                    if len(b.text) == 0:
                        continue
                    factor *= self.decay_factor
                    b.calculate_title_rate(factor, continuous)
                    if b.title_score1 > score:
                        score = b.title_score1
                        title = b.text
            c['title'] = title
        # remove temporary key
        for c in candidate:
            del c['blocks']
        return candidate

class _Empty(object):
    
    def __init__(self):
        # represent for empty block
        self.html = ""
        self.text = ""
        self.reduced_text = ""
        self.score = 0
        self.score1 = 0
        self.title_score = 0
        self.title_score1 = 0

class _Block(object):
    
    def __init__(self, html):
        # represent for div and h1-h6 block
        self.dom = lxml.html.fromstring(html)
        self.html = html
        self.text = self.dom.text_content()
        self.reduced_text = self.reduce_text(self.dom)
        self.score = 0
        self.score1 = 0
        self.title_score = 0
        self.title_score1 = 0
    
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
    
    def calculate_title_rate(self, factor, continuous):
        # calculate title score
        # define 40 as title regular length
        text = re.compile('\s').sub('', self.text)
        if not len(text): return
        self.title_score = (factor / len(self.text)) * 100
        m = re.compile(r'h(.)', re.DOTALL).match(self.dom.tag)
        if m:
            # h1 - h6
            self.title_score *= float(6.0 / float(m.groups()[0])) * 4.63
        self.title_score1 = self.title_score * continuous
    
    def calculate_body_rate(self, factor, continuous):
        # calculate score
        self.score = len(self.reduced_text) * factor
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
    dom = lxml.html.fromstring(candidate['html'])
    candidate.setdefault('img', [])
    for e in dom.xpath('//img'):
        candidate['img'].append({'src': e.get('src'), 'alt': e.get('alt'), 'width': e.get('width'), 'height': e.get('height')});
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
        <h1 id="header">Fab Speakers</h1>
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

if __name__ == '__main__': main()