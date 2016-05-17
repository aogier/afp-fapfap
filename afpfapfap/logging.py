'''
Created on 17 mag 2016

@author: oggei
'''
import logging.config
import os


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'main': {
            'format': '[%(name)s][%(levelname)s] %(message)s'
        }
    },
    'handlers': {
        'null': {
            'level': 'INFO',
            'formatter': 'main',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'tests': {
            'handlers': ['null'],
            'level': 'DEBUG' if os.environ.get('DEBUG') else 'CRITICAL',
        },
        'renamer': {
            'handlers': ['null'],
            'level': 'INFO'if os.environ.get('DEBUG') else 'CRITICAL',
        }

    }
}


def get(logger='root'):
    logging.config.dictConfig(LOGGING)
    return logging.getLogger(logger)
