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

1. Download [Scrapy](https://scrapy.org/)
1. `cd src/crawler`
1. run `scrapy crawl questions-bfs`

This will start the simple breadth first search spider module responsible for downloading all pages in the specified domain. You can see them on the fly in `src/crawler/documents` folder.
