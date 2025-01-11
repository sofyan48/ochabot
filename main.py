import os, logging, sys, uvicorn, argparse
from uvicorn import Config, Server
from loguru import logger
from pkg import utils
from dotenv import load_dotenv, find_dotenv


LOG_LEVEL = logging.getLevelName(os.getenv("LOGGER_LEVEL", "INFO"))

class InterceptHandler(logging.Handler):
    def emit(self, record):
        # get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # find caller from where originated the logged message
        frame, depth = sys._getframe(6), 6
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1
        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def setup_logging():
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(LOG_LEVEL)

    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True
    # configure loguru
    logger.configure(handlers=[{"sink": sys.stdout, "serialize": True}])


if __name__ == '__main__':
    try:
        dotenv_path = find_dotenv()
        load_dotenv(dotenv_path)
    except Exception as e:
        print("Error load env: ", e)
        exit(0)
    
    parser = argparse.ArgumentParser()
    parser.add_argument("command", help="Perintah yang ingin Anda jalankan")
    args = parser.parse_args()
    from app import app, APP_ROOT
    if args.command == "serve":
        if utils.environment_transform() != "loc":
            server = Server(
                Config(
                    app=app,
                    host=os.getenv("APP_HOST", "0.0.0.0"),
                    port=int(os.getenv("APP_PORT", "8080")),
                    log_level=LOG_LEVEL,
                    workers=16,
                    timeout_keep_alive=60,
                    root_path=APP_ROOT
                ),
            )
            setup_logging()
            server.run()
        else:
            uvicorn.run(
                app="app:app",
                host=os.getenv("APP_HOST", "0.0.0.0"),
                port=int(os.getenv("APP_PORT", "8080")),
                reload=True,
                log_level=logging.getLevelName(os.getenv("LOGGER_LEVEL", "DEBUG")),
            )
        exit(0);