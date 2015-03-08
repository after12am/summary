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
        self.text1 = '''
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
        
        self.text2 = '''
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
        
        self.text3 = '''
        Not HTML document
        '''
        
        self.text4 = '''
        <!DOCTYPE HTML>
        <html lang="en">
        <head>
        <title></title>
        </head>
        <body>
        </body>
        </html>
        '''
    
    def test_detect_text_1(self):
        encoding = detect_charset(self.text1)
        self.assertEqual(encoding, 'utf-8')
    
    def test_detect_text_2(self):
        encoding = detect_charset(self.text2)
        self.assertEqual(encoding, 'utf-8')
    
    def test_detect_text_3(self):
        encoding = detect_charset(self.text3)
        self.assertEqual(encoding, None)
    
    def test_detect_text_4_case_1(self):
        encoding = detect_charset(self.text4)
        self.assertEqual(encoding, None)
    
    def test_detect_text_4_case_2(self):
        encoding = detect_encoding(self.text4)
        self.assertEqual(encoding, 'ascii')
