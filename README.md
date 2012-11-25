Summary
=======

This is a python module to extract title, main text and images from the web page. This module is simple and easy to use.

## Usage

Here is how you get summary from the web page.

```
uri = 'web page you want to extract main text.'
res = extract(urllib.urlopen(uri).read())
print res['title'], '\n' # header of main content
print res['body'], '\n' # main content
print res['img'], '\n' # candidates of main images
```

In addition, you are able to override `is_collection_of_links()` and `not_body_rate()`, which are methods of extractor module, 
in response to your necessary. `is_collection_of_links()` decides whether layout block is a collection of links.

```
def is_collection_of_links(block):
    # whether this layout block is a collection of links.
    return False
```

`not_body_rate()` decides the rate which means that layout block is not body.

```
def not_body_rate(block):
    # not_body_rate() takes account of not_body_rate.
    # return value has to be float or integer.
    return 0
```

## Notes

### Copyright of the original implementation

Copyright © 2007/2008 Nakatani Shuyo / Cybozu Labs Inc. All rights reserved.

<ul>
    <li><a href="http://labs.cybozu.co.jp/blog/nakatani/2007/09/web_1.html">labs.cybozu.co.jp/blog/nakatani/2007/09/web_1.html</a></li>
</ul>