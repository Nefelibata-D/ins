from django.http import JsonResponse
from .models import *
from .patch import *
from datetime import datetime


def download(request):
    if request.method == 'GET':
        url = request.GET.get('url', '')
        url_shortcode = '/p/' + url.split('/')[-2] + "/"
        query = ShortPath.objects.filter(shortcode=url_shortcode)
        if query:
            inf = {}  # 判断是否重复提交，直接返回链接
            for i in query:
                name = i.name
                link = i.download_url
                inf[name] = link
            data = {
                'shorturl': url_shortcode,
                'inf': inf,
                'status': 'success',
                'massage': ''
            }
        else:  # 不是重复链接，存入数据库
            inf = download_single(url=url)
            print(inf)
            if inf['status'] == 'success':  # 判断是否是有效网页
                for key, value in inf['inf_return'].items():
                    inf_dict = {
                        'name': key,
                        'download_url': value,
                        'file_path': key,
                        'shortcode': url_shortcode,
                        'time': datetime.now().replace(microsecond=0)
                    }
                    ShortPath.objects.create(**inf_dict)
                data = {
                    'shorturl': url_shortcode,
                    'inf': inf['inf_return'],
                    'status': 'success',
                    'massage': ''
                }
            else:  # 无效网页返回错误链接
                data = {
                    'shorturl': '',
                    'inf': '',
                    'status': 'failed',
                    'massage': '未找到页面，请检查链接是否正确'
                }
        return JsonResponse(data)
