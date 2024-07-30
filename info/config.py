from datetime import time

BOT_TOK = ''
api_key = ''
NOTIFICATION_TIME = time(hour=9, minute=0, second=0)

WEBHOOK_HOST = ''
WEBHOOK_LISTEN = '0.0.0.0'
WEBHOOK_PORT = 443

WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Путь к сертификату
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Путь к приватному ключу

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (BOT_TOK)
