from pecan import make_app

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

    return make_app(
        app_conf.pop('root'),
        logging=getattr(config, 'logging', {}),
        hooks=app_hooks,
        **app_conf
    )
