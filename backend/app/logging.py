import logging
from pymongo import MongoClient
from app.constants.config_strings import ConfigStrings

class MongoHandler(logging.Handler):
    """Custom logging handler to write logs to MongoDB."""
    def __init__(self, mongo_uri, database, collection):
        super().__init__()
        client = MongoClient(mongo_uri)
        self.collection = client[database][collection]

    def emit(self, record):
        log_entry = self.format(record)
        self.collection.insert_one({
            "log": log_entry,
            "level": record.levelname,
            "message": record.msg,
            "time": record.asctime,
        })

def setup_logging(app):
    mongo_handler = MongoHandler(ConfigStrings.MONGO_URI, ConfigStrings.LOG_DATABASE, ConfigStrings.LOG_COLLECTION)
    mongo_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    mongo_handler.setFormatter(formatter)
    app.logger.addHandler(mongo_handler)
