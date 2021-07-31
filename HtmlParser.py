import urllib.request


class HtmlParser:
    def __init__(self, url):
        fp = urllib.request.urlopen(url)
        self.htmlText = fp.read().decode("utf8")
        fp.close()

    def print(self):
        print(self.htmlText)
