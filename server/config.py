from environs import Env

env = Env()
env.read_env()


class BaseConfig:
    HOST = env.str('HOST')
    PORT = env.str('PORT')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True


