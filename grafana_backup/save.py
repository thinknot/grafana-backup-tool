from grafana_backup.save_dashboards import main as save_dashboards
from grafana_backup.save_datasources import main as save_datasources
from grafana_backup.save_folders import main as save_folders
from grafana_backup.save_alert_channels import main as save_alert_channels
from grafana_backup.archive import main as archive
from grafana_backup.s3_upload import main as s3_upload
from grafana_backup.influx import main as influx


def main(args, settings):
    aws_s3_bucket_name = settings.get('AWS_S3_BUCKET_NAME')
    influxdb_measurement = settings.get('INFLUXDB_MEASUREMENT')

    arg_components = args.get('--components', False)
    arg_no_archive = args.get('--no-archive', False)

    if aws_s3_bucket_name:
        s3_upload(args, settings)

    if influxdb_measurement:
        influx(args, settings)

    backup_functions = { 'dashboards': save_dashboards,
                         'datasources': save_datasources,
                         'folders': save_folders,
                         'alert-channels': save_alert_channels }
    if arg_components:
        arg_components_list = arg_components.split(',')
        # Backup only the components that provided via an argument
        for backup_function in arg_components_list:
            backup_functions[backup_function](args, settings)
    else:
        # Backup every component
        for backup_function in backup_functions.keys():
            backup_functions[backup_function](args, settings)
    if not arg_no_archive:
        archive(args, settings)