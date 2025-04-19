import re
from typing import Any

import pymongo
import scrapy
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.http import Response
from scrapy.pipelines.images import ImagesPipeline
from scrapy.pipelines.media import MediaPipeline
import logging


class MongoDBPipeline(object):

    @classmethod
    def from_crawler(cls, crawler):
        cls.connection_string = crawler.settings.get('MONGODB_CONNECTION_STRING')
        cls.database = crawler.settings.get('MONGODB_DATABASE')
        cls.collection = crawler.settings.get('MONGODB_COLLECTION')
        return cls()

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.connection_string)
        self.db = self.client[self.database]

    def process_item(self, item, spider):
        self.db[self.collection].update_one({
            'name': item['name']
        }, {
            '$set': dict(item)
        }, True)
        return item

    def close_spider(self, spider):
        self.client.close()


class ImagePipeline(ImagesPipeline):
    def file_path(
            self,
            request: Request,
            response: Response | None = None,
            info: MediaPipeline.SpiderInfo | None = None,
            *,
            item: Any = None,
    ) -> str:
        movie = request.meta['movie']
        type = request.meta['type']
        name = request.meta['name']
        file_name = f'{movie}/{type}/{name}.jpg'
        # file_name = re.sub('/', '_', re.sub('[\s()]', '', file_name))
        image_name = file_name.replace(" ", "_").replace(":", "_")
        image_name = image_name.encode('utf-8').decode('utf-8')
        logging.warning(f'file_name：{image_name}')

        return image_name

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem(f'注意图片下载失败！！！')
        logging.warning("图片下载成功！！")
        return item

    def get_media_requests(self, item, info):
        for director in item.get('directors', []):
            director_name = director['name']
            director_image = director['image']
            logging.warning(f"Requesting image for director: {director_name}, {director_image}")
            yield Request(director_image, meta={
                'name': director_name,
                'type': 'director',
                'movie': item['name']
            })

        for actor in item.get('actors', []):
            actor_name = actor['name']
            actor_image = actor['image']
            logging.warning(f"Requesting image for actor: {actor_name}, {actor_image}")

            yield Request(actor_image, meta={
                'name': actor_name,
                'type': 'actor',
                'movie': item['name']
            })
