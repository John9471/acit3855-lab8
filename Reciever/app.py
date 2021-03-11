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

client = KafkaClient(hosts=app_config['events']['hostname']+':'+str(app_config['events']['port']))
topic = client.topics[str.encode(app_config['events']['topic'])]
producer = topic.get_sync_producer()



def addInventory(body):
    global id
    print(body)
    headers = {'Content-Type':'application/json'}
    
    msg = {"type": "inventory",
            "datetime": datetime.datetime.now().strftime("%Y-%m-%d"),
            "payload": body}
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))

    logger.info('revieved event "Add Inventory" request with a unique id of '+ str(id))
    logger.info('returned event "Add Inventory" request id:'+str(id)+' with a status of '+ str(201))
    id += 1
    return NoContent, 201

def addProfit(body):
    global id
    print(body)
    headers = {'Content-Type':'application/json'}
    msg = {"type": "profit",
            "datetime": datetime.datetime.now().strftime("%Y-%m-%d"),
            "payload": body}
    logger.info('revieved event "Add Profit" request with a unique id of '+ str(id))
    logger.info('returned event "Add Profit" request id:'+str(id)+' with a status of '+ str(201))
    id += 1
    
    return NoContent, 201
    

app = connexion.FlaskApp(__name__, specification_dir='openapi/')
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    app.run(port=8080)