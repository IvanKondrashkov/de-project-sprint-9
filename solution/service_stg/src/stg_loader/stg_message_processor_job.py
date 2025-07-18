from datetime import datetime
from logging import Logger
from typing import List, Dict
from lib.util import str2json, json2str
from lib.kafka_connect import KafkaConsumer, KafkaProducer
from lib.redis import RedisClient
from stg_loader.repository import *

class StgMessageProcessor:
    def __init__(self,
                 consumer: KafkaConsumer,
                 producer: KafkaProducer,
                 redis: RedisClient,
                 stg_repository: StgRepository,
                 batch_size: int, 
                 logger: Logger) -> None:
        self._consumer = consumer
        self._producer = producer
        self._redis = redis
        self._stg_repository = stg_repository
        self._batch_size = batch_size
        self._logger = logger

    def run(self) -> None:
        self._logger.info(f"{datetime.utcnow()}: START")

        for _ in range(self._batch_size):
            msg = self._consumer.consume()
            if not msg:
                break

            self._logger.info(f"{datetime.utcnow()}: Message received")
            self._logger.info(f"{msg}: Message object")

            msg_consumer = MessageConsumerObj(**msg)
            order = msg_consumer.payload
            self._stg_repository.order_events_insert(
                msg_consumer.object_id,
                msg_consumer.object_type,
                msg_consumer.sent_dttm,
                json2str(order))

            user_id = order["user"]["id"]
            user = self._redis.get(user_id)
            user_name = user["name"]
            user_login = user["login"]

            restaurant_id = order["restaurant"]["id"]
            restaurant = self._redis.get(restaurant_id)
            restaurant_name = restaurant["name"]

            dst_msg = {
                "object_id": msg_consumer.object_id,
                "object_type": "order",
                "payload": {
                    "id": msg_consumer.object_id,
                    "date": order["date"],
                    "cost": order["cost"],
                    "payment": order["payment"],
                    "status": order["final_status"],
                    "restaurant": self._format_restaurant(restaurant_id, restaurant_name),
                    "user": self._format_user(user_id, user_name, user_login),
                    "products": self._format_items(order["order_items"], restaurant)
                }
            }

            msg_producer = MessageProducerObj(**dst_msg)
            self._producer.produce(str2json(msg_producer.model_dump_json()))
            self._logger.info(f"{datetime.utcnow()}. Message Sent")

        self._logger.info(f"{datetime.utcnow()}: FINISH")

    def _format_restaurant(self, id, name) -> Dict[str, str]:
        return {
            "id": id,
            "name": name
        }

    def _format_user(self, id, name, login) -> Dict[str, str]:
        return {
            "id": id,
            "name": name,
            "login": login
        }

    def _format_items(self, order_items, restaurant) -> List[Dict[str, str]]:
        items = []

        menu = restaurant["menu"]
        for it in order_items:
            menu_item = next(x for x in menu if x["_id"] == it["id"])
            dst_it = {
                "id": it["id"],
                "price": it["price"],
                "quantity": it["quantity"],
                "name": menu_item["name"],
                "category": menu_item["category"]
            }
            items.append(dst_it)

        return items   