# Server Specific Configurations
server = {
    'port': '8080',
    'host': '0.0.0.0'
}

# Pecan Application Configurations
app = {
    'root': 'iot.controllers.root.RootController',
    'modules': ['iot'],
    'static_root': '%(confdir)s/public',
    'template_path': '%(confdir)s/iot/templates',
    'debug': True,
    'default_renderer': 'jinja',
    'errors': {
        404: '/error/404',
        '__force_dict__': True
    },
}

logging = {
    'root': {'level': 'INFO', 'handlers': ['console']},
    'loggers': {
        'iot': {'level': 'DEBUG', 'handlers': ['console'], 'propagate': False},
        'pecan': {'level': 'DEBUG', 'handlers': ['console'], 'propagate': False},
        'py.warnings': {'handlers': ['console']},
        '__force_dict__': True
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'color'
        }
    },
    'formatters': {
        'simple': {
            'format': ('%(asctime)s %(levelname)-5.5s [%(name)s]'
                       '[%(threadName)s] %(message)s')
        },
        'color': {
            '()': 'pecan.log.ColorFormatter',
            'format': ('%(asctime)s [%(padded_color_levelname)s] [%(name)s]'
                       '[%(threadName)s] %(message)s'),
        '__force_dict__': True
        }
    }
}


# Bindings and options to pass to SQLAlchemy's ``create_engine``
sqlalchemy = {
    'url': 'mysql://root:@localhost/dbname?charset=utf8&use_unicode=0',
    'echo': False,
    'echo_pool': False,
    'pool_recycle': 3600,
    'encoding': 'utf-8'
}

redis = {
    'host': '127.0.0.1',
    'port': 6379
}

mongo = {
    'url': 'mongodb://autoscrapy:123456@127.0.0.1/autoscrapy'
}

# Custom Configurations must be in Python dictionary format::
#
# foo = {'bar':'baz'}
#
# All configurations are accessible at::
# pecan.conf
