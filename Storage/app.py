import connexion
from connexion import NoContent

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from inventory import Inventory
from profit import Profit
import datetime
import yaml
import logging
from logging import config
from datetime import datetime
from pykafka import KafkaClient
from pykafka.common import OffsetType
from threading import Thread
import json


id = 1

with open('openapi/app_conf.yml', 'r') as f:
    app_config= yaml.safe_load(f.read())

DB_ENGINE = create_engine('mysql+pymysql://'+app_config['datastore']['user']+':'+app_config['datastore']['password']+'@'+app_config['datastore']['hostname']+':'+app_config['datastore']['port']+'/'+app_config['datastore']['db']+'')
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)



with open('openapi/log_conf.yml', 'r') as f:
    log_config= yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)
    
logger = logging.getLogger('basicLogger')
logger.info("connecting to mysql database: "+app_config['datastore']['hostname']+':'+app_config['datastore']['port'])


def getInventory(timestamp):
    session = DB_SESSION()

    timestamp_datetime = datetime.strptime(timestamp, "%Y-%m-%d")
    print(timestamp_datetime)
    readings = session.query(Inventory).filter(Inventory.date_created >=
    timestamp_datetime)
    results_list = []
    for reading in readings:
        results_list.append(reading.to_dict())
    session.close()

    logger.info("Query for Inventory readings after %s returns %d results" %
    (timestamp, len(results_list)))
    return results_list, 200

    
def getProfit(timestamp):
    session = DB_SESSION()

    timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%d")
    print(timestamp_datetime)
    readings = session.query(Profit).filter(Profit.date_created >=
    timestamp_datetime)
    results_list = []
    for reading in readings:
        results_list.append(reading.to_dict())
    session.close()

    logger.info("Query for Profit readings after %s returns %d results" %
    (timestamp, len(results_list)))
    return results_list, 200

app = connexion.FlaskApp(__name__, specification_dir='openapi/')
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)

def process_messages():
    global id

    hostname = "%s:%d" % (app_config["events"]["hostname"],app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]

    # Create a consume on a consumer group, that only reads new messages
    # (uncommitted messages) when the service re-starts (i.e., it doesn't
    # read all the old messages from the history in the message queue).
    consumer = topic.get_simple_consumer(consumer_group=b'event_group',reset_offset_on_start=False,auto_offset_reset=OffsetType.LATEST)
    # This is blocking - it will wait for a new message
    for msg in consumer:
        msg_str = msg.value.decode('utf-8')
        msg = json.loads(msg_str)
        logger.info("Message: %s" % msg)
        payload = msg["payload"]
        if msg["type"] == "inventory": 
            session = DB_SESSION()
            print(payload)
            inventory = Inventory(payload['name'],
                            payload['contents'],
                            payload['price'])

            session.add(inventory)

            session.commit()
            session.close()
            logger.debug('stored event "Add Inventory" with a unique id of '+str(id)) 
            id += 1

        elif msg["type"] == "profit": 
            session = DB_SESSION()

            profit = Profit(payload['companyName'],
                            payload['quantity'],
                            payload['drink'])

            session.add(profit)

            session.commit()
            session.close()
            logger.debug('stored event "Add Profit" with a unique id of '+str(id)) 
            id += 1
        consumer.commit_offsets()


if __name__ == "__main__":
    t1 = Thread(target=process_messages)
    t1.setDaemon(True)
    t1.start()
    app.run(port=8090)