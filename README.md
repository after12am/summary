Summary
=======

Summary is a python module to extract main content from the web page. 
This script was originally implemented by Nakatani Shuyo with ruby. 
But his script extracts text including garbage, as a example, comments of blog entry. 
So I improved not to extract that garbage as increasing of precision of 
calculating Layout Block, upon implementing this with python. 
In addition, I added function to extract specious and appropriate title, 
even if being not a standard coding about html document. 
Summary is useful, and its usage is so simple that you call 1 api. 
Now, let's dive into web.

## Usage

Here is how you get summary from the web page.

```
from summary import extract
uri = 'web page you want to extract main text.'
res = extract(urllib.urlopen(uri).read())
print res['title'], '\n' # header of main content
print res['body'], '\n' # main content
print res['img'], '\n' # candidates of main images
```

In addition, you are able to override `is_collection_of_links()` and 
`not_body_rate()`, which are methods of extractor module, in response to your necessary. 
`is_collection_of_links()` decides whether layout block is a collection of links.

```
# /path/to/any.py
# include `is_collection_of_links()` for overriding
from summary import extractor

def _is_collection_of_links(block):
    # whether this layout block is a collection of links.
    print block
    return False

extractor.is_collection_of_links = _is_collection_of_links
```

`not_body_rate()` decides the rate which means that layout block is not body.

```
# /path/to/any.py
# include `not_body_rate()` for overriding
from summary import extractor

def _not_body_rate(block):
    # not_body_rate() takes account of not_body_rate.
    # return value has to be float or integer.
    print block
    return 0

extractor.not_body_rate = _not_body_rate
```

## Notes

### Copyright of the original implementation

Copyright © 2007/2008 Nakatani Shuyo / Cybozu Labs Inc. All rights reserved.

<ul>
    <li><a href="http://labs.cybozu.co.jp/blog/nakatani/2007/09/web_1.html">labs.cybozu.co.jp/blog/nakatani/2007/09/web_1.html</a></li>
</ul>