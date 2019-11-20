from bs4 import BeautifulSoup
import requests
import re
import time

url_main = 'https://bj.58.com/pbdn/0/'
lists = []

#从主页面获取所有商品的链接，同时用who_sells判断是普通个人商品还是商家商品
#没有排除广告信息
def get_links_from(who_sells=0):
    urls = []
    list_view = 'https://bj.58.com/pbdn/{}/'.format(str(who_sells))
    wb_data = requests.get(list_view)
    soup = BeautifulSoup(wb_data.text,'lxml')
    for link in soup.select('td.t a.t.ac_linkurl'):
        urls.append(link.get('href').split('?')[0])
    print(urls)
    # return urls


#获取浏览量  !!!!!!!!!!!!!现在此方法暂时不行，返回值还是0
def get_view_info(url):
    id = url.split('/')[-1].strip('x.shtml')
    api = 'https://jst1.58.com/counter?infoid={}'.format(id)
    js = requests.get(api)
    views = js.text.split('=')[-1]
    # return views
    print(id)



#自己写的
#-----------------------------------------------------------------------------------------------

#从主界面获取所有链接
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
    commodity_data = requests.get(com_url)
    soup = BeautifulSoup(commodity_data.text,'lxml')
    # print(soup)

    title = soup.select('h1.detail-title__name')
    times = soup.select('div.detail-title__info__text')
    pageviews = soup.select('p.uv')
    price = soup.select('span.infocard__container__item__main__text--price')
    place = soup.select('div.infocard__container__item__main > a')
    print(pageviews)

    prices = re.sub("\D", "", price[0].get_text())
    prices += '元'
    titles = title[0].get_text().strip('\r\n ')#删除标题中的空格换行符
    data = {
        'title':titles,
        'time':times[0].get_text(),
        'pageviews':pageviews[0].get_text(),
        'price':prices,
        'place':place[0].get_text()
    }
    write_text(data)#将所爬取的数据写入当地文本中
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
# get_links_from(0)
