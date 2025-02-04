import os, uvicorn, argparse
from pkg import utils
from dotenv import load_dotenv, find_dotenv
from config.logger import logging_config


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
    if args.command == "serve":
        worker = 2
        if os.environ.get("IS_WORKER_SET", False):
            from config.multiprocessing import UvicornWorkerRecommender
            worker = UvicornWorkerRecommender().recommend_workers()
        if utils.environment_transform() != "loc":
            uvicorn.run(
                app="app:app",
                host=os.getenv("APP_HOST", "0.0.0.0"),
                port=int(os.getenv("APP_PORT", "8080")),
                workers=2,
                reload=False,
                log_config=logging_config
            )
        else:
            uvicorn.run(
                app="app:app",
                host=os.getenv("APP_HOST", "0.0.0.0"),
                port=int(os.getenv("APP_PORT", "8080")),
                reload=True,
                # log_config=logging_config
            )
        exit(0);