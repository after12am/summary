
import lxml, chardet

class DetectEncodeException(Exception):
    pass

REGX_CHARSET = r"charset=(?P<charset>[a-zA-Z0-9-]+)"

def _detect_from_html(self, text):
	root = lxml.html.fromstring(text.lower())
	for meta in root.xpath("//meta[@charset]"):
		encoding = meta.get("charset")
		if encoding:
			break
	else:
		for meta in root.xpath("//meta[@http-equiv='content-type']"):
			encoding = meta.get("charset")
			if encoding:
				break
			content = meta.get("content")
			if content:
				charset = re.compile(REGX_CHARSET).findall(content)
				if charset and len(charset):
					encoding = charset[0].strip()
					break
	return encoding

def detect_encoding(self, text):
	try:
	    # as we supposed text as html string
		encoding = _detect_from_html(text)
	except:
	    pass
	if not encoding: 
	    # as we supposed text as string
	    encoding = chardet.detect(text)['encoding']
	return encoding

def	force_unicode(text):
	try:
		result = unicode(text, 'utf-8', 'replace')
	except:
		encoding = detect_encoding(text)
		if encoding:
		    result = unicode(text, encoding, 'replace')
		else:
		    raise DetectEncodeException('Unknown charset')
	return result
