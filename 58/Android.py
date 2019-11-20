from bs4 import BeautifulSoup
import requests
import re
import time

#模拟手机端操作
headers = {
    'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
}

url='https://bj.58.com/pingbandiannao/39890473714957x.shtml?link_abtest=&amp;psid=135650812206337799810192883&amp;entinfo=39890473714957_p&amp;slot=-1'

url_main = 'https://bj.58.com/pbdn/0/'
lists = []
def main_url(url):
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text, 'lxml')

    links = soup.select('a.t.ac_linkurl')
    # data = {}
    for link in links:
        link_sel = link.get('href')
        # print(link_sel.split('/')[2])
        if link_sel.split('/')[2] != 'jumpzhineng.58.com':
            data = {
                'link': link_sel
            }
            lists.append(data)

    print(len(lists))
    print(lists)


def deal_url(com_url):
    time.sleep(2)
    commodity_data = requests.get(com_url,headers=headers)
    soup = BeautifulSoup(commodity_data.text,'lxml')
    # print(soup)

    title = soup.select('h1.titleArea-title')
    times = soup.select('p.time')
    pageviews = soup.select('p.uv')
    price = soup.select('div.titleArea-price')
    place = soup.select('a.icon-location.icon')
    # print(pageviews)

    prices = re.sub("\D", "", price[0].get_text())
    prices += '元'
    titles = title[0].get_text().strip('\r\n ')#删除标题中的空格换行符
    data = {
        'title':titles,
        'time':times[0].get_text(),
        'pageviews':pageviews[0].get_text(),
        'price':prices,
        'place':place[0].get_text().strip('\r\n ')
    }
    # write_text(data)
    print(data)

def write_text(data):
    f = open("commodity.txt", 'a')
    f.write(str(data)+'\n')
    f.close()

main_url(url_main)
for list in lists:
    deal_url(list['link'])

# url='https://bj.58.com/pingbandiannao/39890473714957x.shtml?link_abtest=&amp;psid=135650812206337799810192883&amp;entinfo=39890473714957_p&amp;slot=-1'
# deal_url(url)