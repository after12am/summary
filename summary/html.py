# -*- coding: utf-8 -*-
import sys, re, copy, urllib
import lxml.html
import digest
from lxml.etree import ParserError
from charset import to_unicode, to_unicode_if_htmlentity


class ContentExtractor(object):
    
    IGNORE_TAGS = ['script', 'noscript', 'style', 'iframe', 'select']
    
    def __init__(self, document, threshold = 100, continuous_factor = 1.62, decay_factor = .93):
        self.threshold = threshold
        self.continuous_factor = continuous_factor
        self.decay_factor = decay_factor
        self.raw = to_unicode(document)
        self.normalize()
    
    def normalize(self):
        """
             Removed ignore tags and comments from HTML document.
        """
        document = to_unicode_if_htmlentity(self.raw)
        document = re.compile('<!--.*?-->', re.DOTALL).sub('', document)
        for tag in self.IGNORE_TAGS:
            document = re.compile('<%s.*?/%s>' % (tag, tag), re.DOTALL).sub('', document)
        self.raw = document
    
    def dom(self):
        """
            Returns dom based on whether the string looks like a full document.
        """
        return lxml.html.fromstring(self.raw)
    
    def body(self):
        """
            Return body of HTML content
        """
        dom = self.dom()
        if dom is not None:
            body = ''
            for item in list(dom.xpath('body')[0]):
                body += lxml.html.tostring(item)
            return body
        return None
    
    def highscore(self):
        """
            Return high score Layout Block
        """
        top = None
        for item in self.cluster():
            if not top:
                top = item
            elif top.score < item.score:
                top = item
        return top
    
    def guessed_title(self):
        """
            Return the guessed title of the main content
        """
        return self.highscore().title
    
    def guessed_content(self):
        """
            Return the guessed main content of HTML document
        """
        return self.highscore().body
    
    def guessed_main_images(self):
        """
            Return candidate of main image
        """
        return [item.attrib for item in self.highscore().dom().xpath('//img')]
    
    def topics(self):
        """
            Return the topics, which mean keywords, of the main content.
        """
        pass
    
    def summarize(self):
        """
           Return guessed digest of HTML document.
        """
        summarized = digest.summarize(self.guessed_content())
        return ''.join(summarized['top_n_summary'])
    
    def summary(self):
        """
            Return data includes subject, content, topics and digest
        """
        return dict(
            title = self.guessed_title(),
            body = self.guessed_content(),
            digest = self.summarize(),
            img = self.guessed_main_images()
        )
    
    def decompose(self):
        """
            Return block are divided from HTML document.
        """
        match = []
        hx = ''
        for m in [m for m in re.compile(r'<div.*?>|</div>|<(h.).*?>|</(h.)>', re.DOTALL).split(self.body()) if m]:
            _m = None
            if m:
                _m = re.compile('h.', re.DOTALL).match(m)
            if _m:
                if hx == '':
                    hx = '<%s>' % _m.group()
                else:
                    match.append(hx + '</%s>' % _m.group())
                    hx = ''
            elif hx:
                hx += m
            else:
                match.append(m)
        block = []
        for m in match:
            # ignore content has only white spaces
            if len(re.compile('\s').sub('', m)) > 0:
                try:
                    b = _Block(m)
                except ParserError:
                    block.append(_EmptyBlock())
                else:
                    block.append(b)
            else:
                # we can not ignore empty block
                # has to influence distance of layout block
                block.append(_EmptyBlock())
        return block
    
    def cluster(self):
        """
            Return cluster which is consist of layout blocks depending on thier score  from HTML document.
        """
        factor = 1.0
        continuous = 1.0
        block = self.decompose()
        nascent = _LayoutBlock()
        cluster = []
        # calculate score of main content
        for b in block:
            if len(nascent.body) > 0:
                continuous /= self.continuous_factor
            if len(b.text_with_strip()) == 0 or len(b.text_without_link()) == 0:
                continue
            factor *= self.decay_factor
            if b.score1(factor, continuous) > self.threshold:
                nascent.put(b, factor, continuous)
                continuous = self.continuous_factor
            elif b.score(factor) > self.threshold:
                cluster.append(nascent)
                nascent = _LayoutBlock()
                nascent.put(b, factor, continuous)
                factor = 1.0
                continuous = self.continuous_factor
        cluster.append(nascent)
        # calculate score of title
        for item in cluster:
            factor = 1.0
            continuous = 1.0
            title, score = '', 0
            if len(item.component) and block.index(item.component[0]) > 0:
                n = range(0, block.index(item.component[0]) - 1)
                n.reverse()
                for b in [block[i] for i in n]:
                    if len(title) > 0:
                        continuous /= self.continuous_factor
                    if len(b.text_with_strip()) == 0:
                        continue
                    factor *= self.decay_factor
                    if b.title_score1(factor, continuous) > score:
                        score = b.title_score1(factor, continuous)
                        title = b.text_with_strip()
            item.title = title
        return cluster


class _LayoutBlock(object):
    
    """
        Layout Block represents for bundle of Blocks.
    """
    
    def __init__(self):
        self.title = ''
        self.body  = ''
        self.raw   = ''
        self.score = 0
        self.component = []
    
    def put(self, block, factor, continuous):
        self.body  += block.text_with_strip()
        self.raw   += block.raw
        self.score += block.score(factor)
        self.component.append(block)
    
    def dom(self):
        if self.raw:
            return lxml.html.fromstring(self.raw)
        return None


class _Block(object):
    
    """
        Block represents for block elements div and h1-6 element.
    """
    
    def __init__(self, string):
        self.raw = string
    
    def dom(self, deepcopy = False):
        """
            Returns dom based on whether the string looks like a full document.
        """
        if self.raw:
            try:
                dom = lxml.html.fromstring(self.raw)
                if dom is not None:
                    return copy.deepcopy(dom) if deepcopy else dom
            except ParserError:
                pass
        return None
    
    def text_with_strip(self):
        """
            Return tags removed text.
        """
        if self.dom() is not None:
            return self.dom().text_content().strip()
        return ''
    
    def text_without_link(self):
        """
          Return text the links were removed.
        """
        # cache for performance
        if hasattr(self, 'cache'):
            return  self.cache
        self.cache = ''
        dom = self.dom(deepcopy = True)
        if dom is not None:
            items = dom.xpath('//a')
            # drop link from dom tree
            for a in items:
                try:
                    a.drop_tree()
                except AssertionError:
                    pass
            norm = re.compile('\s').sub('', dom.text_content())
            # At least link-removed content has to have 20 charactors.
            if len(norm) < 20 * len(items) or is_collection_of_links(self):
                pass
            else:
                self.cache = dom.text_content()
        return self.cache
    
    def score(self, factor):
        """
            Return score of content
        """
        score = len(self.text_without_link()) * factor
        rate = not_body_rate(self)
        if rate > 0:
            score *= (0.72 ** rate)
        return score
    
    def score1(self, factor, continuous):
        """
            Return score1 of content
        """
        return self.score(factor) * continuous
    
    def title_score(self, factor):
        """
            Return score of title
        """
        # calculate title score
        # define 40 as title regular length
        text = re.compile('\s').sub('', self.text_with_strip())
        if not len(text):
            return 0
        score = (factor / len(self.text_with_strip())) * 100
        m = re.compile(r'h(.)', re.DOTALL).match(self.dom().tag)
        if m:
            # h1 - h6
            score *= float(6.0 / float(m.groups()[0])) * 4.63
        return score
    
    def title_score1(self, factor, continuous):
        """
            Return score1 of title
        """
        return self.title_score(factor) * continuous


class _EmptyBlock(_Block):
    
    def __init__(self):
        super(_EmptyBlock, self).__init__('')


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
    extractor = ContentExtractor(document)
    return extractor.summary()

def main():
    document = '''
    <!DOCTYPE HTML>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title></title>
        <style>
        body {
            background: #000;
        }
        </style>
    </head>
    <body>
        <script type="type/javascript">alert();</script>
        <noscript>this is part of noscript</noscript>
        <iframe>this is part of iframe</iframe>
        <h1 id="header">Fab Speakers</h1>
        <div>
            <img src="sample.jpeg" width="200" height="200" alt=""/>
            These portable speakers are made from laser-cut wood, fabric, veneer, and electronics. They are powered by three AAA batteries and compatible with any standard audio jack (e.g. on an iPhone, iPod, or laptop).
            <p>The speakers are an experiment in open-source hardware applied to consumer electronics. By making their original design files freely available online, in a way that's easy for others to modify, I hope to encourage people to make and modify them. In particular, I'd love to see changes or additions that I didn't think about and to have those changes shared publicly for others to use or continue to modify. The speakers have been designed to be relatively simple and cheap in the hopes of facilitating their production by others.</p>
        </div>
        <div>sp</div>
        <p>The speakers aren't yet available as a kit, but you can download the files and make them for yourself.</p>
        <div>Use 6mm (1/4") plywood. For the veneer, 1 9/16" edging backed with an iron-on adhesive is ideal (like this one from Rockler), but anything should work if you cut it to that width. Pick whatever fabric you like. For the electronic components, see the bill-of-materials above. You'll also need two-conductor speaker wire, available at Radio Shack.</div>
        <select>
        <option>opt_a</option>
        <option>opt_b</option>
        <option>opt_c</option>
        </select>
    </body>
    </html>
    '''
    extractor = ContentExtractor(document)
    print extractor.guessed_title(), "\n"
    print extractor.guessed_content(), "\n"
    print extractor.summarize(), "\n"
    print extractor.summary(), "\n"
    print extract(document), "\n"
    

if __name__ == '__main__': main()