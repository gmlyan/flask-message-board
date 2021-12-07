from environs import Env

env = Env()
env.read_env()


class BaseConfig:
    HOST = env.str('HOST')
    PORT = env.str('PORT')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data.sqlite'
    PROPAGATE_EXCEPTIONS = True

