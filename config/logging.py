import logging

def setup_logging(config: dict):
    log_level = config["logging"]["level"].upper()

    try:
        level = getattr(logging, log_level)
    except AttributeError:
        raise ValueError(f"Invalid log level: {log_level}")

    logging.basicConfig(
        level = level,
        format = config["logging"]["format"]
    )