import logging
import routes
from settings import log_conf, app
from models.db import db


def configure_logs():
    log_file_name = log_conf["file_name"]
    log_level = log_conf["level"]

    # Needed to clear log file
    with open(log_file_name, "w"):
        pass

    logging.basicConfig(
        filename=log_file_name,
        level=log_level,
        format="%(asctime)s %(levelname)-5s[%(name)s] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


if __name__ == "__main__":
    configure_logs()
    db.create_all()
    app.run()

