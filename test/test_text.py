import unittest
from summary.text import *

class TestDecodeEntities(unittest.TestCase):
    
    def setUp(self):
        self.entities = 'A &#039;quote&#039; is &lt;b&gt;bold&lt;/b&gt;'

    def test_decode_entities(self):
        decoded = decode_entities(self.entities)
        self.assertEqual(decoded, "A 'quote' is <b>bold</b>")


class TestDetectEncoding(unittest.TestCase):
    
    def setUp(self):
        self.encoding_located_in_charset = '''
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
        self.encoding_located_in_content = '''
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
        self.not_html_document = '''
        Not HTML document
        '''
        self.no_specified_encoding = '''
        <!DOCTYPE HTML>
        <html lang="en">
        <head>
        <title></title>
        </head>
        <body>
        </body>
        </html>
        '''
    
    def test_encoding_located_in_charset(self):
        encoding = detect_charset(self.encoding_located_in_charset)
        self.assertEqual(encoding, 'utf-8')
    
    def test_encoding_located_in_content(self):
        encoding = detect_charset(self.encoding_located_in_content)
        self.assertEqual(encoding, 'utf-8')
    
    def test_text_3(self):
        encoding = detect_charset(self.text3)
        self.assertEqual(encoding, None)
    
    def test_not_html_document(self):
        encoding = detect_charset(self.not_html_document)
        self.assertEqual(encoding, None)
    
    def test_no_specified_encoding(self):
        encoding = detect_encoding(self.no_specified_encoding)
        self.assertEqual(encoding, 'ascii')
