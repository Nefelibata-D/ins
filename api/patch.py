import requests
from bs4 import BeautifulSoup
import json

# noinspection PyRedundantParentheses
detail_query_hash = '003056d32c2554def87228bc3fd9668a'  # ins中获取详细内容的hash值，目前来看是固定的
user_query_hash = '6ff3f5c474a240353993056428fb851e'  # ins中获取发布者相关信息的hash值
my_query_hash = 'b1245d9d251dff47d91080fbdd6b274a'  # ins中获取请求人相关信息的hash值
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/90.0.4430.19 Safari/537.36 Edg/90.0.818.6',
    'Cookie': 'mid=YY-tfAALAAFkUdUyjbGilIWtsFJR; '
              'ig_did=C852CB39-24F1-4815-B28F-02E3E8B61438; '
              'ds_user_id=46117876343; '
              'sessionid=46117876343%3AW6YVS7fVeZhHtp%3A3; '
    # session id为有效cookies
}


def judge(url):
    url_shortcode = '/p/' + url.split('/')[-2] + "/',"  # 获取shortcode
    res = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    for i in soup.find_all('script', type='text/javascript'):
        if 'window.__additionalDataLoaded(' in str(i):  # 'window.__additionalDataLoaded('精确定位到所需数据
            information = \
                str(i).split('>')[1].split('window.__additionalDataLoaded(')[1].split(');</script')[0].split(
                    url_shortcode)[1]  # 处理数据
            information_json = json.loads(information)  # 将处理数据转换成json格式
            is_video = information_json['graphql']['shortcode_media']['is_video']
            if is_video:
                return {'is_video': True, 'information': information_json, 'shortcode': url.split('/')[-2]}
            else:
                return {'is_video': False, 'information': information_json, 'shortcode': url.split('/')[-2]}

    return False  # 若为空链接，则无法找到 'window.__additionalDataLoaded(' 函数直接返回None


# noinspection DuplicatedCode
def single_image(deal):
    inf_return = {}
    try:  # 有多个下载图片链接
        images = deal['information']['graphql']['shortcode_media']['edge_sidecar_to_children']['edges']
        times = 0
        for i in images:
            times += 1
            url = i['node']['display_url']
            res = requests.get(url=url, headers=headers)
            items = create_return_inf(deal, '.jpg', times)
            inf_return[items[0]] = items[1]
            with open('media/' + items[0], 'wb') as file:
                file.write(res.content)
    except KeyError:  # 只有一个下载链接
        image_url = deal['information']['graphql']['shortcode_media']['display_url']
        res = requests.get(url=image_url, headers=headers)
        items = create_return_inf(deal, '.jpg')
        inf_return[items[0]] = items[1]
        with open('media/' + items[0], 'wb') as file:
            file.write(res.content)

    return {'inf_return': inf_return, 'status': 'success'}


def single_video(deal):
    inf_return = {}
    video_url = deal['information']['graphql']['shortcode_media']['video_url']  # 视频必然只有一个
    res = requests.get(url=video_url, headers=headers)
    items = create_return_inf(deal, '.mp4')
    inf_return[items[0]] = items[1]
    with open('media/' + items[0], 'wb') as file:
        file.write(res.content)

    return {'inf_return': inf_return, 'status': 'success'}


def download_single(url):
    deal = judge(url)
    if deal:
        if deal['is_video']:
            inf = single_video(deal)  # 下载视频
        else:
            inf = single_image(deal)  # 下载图片
    else:
        inf = {'inf_return': '',
               'status': 'failed', }
    return inf


def create_return_inf(deal, filetype, times=0):
    name = deal['shortcode'] + '_' + str(times) + filetype
    link = 'media/' + name

    return name, link
