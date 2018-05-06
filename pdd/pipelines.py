# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings
import pymongo, datetime

from pdd.items import GetGoodsItem, GetCategoryItem



class PddPipeline(object):
    def process_item(self, item, spider):
        return item



class MongoDBPipeline(object):

     # 连接数据库
    def __init__(self):

        # 获取数据库连接信息
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbname = settings['MONGODB_DBNAME']
        client = pymongo.MongoClient(host=host, port=port)

        # 定义数据库
        db = client[dbname]
        self.collection_goods = db[settings['MONGODB_TABLE']]
        self.collection_goods_sale = db['goods_sale']
        self.collection_sku_sale = db['sku_sale']
        self.collection_categroy = db['category']


    def insertDB(self, db_collection, doc):
        try:
            db_update_result = db_collection. insert_one(doc)

        except Exception as e:
            print("Unexpected error when updating database:", type(e), e)


    def insertDB_many(self, db_collection, doc):
        '''
        doc should be a list contains one or more dict.
        '''
        try:

            db_update_result = db_collection.insert_many(doc)

            return db_update_result


        except Exception as e:
            print("Unexpected error when updating database many:", type(e), e)


    def insertDB_with_id(self, db_collection, itemid, doc):
        try:
            doc_ = {}
            doc_.update({'_id': itemid})
            doc_.update(doc)
            db_update_result = db_collection. insert_one(doc_)


        except pymongo.errors.DuplicateKeyError:
            pass

        except Exception as e:
            print("Unexpected error when updating database:", type(e), e)


    def updateDB(self, db_collection, itemid, doc):
        try:
            db_update_result = db_collection.update({'_id': itemid}, doc, upsert=True)
            #return db_update_result['ok']

        except Exception as e:
            print("Unexpected error when updating database:", type(e), e)


    def get_goods_sales_from_orig(self, goods_doc_orig):
        goods_id = goods_doc_orig['goods_id']
        cat_id = goods_doc_orig['cat_id']
        mall_id = goods_doc_orig['mall_id']
        sales = goods_doc_orig['sales']
        cat_id_1 = goods_doc_orig['cat_id_1']

        return {'goods_id':goods_id, 'cat_id':cat_id,'mall_id':mall_id,'sales':sales,'cat_id_1':cat_id_1}



    def process_item(self, item, spider):


        date = datetime.datetime.utcnow()

        if isinstance(item, GetGoodsItem):


            # goods,only once, id is goods_id, will not update other information in future
            #
            doc_good = {'date': date}
            orig_doc_goods = item['goods_json_doc']
            doc_good.update(orig_doc_goods)

            self.insertDB_with_id(self.collection_goods , item['goods_id'],  doc_good)

            # update goods sale everyday
            #
            goods_doc_sale = {'date': date}
            if orig_doc_goods:

                goods_doc_everyday = self.get_goods_sales_from_orig(orig_doc_goods)
                goods_doc_sale.update(goods_doc_everyday)

                self.insertDB(self.collection_goods_sale, goods_doc_sale)




            # update sku sale everyday
            #
            if orig_doc_goods:
                sku_docs = []
                if 'sku' in orig_doc_goods:
                    skus = orig_doc_goods['sku']
                    for sku in skus:
                        sku_doc = {'date': date}
                        sku_doc.update(sku)
                        sku_docs.append(sku_doc)

                    self.insertDB_many(self.collection_sku_sale, sku_docs)


        elif isinstance(item, GetCategoryItem):
            doc_category = {'date': date}
            doc_category.update(item['category_json_doc'])

            self.updateDB(self.collection_categroy , item['category_id'], doc_category)

        return item
