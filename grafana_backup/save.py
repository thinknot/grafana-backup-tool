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

    save_dashboards(args, settings)
    save_datasources(args, settings)
    save_folders(args, settings)
    save_alert_channels(args, settings)
    archive(args, settings)

    if aws_s3_bucket_name:
        s3_upload(args, settings)

    if influxdb_measurement:
        influx(args, settings)
