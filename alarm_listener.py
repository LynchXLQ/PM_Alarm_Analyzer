# -*- Coding: utf-8 -*-
# @Time     : 5/23/2025 11:16 AM
# @Author   : Linqi Xiao
# @Software : PyCharm
# @Version  : python 3.6
# @Description :

from kafka import KafkaConsumer
import logging

# 设置日志格式
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
)


def start_kafka_consumer():
    # 配置 Kafka 服务器和 Topic
    KAFKA_BROKER = '10.177.47.29:9092'
    KAFKA_TOPIC = 'alarmoptical-tunnel'
    GROUP_ID = 'transportpceTest'

    try:
        # 创建 Kafka 消费者
        consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=KAFKA_BROKER,
            group_id=GROUP_ID,
            auto_offset_reset='latest',
            enable_auto_commit=True
        )

        logging.info(f"Listening to topic `{KAFKA_TOPIC}` on broker {KAFKA_BROKER}...")

        # 无限循环读取消息
        for message in consumer:
            try:
                decoded_msg = message.value.decode('utf-8')
                logging.info(f"Received alarm message: {decoded_msg}")
            except Exception as e:
                logging.error(f"Failed to decode message: {e}")

    except Exception as e:
        logging.error(f"Kafka consumer failed to start: {e}")


if __name__ == "__main__":
    start_kafka_consumer()
