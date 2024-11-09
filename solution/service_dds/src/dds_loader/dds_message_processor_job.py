import uuid
from logging import Logger
from datetime import datetime
from lib.util import str2json
from lib.kafka_connect import KafkaConsumer, KafkaProducer
from dds_loader.repository import *

class DdsMessageProcessor:
    def __init__(self,
                 consumer: KafkaConsumer,
                 producer: KafkaProducer,
                 dds_repository: DdsRepository,
                 batch_size: int, 
                 logger: Logger) -> None:
        self._consumer = consumer
        self._producer = producer
        self._dds_repository = dds_repository
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
            order_id = msg_consumer.object_id
            order_date = order["date"]
            order_cost = order["cost"]
            order_payment = order["payment"]
            order_status = order["status"]
            user_id = order["user"]["id"]
            user_name = order["user"]["name"]
            user_login = order["user"]["login"]
            restaurant_id = order["restaurant"]["id"]
            restaurant_name = order["restaurant"]["name"]

            load_dt = datetime.now()
            load_src = "service_stg"

            h_user_pk = uuid.uuid5(uuid.NAMESPACE_X500, str(user_id))
            h_restaurant_pk = uuid.uuid5(uuid.NAMESPACE_X500, str(restaurant_id))
            h_order_pk = uuid.uuid5(uuid.NAMESPACE_X500, str(order_id))
            hk_order_user_pk = uuid.uuid5(uuid.NAMESPACE_X500, "".join([str(h_order_pk), str(h_user_pk)]))
            hk_user_names_hashdiff = uuid.uuid5(uuid.NAMESPACE_X500, "".join([str(h_user_pk), str(load_dt)]))
            hk_restaurant_names_hashdiff = uuid.uuid5(uuid.NAMESPACE_X500, "".join([str(h_restaurant_pk), str(load_dt)]))
            hk_order_cost_hashdiff = uuid.uuid5(uuid.NAMESPACE_X500, "".join([str(h_order_pk), str(load_dt)]))
            hk_order_status_hashdiff = uuid.uuid5(uuid.NAMESPACE_X500, "".join([str(h_order_pk), str(load_dt)]))

            self._dds_repository.h_user_insert(h_user_pk, user_id, load_dt, load_src)
            self._dds_repository.h_restaurant_insert(h_restaurant_pk, restaurant_id, load_dt, load_src)
            self._dds_repository.h_order_insert(h_order_pk, order_id, order_date, load_dt, load_src)

            self._dds_repository.l_order_user_insert(hk_order_user_pk, h_order_pk, h_user_pk, load_dt, load_src)

            self._dds_repository.s_user_names_insert(hk_user_names_hashdiff, h_user_pk, user_name, user_login, load_dt, load_src)
            self._dds_repository.s_restaurant_names_insert(hk_restaurant_names_hashdiff, h_restaurant_pk, restaurant_name, load_dt, load_src)
            self._dds_repository.s_order_cost_insert(hk_order_cost_hashdiff, h_order_pk, order_cost, order_payment, load_dt, load_src)
            self._dds_repository.s_order_status_insert(hk_order_status_hashdiff, h_order_pk, order_status, load_dt, load_src)


            for product in order["products"]:
                product_id = product["id"]
                product_name = product["name"]
                product_category = product["category"]
                h_product_pk = uuid.uuid5(uuid.NAMESPACE_X500, str(product_id))
                h_category_pk = uuid.uuid5(uuid.NAMESPACE_X500, str(product_category))
                hk_order_product_pk = uuid.uuid5(uuid.NAMESPACE_X500, "".join([str(h_order_pk), str(h_product_pk)]))
                hk_product_restaurant_pk = uuid.uuid5(uuid.NAMESPACE_X500, "".join([str(h_product_pk), str(h_restaurant_pk)]))
                hk_product_category_pk = uuid.uuid5(uuid.NAMESPACE_X500, "".join([str(h_product_pk), str(h_category_pk)]))
                hk_product_names_hashdiff = uuid.uuid5(uuid.NAMESPACE_X500, "".join([str(h_product_pk), str(load_dt)]))

                self._dds_repository.h_product_insert(h_product_pk, product_id, load_dt, load_src)
                self._dds_repository.h_category_insert(h_category_pk, product_category, load_dt, load_src)

                self._dds_repository.l_order_product_insert(hk_order_product_pk, h_order_pk, h_product_pk, load_dt, load_src)
                self._dds_repository.l_product_restaurant_insert(hk_product_restaurant_pk, h_product_pk, h_restaurant_pk, load_dt, load_src)
                self._dds_repository.l_product_category_insert(hk_product_category_pk, h_product_pk, h_category_pk, load_dt, load_src)
                self._dds_repository.s_product_names_insert(hk_product_names_hashdiff, h_product_pk, product_name, load_dt, load_src)

                dst_msg = {
                    "object_id": msg_consumer.object_id,
                    "object_type": "order",
                    "payload": {
                        "user_id": h_user_pk,
                        "product_id": h_product_pk,
                        "category_id": h_category_pk,
                        "product_name": product_name,
                        "category_name": product_category,
                        "order_cnt": 1
                    }
                }

                msg_producer = MessageProducerObj(**dst_msg)
                self._producer.produce(str2json(msg_producer.model_dump_json()))
                self._logger.info(f"{datetime.utcnow()}. Message Sent")        

        self._logger.info(f"{datetime.utcnow()}: FINISH")