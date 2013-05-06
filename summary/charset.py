import re, chardet, htmlentitydefs
import lxml.html

class UnknownEncodingException(Exception):
    def __init__(self):
        Exception.__init__(self, 'Unknown encoding')

def encoding_if_html(text):
    REGX_CHARSET = r"charset=(?P<charset>[a-zA-Z0-9-_]+)"
    root = lxml.html.fromstring(text.lower())
    for meta in root.xpath("//meta[@charset]"):
        encoding = meta.get("charset")
        if encoding:
            return encoding
    for meta in root.xpath("//meta[@content]"):
        content = meta.get("content")
        if content:
            encoding = re.compile(REGX_CHARSET).findall(content)
            if encoding:
                return encoding[0].strip()
    raise UnknownEncodingException()

def encoding_if_text(text):
    # as we suppose text as html string
    try:
        encoding = encoding_if_html(text)
    except:
        encoding = chardet.detect(text)['encoding']
    return encoding

def to_unicode(text):
    unicoded, encoding = None, encoding_if_text(text)
    if encoding:
        unicoded = unicode(text, encoding, 'replace')
    return unicoded

def to_unicode_if_htmlentity(text):
    REFERENCE_REGEX = re.compile(u'&(#x?[0-9a-f]+|[a-z]+);', re.IGNORECASE)
    NUM16_REGEX = re.compile(u'#x\d+', re.IGNORECASE)
    NUM10_REGEX = re.compile(u'#\d+', re.IGNORECASE)
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

def main():
    text = '''
    <!DOCTYPE HTML>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <title></title>
    </head>
    <body>
    </body>
    </html>
    '''
    print encoding_if_html(text)
    
    text = '''
    <!DOCTYPE HTML>
    <html lang="en">
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title></title>
    </head>
    <body>
    </body>
    </html>
    '''
    print encoding_if_html(text)
    
    text = '''
    <!DOCTYPE HTML>
    <html lang="en">
    <head>
    <title></title>
    </head>
    <body>
    </body>
    </html>
    '''
    print encoding_if_text(text)

if __name__ == '__main__': main()