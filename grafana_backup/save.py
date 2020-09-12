from grafana_backup.api_checks import main as api_checks
from grafana_backup.save_dashboards import main as save_dashboards
from grafana_backup.save_datasources import main as save_datasources
from grafana_backup.save_folders import main as save_folders
from grafana_backup.save_alert_channels import main as save_alert_channels
from grafana_backup.archive import main as archive
from grafana_backup.s3_upload import main as s3_upload
from grafana_backup.save_orgs import main as save_orgs
from grafana_backup.save_users import main as save_users
import sys


def main(args, settings):
    aws_s3_bucket_name = settings.get('AWS_S3_BUCKET_NAME')
    influxdb_measurement = settings.get('INFLUXDB_MEASUREMENT')

    arg_components = args.get('--components', False)
    arg_no_archive = args.get('--no-archive', False)

    backup_functions = {'dashboards': save_dashboards,
                        'datasources': save_datasources,
                        'folders': save_folders,
                        'alert-channels': save_alert_channels,
                        'organizations': save_orgs,
                        'users': save_users}

    (status, json_resp, api_version) = api_checks(settings)

    # Do not continue if API is unavailable or token is not valid
    if not status == 200:
        print("server status is not ok: {0}".format(json_resp))
        sys.exit(1)

    settings.update({'API_VERSION': api_version})

        influx(args, settings)
    if influxdb_measurement:
    if arg_components:
        arg_components_list = arg_components.split(',')
        # Backup only the components that provided via an argument
        for backup_function in arg_components_list:
            backup_functions[backup_function](args, settings)
    else:
        # Backup every component
        for backup_function in backup_functions.keys():
            backup_functions[backup_function](args, settings)

    aws_s3_bucket_name = settings.get('AWS_S3_BUCKET_NAME')

    if not arg_no_archive:
        archive(args, settings)

    if aws_s3_bucket_name:
        print('Upload archives to S3:')
        s3_upload(args, settings)
