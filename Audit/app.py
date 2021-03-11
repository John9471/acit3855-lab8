import connexion
from connexion import NoContent
import openapi
import json
import requests
import yaml
import logging
from logging import config
import datetime
import json
from pykafka import KafkaClient 

id = 1
with open('openapi/app_conf.yml', 'r') as f:
    app_config= yaml.safe_load(f.read())

with open('openapi/log_conf.yml', 'r') as f:
    log_config= yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')



def getInventory(index):
    hostname = "%s:%d" % (app_config["events"]["hostname"],app_config["events"]["port"]) 
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]
    consumer = topic.get_simple_consumer(reset_offset_on_start=True,consumer_timeout_ms=5000)
    logger.info("Retrieving inventory at index %d" % index)
    count = 0
    try:
        for msg in consumer:
            msg_str = msg.value.decode('utf-8')
            msg = json.loads(msg_str)
            if msg['type'] == "inventory":
                count += 1
            if int(count) == int(index):
                
                return msg["payload"], 200
    except:
        logger.error("Could not find inventory at index %d" % index)
    return { "message": "Not Found"}, 404

def getProfit(index):
    hostname = "%s:%d" % (app_config["events"]["hostname"],app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]
    # Here we reset the offset on start so that we retrieve
    # messages at the beginning of the message queue.
    # To prevent the for loop from blocking, we set the timeout to
    # 100ms. There is a risk that this loop never stops if the
    # index is large and messages are constantly being received!
    consumer = topic.get_simple_consumer(reset_offset_on_start=True,consumer_timeout_ms=1000)
    logger.info("Retrieving inventory at index %d" % index)
    count = 0

    for msg in consumer:
        msg_str = msg.value.decode('utf-8')
        msg = json.loads(msg_str)
        if msg['type'] == "profit":
            count += 1
        if int(count) == int(index):
            return msg["payload"], 200

    logger.error("Could not find profit at index %d" % index)
    return { "message": "Not Found"}, 404

app = connexion.FlaskApp(__name__, specification_dir='openapi/')
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    app.run(port=8110)