# -*- coding: utf-8 -*-
import scrapy
import json
from QQ_Music.items import QqMusicItem



class MusicCategoryListSpider(scrapy.Spider):
    name = "Music_Category_list"
    # allowed_domains = ["www"]
    start_urls = ['https://c.y.qq.com/splcloud/fcgi-bin/fcg_get_diss_tag_conf.fcg?g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0']

    def parse(self, response):
        # 分类歌单下json信息
        category_josn = json.loads(response.text)
        # 分组歌单
        category_list = category_josn['data']['categories']
        # 循环取出分组歌单名字以及歌单下分类名字和ID与根据最新与最热和默认及其他sortid，但是分析发现sortID是从2(最新排序)开始的，以下3(最热)4(评分)5(默认)返回的json文件是相同的，所以在这里只取了2和3
        for cate in category_list:
            category_group_name = cate['categoryGroupName']
            for i in cate['items']:
                category_name = i['categoryName']
                category_id = i['categoryId']
                # 利用循环的方式拼接一个分类下的最新与最热的url进行下面的解析
                for sortid in range(2,4):
                    category_url = 'https://c.y.qq.com/splcloud/fcgi-bin/fcg_get_diss_by_tag.fcg?picmid=1&rnd=0.2473376608007709&g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0&categoryId={}&sortId={}&sin=0&ein=100000'.format(category_id,sortid)
                    yield scrapy.Request(category_url,self.category_parse,meta={
                        'category_group_name':category_group_name,
                        'category_name':category_name,
                        'category_id':category_id,
                        'sortid':str(sortid)
                    })

    def category_parse(self,response):
        # 接收上级解析出的，分组名字，分类名，分类id以及分类排序（最新，最热）
        category_group_name = response.meta['category_group_name']
        category_name = response.meta['category_name']
        category_id = response.meta['category_id']
        if response.meta['sortid'] == '2':
            sort = '最新_new'
        else:
            sort = '最热_hot'
        print(category_group_name,category_name,sort)
        # 分类下data信息
        category_json_data = json.loads(response.text)
        category_data = category_json_data['data']

        # 解析歌单详情需要传递的参数有disstid
        for category_list in category_data['list']:
            category_disstid = category_list['dissid']
            headers = {
                'referer': 'https://y.qq.com/n/yqq/playsquare/{}.html'.format(category_disstid),
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
            }
            # 分类详情url拼接
            cate_detail_url = 'https://c.y.qq.com/qzone/fcg-bin/fcg_ucc_getcdinfo_byids_cp.fcg?type=1&json=1&utf8=1&onlysong=0&disstid={}&g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0'.format(category_disstid)
            yield scrapy.Request(cate_detail_url,self.cate_detail_parse,meta={
                'category_group_name':category_group_name,
                'category_name':category_name,
                'category_id':category_id,
                'category_sort':sort,
                'category_data':category_data
            },headers=headers)
    def cate_detail_parse(self,response):
        cate_detail_json = json.loads(response.text)

        category_group_name = response.meta['category_group_name']
        category_name = response.meta['category_name']
        category_id = response.meta['category_id']
        category_sort = response.meta['category_sort']
        category_data = response.meta['category_data']
        cd_list = cate_detail_json['cdlist']

        item = QqMusicItem()
        item['category_group_name'] = category_group_name
        item['category_name'] = category_name
        item['category_id'] = category_id
        item['category_sort'] = category_sort
        item['category_data'] = category_data
        item['cd_list'] = cd_list

        yield item