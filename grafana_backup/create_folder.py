import json
from grafana_backup.dashboardApi import create_folder


def main(args, settings, file_path):
    grafana_url = settings.get('GRAFANA_URL')
    http_post_headers = settings.get('HTTP_POST_HEADERS')
    verify_ssl = settings.get('VERIFY_SSL')
    client_cert = settings.get('CLIENT_CERT')
    debug = settings.get('DEBUG')

    with open(file_path, 'r') as f:
        data = f.read()

    folder = json.loads(data)
    result = create_folder(json.dumps(folder), grafana_url, http_post_headers, verify_ssl, client_cert, debug)
    print("create folder {0}, status: {1}, msg: {2}".format(folder.get('title', ''), result[0], result[1]))
