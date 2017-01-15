from pecan import make_app
from beaker.middleware import SessionMiddleware

from iot import model
from iot import hooks

def setup_app(config):

    model.init_model()
    app_conf = dict(config.app)
    app_hooks = [
            hooks.RedisDbHook(),
            hooks.MongoDbHook(),
            hooks.SqlalchemyTransactionHook(),
    ]

    app = make_app(
        app_conf.pop('root'),
        logging=getattr(config, 'logging', {}),
        hooks=app_hooks,
        **app_conf
    )
    return SessionMiddleware(app, config.beaker)
