<h1>Summary</h1>

Summary is a python script to extract main content from the web page. This script is simple to use and provides easy way to pick up candidate of main text and image from body in html document. All you have to do is only to call 1 line Summary provides.

## Usage

For getting main text, execute following lines.

```
uri = 'web page you want to extract main text.'
print extract(urllib.urlopen(uri).read())['body'], '\n'
```

For getting main image, execute following lines.

```
uri = 'web page you want to extract main image.'
print extract_img(urllib.urlopen(uri).read()), '\n'
```

## Notes

### Copyright of the original implementation

Copyright © 2007/2008 Nakatani Shuyo / Cybozu Labs Inc. All rights reserved.

<ul>
    <li><a href="http://labs.cybozu.co.jp/blog/nakatani/2007/09/web_1.html">labs.cybozu.co.jp/blog/nakatani/2007/09/web_1.html</a></li>
</ul>