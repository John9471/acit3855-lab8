import connexion
from connexion import NoContent
import openapi
import json
import requests
import yaml
import logging
from logging import config
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

id = 1
with open('openapi/app_conf.yml', 'r') as f:
    app_config= yaml.safe_load(f.read())

with open('openapi/log_conf.yml', 'r') as f:
    log_config= yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

loggingRN= False


def getStats():
    global id
    r = requests.get(app_config['eventstore']['url'])
    logger.info('revieved event "Get stats" request with a unique id of '+ str(id))
    logger.info('returned event "Get Stats" request id:'+str(id)+' with a status of '+ str(r.status_code))
    id += 1
    return NoContent, r.status_code


def populate_stats():
    """ periodically update stats """
    global loggingRN
    if loggingRN == False:
        logger.info("Periodic processing has started")
        loggingRN = True



    now = datetime.now()
    format = "%Y-%m-%d"
    date = now.strftime(format)
    r = requests.get(app_config["eventstore"]["url"]+"/inventory/purchase", params={"timestamp":str(date)})
    r2 = requests.get(app_config["eventstore"]["url"]+"/orders", params={"timestamp":str(date)})

    if r.status_code == 200 and r2.status_code == 200:
        n = len(r.json())
        n2 = len(r2.json())
        data = {"items":n, "orders":n2, "last item": r.json()[-1], "last order": r2.json()[-1], "last updated":str(datetime.now())}
        logger.info(f"{n} items and {n2} orders received.")
        with open('data.json', 'w') as f:
            json.dump(data, f)


    else:
        logger.error("what?")

def getData():
    try:
        with open("data.json","r") as f:
            data = json.load(f)
            return data, 200
    except:
        return {"message": "Error"}, 400

def init_scheduler():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(populate_stats,
    'interval',
    seconds=app_config['scheduler']['period_sec'])
    sched.start()


app = connexion.FlaskApp(__name__, specification_dir='openapi/')
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
 # run our standalone gevent server
    init_scheduler()
    app.run(port=8100, use_reloader=False)