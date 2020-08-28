import requests
import lxml.etree
import re
from multiprocessing.dummy import Pool
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
}
# 线程池--------------------------------------------------------------------------------------------------------------------------------------------
url = 'https://www.pearvideo.com/category_4'
res = requests.get(url,headers=headers).text
soul = lxml.etree.HTML(res)
items = soul.xpath('//ul[@id = "listvideoListUl"]/li')
url_list = []
for item in items:
    link = 'https://www.pearvideo.com/'+item.xpath('./div/a/@href')[0]
    linkname = item.xpath('./div/a/div[2]/text()')[0]
    print(link,linkname)
    detail_url_res = requests.get(url=link,headers=headers).text
    redu = 'srcUrl="(.*?)",vdoUrl'
    video_url = re.findall(redu,detail_url_res)[0]
    print(video_url)
    dict = {
        'name':linkname,
        'link':video_url
    }
    url_list.append(dict)
def get_data(dict):
    url = dict['link']
    print('{}正在下载'.format(dict['name']))
    response = requests.get(url,headers=headers).content
    # baocun
    with open('./{}.mp4'.format(dict['name']),'wb') as f:
        f.write(response)
        print('{}下载成功'.format(dict['name']))
pool = Pool(4)
pool.map(get_data,url_list)
pool.close()
pool.join()