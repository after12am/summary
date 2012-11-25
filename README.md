Summary
========

Summary is a python script to extract main content from the web page. This script is simple to use and provides easy way to pick up candidate of main text and image from body in html document. All you have to do is only one thing.

## Usage

Here shows you to get summary from the web page.

```
uri = 'web page you want to extract main text.'
res = extract(urllib.urlopen(uri).read())
print res['title'], '\n'
print res['body'], '\n' # main content
print res['img'], '\n' # candidates of main image
```

Also, you can override extractor's methods in response to your necessary. Here is a method that decides whether layout block is a collection of links.

```
def is_collection_of_links(block):
    # whether this layout block is a collection of links.
    return False
```

A method that takes account of not_body_rate.

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