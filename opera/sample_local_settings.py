SECRET_KEY = ''

DEBUG = False

ALLOWED_HOSTS = []

MEDIA_URL = '/media/'
STATIC_URL = '/static/'

# celery
RABBITMQ_USER = '****'
RABBITMQ_PASSWORD = '****'
RABBITMQ_VHOST = '****'
BROKER_URL = 'amqp://%s:%s@localhost:5672/%s' % (
    RABBITMQ_USER,
    RABBITMQ_PASSWORD,
    RABBITMQ_VHOST,
)

# settings for virtuoso
VIRTUOSO_ENDPOINT = '****'

MY_ENDPOINT = '****'

# retry policy for notifying the remote virtuoso opera indexers
# retry every hour for the next 3 days
RETRY_DELAY = 3600  # in seconds
MAX_RETRIES = 72  # 3 * 24
