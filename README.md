Summary
=======

Summary is a python module to extract main content from the web page. 
This was originally implemented by Nakatani Shuyo with ruby. 
His strategy and implementation about extraction is great. But there is room for improvement. 
The extracted content includes the garbages, e.g. comments of blog entry. 
I improved not to extract those as increasing of precision of calculating Layout Block, upon implementing with python. 
And also Summary extracts not only main content but also appropriate title, even if being broken page.


## strategy

```
1. removes the unnecessary elements from the web page.
2. divides block elements into layout blocks and empty blocks.
3. scores the those blocks.
4. clusters the high score blocks that are next each others.
5. scores the clusters.
6. high score cluster is what we have been seeking. 
```

## Install

I prepare easy install way. Run the following command in your new terminal.

```
sudo easy_install summary
```

## Prepare

Run the following and download `punkt` package and `stopwords` corpora.

```
$ python
>>> import nltk
>>> nltk.download() 
```

## Usage

Here is how you get summary from the web page.

```
from summary import extract
uri = 'web page you want to extract main text.'
res = extract(urllib.urlopen(uri).read())
print res['title'], '\n' # guessed title of main content
print res['body'], '\n' # guessed main content
print res['digest'], '\n' # guessed summarization
print res['img'], '\n' # candidate of main images
```

Here shows the way to override the noise filters of extractor module. Use these overriding in response to your necessary. 
The noise filters are `is_collection_of_links()` and `not_body_rate()`. 
`is_collection_of_links()` decides whether layout block is a collection of links.

```
# /path/to/any.py
# include `is_collection_of_links()` for overriding
from summary import extractor

def my_is_collection_of_links(block):
    # whether this layout block is a collection of links.
    print block
    return False

extractor.is_collection_of_links = my_is_collection_of_links
```

`not_body_rate()` decides the rate which means given layout block is not body.

```
# /path/to/any.py
# include `not_body_rate()` for overriding
from summary import extractor

def my_not_body_rate(block):
    # not_body_rate() takes account of not_body_rate.
    # return value has to be float or integer.
    print block
    return 0

extractor.not_body_rate = my_not_body_rate
```

## Notes

### Copyright of the original implementation

Copyright © 2007/2008 Nakatani Shuyo / Cybozu Labs Inc. All rights reserved.

* [labs.cybozu.co.jp/blog/nakatani/2007/09/web_1.html](http://labs.cybozu.co.jp/blog/nakatani/2007/09/web_1.html)

## License

Copyright (c) 2012-2015 Satoshi Okami. See the LICENSE file for license rights and limitations (MIT).
