import scrapy

from bs4 import BeautifulSoup
import requests
import json, io, sys, re
import pymongo

from multiprocessing import Process
from multiprocessing.pool import ThreadPool
import multiprocessing


from pdd.items import GetGoodsItem, GetCategoryItem


class PddSpider(scrapy.Spider):
    name = "pdd2"

    def __init__(self, input_szie = None, first= None, last=None):
        self.input_szie = input_szie  # source file name
        self.first = first
        self.last = last



    def start_requests(self):

        #category_ids = [140,]

        size = self.input_szie
        first = self.first
        last = self.last
        for category_id in range(first,last):
        #for category_id in category_ids:
            for good_type in range(30):
                #good_ids = self.get_goods_id_from_category(category_id, good_type, 1000)
                request_url_category = 'http://apiv4.yangkeduo.com/operation/' + str(category_id) + '/groups?opt_type=' + str(good_type) + '&offset=0&size=' + str(size) + '&pdduid='
                yield scrapy.Request(url=request_url_category, callback=self.parse, meta={'category_id': category_id},)


        # goods_id_all = [628563806, 53564917]
        #
        #
        # for goods_id in goods_id_all:
        #     url = 'http://apiv2.yangkeduo.com/api/oak/v6/goods/'+ str(goods_id)+ '?goods_id=' + str(goods_id) + '&pdduid='
        #
        #     yield scrapy.Request(url=url, callback=self.parse_goods, meta={'goods_id': goods_id},)


    def parse(self, response):
        #page = response.url.split("/")[-2]

        json_doc = json.loads(response.body_as_unicode())
        category_id = response.meta['category_id']

        goods_list = json_doc['goods_list']
        for goods in goods_list:
            goods_id = goods['goods_id']
            url = 'http://apiv2.yangkeduo.com/api/oak/v6/goods/'+ str(goods_id)+ '?goods_id=' + str(goods_id) + '&pdduid='


            yield scrapy.Request(url=url, callback=self.parse_goods, meta={'goods_id': goods_id},)


        item = GetCategoryItem()
        item['category_id'] = category_id
        item['category_json_doc'] = json_doc

        # insertDB(collection_good, goods_id, json_doc)
        # self.log('Saved file %s' % goods_id)

        yield item

    def parse_goods(self, response):
        #page = response.url.split("/")[-2]

        goods_json_doc = json.loads(response.body_as_unicode())
        goods_id = response.meta['goods_id']

        #item = {'goods_id':goods_id, 'json_doc':json_doc}


        item = GetGoodsItem()
        item['goods_id'] = goods_id
        item['goods_json_doc'] = goods_json_doc


        yield item
