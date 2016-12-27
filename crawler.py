from urllib import request, parse
from bs4 import BeautifulSoup
import datetime

base_url = 'https://fullfact.org'

today = datetime.date.today() + datetime.timedelta(days=-12)
print(today)

def soup_data(url):
    return BeautifulSoup(request.urlopen(url), 'html.parser')

def get_quotes(url):
    dicts = []

    def soup_dict(soup):
        quote = []
        author = ''
        date = ''
        link = ''
        list = soup.children
        for i in list:
            if i.find('a') != -1 and i.find('a'):
                author, date = i.text.rsplit(', ', 1)
                link = i.find('a')
                link = link['href']
            elif i.find('p') != -1:
                quote.append(i.text)

        dict = {'quote': ' '.join(quote).replace('\xa0',''), 'author': author.replace('\xa0', ''), 'link': link, 'quote_date': date}
        return dict

    soup = soup_data(url)
    soup = soup.find_all('blockquote')
    if len(soup) == 1:
        dicts.append(soup_dict(soup[0]))
    elif len(soup) > 1:
        for element in soup:
            dicts.append(soup_dict(element))
    else:
        print('No quotes returned')

    return dicts

def get_claim(url):
    claims = []
    soup = soup_data(url)
    soup = soup.find_all('div', {'class': 'col-xs-12 col-sm-6 col-left'})
    [claims.append(i.find('p').string) for i in soup]

    return claims

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
            claims = get_claim(url)
            [print(claim) for claim in claims]
            dicts = get_quotes(url)
            [print(dict) for dict in dicts]
            print()