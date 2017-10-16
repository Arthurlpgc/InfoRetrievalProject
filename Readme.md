## Websites included

The crawler will be retrieving information from the following online judges:

* [Codeforces](http://codeforces.com/)
* [CodeChef](https://www.codechef.com/)
* [URI Online Judge](https://www.urionlinejudge.com.br/)
* [Sphere Online Judge](http://www.spoj.com/)
* [DMOJ](https://dmoj.ca/)
* [A² Online Judge](https://a2oj.com/)
* [AtCoder](https://atcoder.jp/)
* [CS Academy](https://csacademy.com/)
* [Timus Online Judge](http://acm.timus.ru/)
* [Caribbean Online Judge](http://coj.uci.cu)

## Running Crawler

In order to run your crawler, follow these steps:

* First, make sure you have [Python 3.6](https://www.python.org/) and [pip](https://pip.pypa.io/en/stable/installing/) installed in your system. Then:

1. Go to src folder: `cd src`
1. Install project requirements: `pip install -r requirements.txt`
1. Run the crawler: `scrapy runspider crawler/questions.py`

This will start a breadth first search based on some heurístic spider module responsible for downloading all pages in the specified domain. You can see them on the fly in `src/retrieved/documents` and `src/retrieved/objects` folder.
