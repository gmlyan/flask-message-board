from server import create_app
from server.config import BaseConfig


app = create_app()


if __name__ == '__main__':
    app.run(host=BaseConfig.HOST, port=BaseConfig.PORT)
