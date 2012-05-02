import sys
import re
import lxml.html
import copy
import htmlentitydefs
from charset import force_unicode

threshold = 100
min_length = 80
decay_factor = 0.73
continuous_factor = 1.62

# compile regression
SCRIPT_REGX = re.compile('<script.*?/script>')
NOSCRIPT_REGX = re.compile('<noscript.*?/noscript>')
STYLE_REGX = re.compile('<style.*?/style>')
IFRAME_REGX = re.compile('<iframe.*?/iframe>')
SELECT_REGX = re.compile('<select.*?/select>')
COMMENT_REGX = re.compile('<!--.*?-->')

REFERENCE_REGEX = re.compile(u'&(#x?[0-9a-f]+|[a-z]+);', re.IGNORECASE)
NUM16_REGEX = re.compile(u'#x\d+', re.IGNORECASE)
NUM10_REGEX = re.compile(u'#\d+', re.IGNORECASE)

class _Block(object):
    
    # represent div, section, article blocks
    def __init__(self, html):
        self.dom = lxml.html.fromstring(html)
        self.html = html
        self.text = self.dom.text_content()
        self.reduced_text = self._get_reduced_text()
        self.score = 0
        self.score1 = 0
    
    def _get_reduced_text(self):
        # return text removed link text
        dom = copy.deepcopy(self.dom)
        a_list = dom.xpath('//a')
        a_count = len(a_list)
        try:
            for a in a_list:
                a.drop_tree()
        except AssertionError:
            pass
        # at least link-removed content has to have 20 charactors.
        if len(dom.text_content()) < 20 * a_count:
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
        # take account of not_body_rate
        # now not_body_rate is not under consideration.
        self.score1 = self.score * continuous


def htmlentity2unicode(text):
    result = u''
    i = 0
    while True:
        match = REFERENCE_REGEX.search(text, i)
        if match is None:
            result += text[i:]
            break
        result += text[i:match.start()]
        i = match.end()
        name = match.group(1)
        if name in htmlentitydefs.name2codepoint.keys():
            result += unichr(htmlentitydefs.name2codepoint[name])
        elif NUM16_REGEX.match(name):
            result += unichr(int(u'0'+name[1:], 16))
        elif NUM10_REGEX.match(name):
            result += unichr(int(name[1:]))
    return result

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
    match = re.compile('<div.*?>|</div>', re.DOTALL).split(content);
    for m in match:
        # ignore content has only white spaces
        if len(re.compile('\s').sub('', m)) > 0:
            result.append(_Block(m))
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
    # calculate score
    factor = 1.0
    continuous = 1.0
    body = ''
    score = 0
    candidate = []
    
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

def extract(doc):
    doc = force_unicode(doc.lower())
    doc = htmlentity2unicode(doc)
    dom = _from_document(_cleanup_document(doc))
    blocks = _candidate(dom)
    # sort by score
    candidate = { 'body': None, 'score': 0 }
    for b in _analyse(blocks):
        if candidate['score'] < b['score']:
            candidate = b
    return candidate

def main():
    pass

if __name__ == '__main__': main()