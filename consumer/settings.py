import os

# BROKER
LOG_FORMAT = '%(levelname) -10s %(asctime)s %(name) -30s %(funcName) -35s %(lineno) -5d: %(message)s'

BROKER_HOST = os.getenv('BROKER_HOST', '0.0.0.0')
BROKER_PORT = os.getenv('BROKER_PORT', '5672')
BROKER_USER = os.getenv('BROKER_USER', 'guest')
BROKER_PASSWORD = os.getenv('BROKER_PASSWORD', 'guest')

DEFAULT_QUEUE = os.getenv('DEFAULT_QUEUE', 'default-queue')

# MAILCATCHER
MAILCATCHER_HOST = os.getenv('MAILCATCHER_HOST', '0.0.0.0')
MAILCATCHER_PORT = os.getenv('MAILCATCHER_PORT', '1025')
