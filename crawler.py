from urllib import request, parse
from bs4 import BeautifulSoup
import datetime

base_url = 'https://fullfact.org'

today = datetime.date.today() + datetime.timedelta(days=-2)
print(today)

# today = datetime.datetime.strptime('2016-12-21','%Y-%m-%d').date() # test date

def soup_data(url):
    return BeautifulSoup(request.urlopen(url), 'html.parser')

def soup_dict(soup):
    quote = []
    author = ''
    date = ''
    link = ''
    list = soup.children
    for i in list:
        if i.find('a') != -1 and i.find('a'):
            author, date = i.text.rsplit(', ',1)
            link = i.find('a')
            link = link['href']
        elif i.find('p') != -1:
            quote.append(i.text)

    dict = {'quote': ' '.join(quote), 'author': author.replace('\xa0', ''), 'link': link, 'quote_date': date}
    return dict

def get_quotes(url):
    soup = soup_data(url)
    soup = soup.find_all('blockquote')
    if len(soup) == 1:
        dict = soup_dict(soup[0])
        print(dict)
    elif len(soup) > 1:
        for element in soup:
            dict = soup_dict(element)
            print(dict)
    else:
        print('No quotes returned')

if __name__ == '__main__':
    soup = soup_data(base_url)
    soup = soup.find(id='mostRecent').find_all('li')
    for article in soup:
        article_date = article.find('small').text
        article_date = datetime.datetime.strptime(article_date, "%d %b %Y").date()
        if article_date == today:
            url = article.find('a')
            url = parse.urljoin(base_url, url['href'])
            print(url)
            get_quotes(url)