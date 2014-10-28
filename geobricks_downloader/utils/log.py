import logging


settings = {
    "logging": {
        "level": logging.INFO,
        "format": "%(asctime)s | %(levelname)-8s | %(name)-10s | Line: %(lineno)-5d | %(message)s",
        "datefmt": "%d-%m-%Y | %H:%M:%s"
    }
}


level = settings["logging"]["level"]
custom_format = settings["logging"]["format"]
custom_date_format = settings["logging"]["datefmt"]
logging.basicConfig(level=level, format=custom_format, datefmt=custom_date_format)


def logger(logger_name=None):
    custom_logger = logging.getLogger(logger_name)
    custom_logger.setLevel(level)
    return custom_logger