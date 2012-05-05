import sys
import re
import lxml.html
from lxml.etree import ParserError
import copy
from charset import force_unicode, htmlentity2unicode

threshold = 100
min_length = 80
decay_factor = 0.73
continuous_factor = 1.62

# compile regression
SCRIPT_REGX = re.compile('<script.*?/script>', re.DOTALL)
NOSCRIPT_REGX = re.compile('<noscript.*?/noscript>', re.DOTALL)
STYLE_REGX = re.compile('<style.*?/style>', re.DOTALL)
IFRAME_REGX = re.compile('<iframe.*?/iframe>', re.DOTALL)
SELECT_REGX = re.compile('<select.*?/select>', re.DOTALL)
COMMENT_REGX = re.compile('<!--.*?-->', re.DOTALL)

class _EmptyBlock(object):
    
    def __init__(self):
        self.html = ""
        self.text = ""
        self.reduced_text = ""
        self.score = 0
        self.score1 = 0
    
# represent div, section, article blocks
class _Block(object):
    
    def __init__(self, html):
        dom = lxml.html.fromstring(html)
        self.html = html
        self.text = dom.text_content()
        self.reduced_text = self._get_reduced_text(dom)
        self.score = 0
        self.score1 = 0
    
    def _get_reduced_text(self, dom):
        # return text removed link text
        dom = copy.deepcopy(dom)
        a_list = dom.xpath('//a')
        a_count = len(a_list)
        try:
            for a in a_list:
                a.drop_tree()
        except AssertionError:
            pass
        # at least link-removed content has to have 20 charactors.
        if len(re.compile('\s').sub('', dom.text_content())) < 20 * a_count:
            return ""
        if self.has_link_list():
            return ""
        return dom.text_content()
    
    def has_link_list(self):
        # not implemented
        return False
    
    def calculate_score(self, factor, continuous):
        self.score = len(self.reduced_text) * factor
        factor *= decay_factor
        _not_body_rate = not_body_rate()
        if _not_body_rate > 0:
            self.score *= (0.72 ** _not_body_rate)
        self.score1 = self.score * continuous

def _from_document(doc):
    # doc has to be html document.
    # return dom for mainly use of xpath and cssselect.
    return lxml.html.fromstring(doc)

def _candidate(dom):
    # return body content as list
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
                result.append(_EmptyBlock())
            else:
                result.append(b)
        else:
            # we can not ignore empty block
            # has to influence distance of layout block
            result.append(_EmptyBlock())
            
    return result

def _cleanup_document(doc):
    # remove ignore tags
    doc = SCRIPT_REGX.sub('', doc)
    doc = NOSCRIPT_REGX.sub('', doc)
    doc = STYLE_REGX.sub('', doc)
    doc = IFRAME_REGX.sub('', doc)
    doc = SELECT_REGX.sub('', doc)
    doc = COMMENT_REGX.sub('', doc)
    return doc

def _analyse(blocks):
    factor = 1.0
    continuous = 1.0
    body = ''
    score = 0
    candidate = []
    # calculate score
    for b in blocks:
        if len(body) > 0:
            continuous /= continuous_factor
        if len(b.text) == 0:
            continue
        if len(b.reduced_text) == 0:
            continue
        b.calculate_score(factor, continuous)
        if b.score1 > threshold:
            body += b.text
            score += b.score1
            continuous = continuous_factor
        elif b.score > threshold:
            candidate.append({ 'body': body, 'score': score })
            body = b.text
            score = b.score
            continuous = continuous_factor
    candidate.append({ 'body': body, 'score': score })
    return candidate

# we expect you to override in response to necessary.
# but need customize not necessarily.
def not_body_rate():
    # not_body_rate() takes account of not_body_rate.
    # return value has to be float or integer.
    return 0

def extract(doc):
    doc = force_unicode(doc)
    doc = htmlentity2unicode(doc)
    doc = _from_document(_cleanup_document(doc))
    blocks = _candidate(doc)
    # sort by score
    candidate = { 'body': None, 'score': 0 }
    for b in _analyse(blocks):
        if candidate['score'] < b['score']:
            candidate = b
    return candidate

def main():
    print extract('''
    <!DOCTYPE HTML>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title></title>
    </head>
    <body>
        <div>
            These portable speakers are made from laser-cut wood, fabric, veneer, and electronics. They are powered by three AAA batteries and compatible with any standard audio jack (e.g. on an iPhone, iPod, or laptop).
            <p>The speakers are an experiment in open-source hardware applied to consumer electronics. By making their original design files freely available online, in a way that's easy for others to modify, I hope to encourage people to make and modify them. In particular, I'd love to see changes or additions that I didn't think about and to have those changes shared publicly for others to use or continue to modify. The speakers have been designed to be relatively simple and cheap in the hopes of facilitating their production by others.</p>
        </div>
        <div>separator</div>
        <p>The speakers aren't yet available as a kit, but you can download the files and make them for yourself.</p>
        <div>Use 6mm (1/4") plywood. For the veneer, 1 9/16" edging backed with an iron-on adhesive is ideal (like this one from Rockler), but anything should work if you cut it to that width. Pick whatever fabric you like. For the electronic components, see the bill-of-materials above. You'll also need two-conductor speaker wire, available at Radio Shack.</div>
    </body>
    </html>
    ''')

if __name__ == '__main__': main()