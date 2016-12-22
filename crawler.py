from urllib import request
from bs4 import BeautifulSoup

url = 'https://fullfact.org/economy/are-driver-only-trains-safe/'

data = request.urlopen(url)
soup = BeautifulSoup(data, 'html.parser')

soup = soup.find_all('blockquote')

for element in soup:
    quote = []
    author = ''
    date = ''
    link = ''
    list = element.children
    for i in list:
        if i.find('a') != -1 and i.find('a'):
            author, date = i.text.split(',')
            link = i.find('a')
            link = link['href']
        elif i.find('p') != -1:
            quote.append(i.text)

    dict = {'quote': ' '.join(quote), 'author': author.replace('\xa0',''), 'link': link, 'date': date}
    print(dict)