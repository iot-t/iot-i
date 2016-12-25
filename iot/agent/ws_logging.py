import logging

log_file = '/var/log/iot_ws_agent.log'
logger = logging.getLogger(__name__)
hdlr = logging.FileHandler(log_file)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)

def getLogger():
    return logger
