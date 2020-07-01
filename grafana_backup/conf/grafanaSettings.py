from grafana_backup.commons import load_config
from datetime import datetime
import os, json


def main(config_path):
    # Load config from optional configuration file located at ~/.grafana-backup.yml
    # or load defaults from example config stored in grafana-backup.example.yml
    # environment variables can override settings as well

    config_dict = {}

    config = load_config(config_path)

    grafana_url = config.get('grafana', {}).get('url', '')
    grafana_token = config.get('grafana', {}).get('token', '')
    grafana_search_api_limit = config.get('grafana', {}).get('search_api_limit', 5000)

    debug = config.get('main', {}).get('debug', True)
    verify_ssl = config.get('main', {}).get('verify_ssl', False)
    backup_dir = config.get('main', {}).get('backup_dir', '_OUTPUT_')
    encrypt_passphrase = config.get('main', {}).get('encrypt_passphrase', '')
    aws_s3_bucket_name = config.get('aws', {}).get('s3_bucket_name', '')
    aws_s3_bucket_key = config.get('aws', {}).get('s3_bucket_key', '')
    aws_default_region = config.get('aws', {}).get('default_region', '')
    aws_access_key_id = config.get('aws', {}).get('access_key_id', '')
    aws_secret_access_key = config.get('aws', {}).get('secret_access_key', '')

    influxdb_measurement = config.get('influxdb', {}).get('measurement', '')
    influxdb_host = config.get('influxdb', {}).get('host', '')
    influxdb_port = config.get('influxdb', {}).get('port', 0)
    influxdb_username = config.get('influxdb', {}).get('username', '')
    influxdb_password = config.get('influxdb', {}).get('password', '')
    influxdb_database = config.get('influxdb', {}).get('database', '')

    GRAFANA_URL = os.getenv('GRAFANA_URL', grafana_url)
    TOKEN = os.getenv('GRAFANA_TOKEN', grafana_token)
    SEARCH_API_LIMIT = os.getenv('SEARCH_API_LIMIT', grafana_search_api_limit)
    ENCRYPT_PASSPHRASE = os.getenv('ENCRYPT_PASSPHRASE', encrypt_passphrase)

    AWS_S3_BUCKET_NAME = os.getenv('AWS_S3_BUCKET_NAME', aws_s3_bucket_name)
    AWS_S3_BUCKET_KEY = os.getenv('AWS_S3_BUCKET_KEY', aws_s3_bucket_key)
    AWS_DEFAULT_REGION = os.getenv('AWS_DEFAULT_REGION', aws_default_region)
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', aws_access_key_id)
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', aws_secret_access_key)

    INFLUXDB_MEASUREMENT = os.getenv('INFLUXDB_MEASUREMENT', influxdb_measurement)
    INFLUXDB_HOST = os.getenv('INFLUXDB_HOST', influxdb_host)
    INFLUXDB_PORT = int(os.getenv('INFLUXDB_PORT', influxdb_port))
    INFLUXDB_USERNAME = os.getenv('INFLUXDB_USERNAME', influxdb_username)
    INFLUXDB_PASSWORD = os.getenv('INFLUXDB_PASSWORD', influxdb_password)
    INFLUXDB_DATABASE = os.getenv('INFLUXDB_DATABASE', influxdb_database)

    DEBUG = os.getenv('DEBUG', debug)
    if isinstance(DEBUG, str):
        DEBUG = json.loads(DEBUG.lower()) # convert environment variable string to bool

    VERIFY_SSL = os.getenv('VERIFY_SSL', verify_ssl)
    if isinstance(VERIFY_SSL, str):
        VERIFY_SSL = json.loads(VERIFY_SSL.lower()) # convert environment variable string to bool

    BACKUP_DIR = os.getenv('BACKUP_DIR', backup_dir)

    EXTRA_HEADERS = dict(h.split(':') for h in os.getenv('GRAFANA_HEADERS', '').split(',') if 'GRAFANA_HEADERS' in os.environ)

    HTTP_GET_HEADERS = {'Authorization': 'Bearer ' + TOKEN}
    HTTP_POST_HEADERS = {'Authorization': 'Bearer ' + TOKEN, 'Content-Type': 'application/json'}

    for k,v in EXTRA_HEADERS.items():
        HTTP_GET_HEADERS.update({k: v})
        HTTP_POST_HEADERS.update({k: v})

    TIMESTAMP = datetime.today().strftime('%Y%m%d%H%M')

    config_dict['GRAFANA_URL'] = GRAFANA_URL
    config_dict['TOKEN'] = TOKEN
    config_dict['SEARCH_API_LIMIT'] = SEARCH_API_LIMIT
    config_dict['DEBUG'] = DEBUG
    config_dict['VERIFY_SSL'] = VERIFY_SSL
    config_dict['BACKUP_DIR'] = BACKUP_DIR
    config_dict['EXTRA_HEADERS'] = EXTRA_HEADERS
    config_dict['HTTP_GET_HEADERS'] = HTTP_GET_HEADERS
    config_dict['HTTP_POST_HEADERS'] = HTTP_POST_HEADERS
    config_dict['TIMESTAMP'] = TIMESTAMP
    config_dict['ENCRYPT_PASSPHRASE'] = ENCRYPT_PASSPHRASE
    config_dict['AWS_S3_BUCKET_NAME'] = AWS_S3_BUCKET_NAME
    config_dict['AWS_S3_BUCKET_KEY'] = AWS_S3_BUCKET_KEY
    config_dict['AWS_DEFAULT_REGION'] = AWS_DEFAULT_REGION
    config_dict['AWS_ACCESS_KEY_ID'] = AWS_ACCESS_KEY_ID
    config_dict['AWS_SECRET_ACCESS_KEY'] = AWS_SECRET_ACCESS_KEY
    config_dict['INFLUXDB_MEASUREMENT'] = INFLUXDB_MEASUREMENT
    config_dict['INFLUXDB_HOST'] = INFLUXDB_HOST
    config_dict['INFLUXDB_PORT'] = INFLUXDB_PORT
    config_dict['INFLUXDB_USERNAME'] = INFLUXDB_USERNAME
    config_dict['INFLUXDB_PASSWORD'] = INFLUXDB_PASSWORD
    config_dict['INFLUXDB_DATABASE'] = INFLUXDB_DATABASE

    return config_dict
