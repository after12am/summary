import unittest
from summary.char import *

class TestDecodeEntities(unittest.TestCase):
    
    def setUp(self):
        self.entities = 'A &#039;quote&#039; is &lt;b&gt;bold&lt;/b&gt;'

    def test_decode_entities(self):
        decoded = decode_entities(self.entities)
        self.assertEqual(decoded, "A 'quote' is <b>bold</b>")

encoding_located_in_charset = '''
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

encoding_located_in_content = '''
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

encoding_text_format = '''
Not HTML document
'''

encoding_not_specified = '''
<!DOCTYPE HTML>
<html lang="en">
<head>
<title></title>
</head>
<body>
</body>
</html>
'''

class TestDetectEncoding(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def test_html_charset_encoding_detection(self):
        encoding = detect_charset(encoding_located_in_charset)
        assert encoding == 'utf-8'
    
    def test_html_content_encoding_detection(self):
        encoding = detect_charset_in_content(encoding_located_in_content)
        assert encoding == 'utf-8'
    
    def test_text_format_encoding_detection(self):
        encoding = detect_charset(encoding_text_format)
        assert encoding is None
    
    def test_html_not_specified_encoding_detection_pat_1(self):
        encoding = detect_charset(encoding_not_specified)
        assert encoding is None
    
    def test_html_not_specified_encoding_detection_pat_2(self):
        encoding = detect_encoding(encoding_not_specified)
        assert encoding == 'ascii'
