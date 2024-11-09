from logging import Logger
from datetime import datetime
from lib.kafka_connect import KafkaConsumer
from cdm_loader.repository import *

class CdmMessageProcessor:
    def __init__(self,
                 consumer: KafkaConsumer,
                 cdm_repository: CdmRepository,
                 batch_size: int, 
                 logger: Logger) -> None:
        self._consumer = consumer
        self._cdm_repository = cdm_repository
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
            user_id = order["user_id"]
            product_id = order["product_id"]
            category_id = order["category_id"]
            product_name = order["product_name"]
            category_name = order["category_name"]
            order_cnt = order["order_cnt"]

            self._cdm_repository.user_product_counters_insert(user_id, product_id, product_name, order_cnt)
            self._cdm_repository.user_category_counters_insert(user_id, category_id, category_name, order_cnt)      

        self._logger.info(f"{datetime.utcnow()}: FINISH")