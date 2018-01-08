
import urllib
from bs4 import BeautifulSoup

def text_from_url(url):

    settings = {
            'targets':['style'] # 'script','style'
                }

    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html,'html.parser')
    text = ''

    # kill all script and style elements
    for script in soup(settings['targets']):
            script.extract()    # rip it out

            # get text
            text = soup.get_text()

            # break into lines and remove leading and trailing space on each
            lines = (line.strip() for line in text.splitlines())
            # break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            # drop blank lines
            text += '\n'.join(chunk for chunk in chunks if chunk)

    return filter(None,(text.encode('ascii','replace')).replace('?','').split('\n'))


def bookend_list(lst,start,end):

    s1 = lst.index(start)+1
    s2 = lst[s1:].index(end)
    return lst[s1:s1+s2-1]
