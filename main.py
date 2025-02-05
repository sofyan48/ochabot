import os, uvicorn, argparse
from pkg import utils
from dotenv import load_dotenv
from config.logger import logging_config

load_dotenv()
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("command", help="Perintah yang ingin Anda jalankan")
    args = parser.parse_args()
    if args.command == "serve":
        is_reload = False
        if utils.environment_transform() == 'loc':
            is_reload = True
        uvicorn.run(
            app="app:app",
            host=os.getenv("APP_HOST", "0.0.0.0"),
            port=int(os.getenv("APP_PORT", "8080")),
            reload=is_reload,
            log_config=logging_config
        )
        exit(0);