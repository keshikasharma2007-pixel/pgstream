from flask import Flask
from controllers.pub_controller import pub_controller
from controllers.sub_controller import sub_controller

import logging
from config.settings import load_config
from config.logging import setup_logging
from config.db import get_db_connection

from repositories.pub_repository import PubRepository
from repositories.sub_repository import SubRepository
from services.pub_service import PubService
from services.sub_services import SubService

config = load_config()
setup_logging(config)

logger = logging.getLogger(__name__)
conn = get_db_connection(config)

pub_repo = PubRepository(conn, logger)
sub_repo = SubRepository(conn, logger)

logging.info("app wired and starting...")

app = Flask(__name__)
app.register_blueprint(pub_controller)
app.register_blueprint(sub_controller)


print(app.url_map)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)