from bs4 import BeautifulSoup
import requests
import time
import os

url = 'https://weheartit.com/inspirations/taylorswift?scrolling=true&page='


def get_page(url,data=None):
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text,'lxml')
    imgs = soup.select('div.entry-preview.thumb-height > a > img')
    links = soup.select('div.entry-preview.thumb-height > a')

    if data==None:
        for img,link in zip(imgs,links):
            data = {
                'img': img.get('src'),
                'link': link.get('href')
            }
            srcs = data['img']
            print(srcs)
            path = './Swift/' + srcs.split('/')[-2] +'.jpg'
            # print(path)
            try:
                if not os.path.exists(path):
                    r = requests.get(srcs)
                    r.raise_for_status()
                    with open(path,'wb') as f:
                        f.write(r.content)
                        f.close()
                        print('图片保存成功')
                else:
                    print('图片已存在')
            except:
                print('图片保存失败')

def get_more_pages(start,end):
    for one in range(start,end):
        get_page(url+str(one))
        time.sleep(2)

get_more_pages(1,2)