from html.parser import HTMLParser
from urllib.request import urlopen
from urllib import parse

class LinkParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (key, value) in attrs:
                if key == 'href':

                    newurl = parse.urljoin(self.baseUrl, value)
                    self.links += [newurl]

    def getLinks(self, url):
        self.links = []
        self.baseUrl = url

        response = urlopen(url)

        if response.getheader('Content-Type') == 'text/html':
            htmlBytes = response.read()
            htmlString = htmlBytes.decode("utf-8")
            self.feed(htmlString)

            return htmlString, self.links
        else:
            return '',[]

def findword(url, word, maxPages):
    pagestovisit = [url]
    numberVisited = 0
    found = False

    while numberVisited < maxPages and pagestovisit != [] and not found:
        numberVisited += 1
        url = pagestovisit[0]
        pagestovisit = pagestovisit[1:]

        try:
            print("{0} Visiting {1}".format(numberVisited, url))
            parser = LinkParser()
            data, links = parser.getLinks(url)
            if data.find(word) > -1:
                found = True
            pagestovisit += links
            print("Sucess")

        except:
            print("Failure")
    if found == True:
        print("The word {0} was found at {1}".format(word, url))
    else:
        print("word not found")
