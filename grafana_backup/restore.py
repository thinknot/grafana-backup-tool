from grafana_backup.create_folder import main as create_folder
from grafana_backup.create_datasource import main as create_datasource
from grafana_backup.create_dashboard import main as create_dashboard
from grafana_backup.create_alert_channel import main as create_alert_channel
from grafana_backup.s3_download import main as s3_download
from grafana_backup.crypto import decrypt
from glob import glob
import tarfile, tempfile, sys


def main(args, settings):
    archive_file = args.get('<archive_file>', None)
    arg_components = args.get('--components', False)
    arg_encrypt_passphrase = args.get('--encrypt-passphrase', '')

    encrypt_passphrase = settings.get('ENCRYPT_PASSPHRASE')
    aws_s3_bucket_name = settings.get('AWS_S3_BUCKET_NAME')

    # Ensure encrypt_passhrase gets set if argument is used...
    if arg_encrypt_passphrase:
        encrypt_passphrase = arg_encrypt_passphrase

    # Use tar data stream if S3 bucket name is specified
    if aws_s3_bucket_name:
        s3_data = s3_download(args, settings)
        try:
            tar = tarfile.open(fileobj=s3_data, mode='r:gz')    
        except Exception as e:
            print(str(e))
            sys.exit(1)
    else:
        try:
            tarfile.is_tarfile(name=arg_archive_file)
        except IOError as e:
            print(str(e))
            sys.exit(1)
        try:
            tar = tarfile.open(name=arg_archive_file, mode='r:gz')
        except Exception as e:
            print(str(e))
            sys.exit(1)

    with tempfile.TemporaryDirectory() as tmpdir:
        tar.extractall(tmpdir)
        tar.close()
        for ext in ['folder', 'datasource', 'dashboard', 'alert_channel']:
            for file_path in glob('{0}/**/*.{1}'.format(tmpdir, ext), recursive=True): 
                if encrypt_passphrase:
                    print("Decrypting backup contents using supplied passphrase...")
                    with open(file_path, 'r+') as f:
                        encrypted_data = f.read()
                        data = decrypt(encrypt_passphrase, encrypted_data)
                        f.seek(0)
                        f.write(data)
                        f.truncate()
                if ext == 'folder':
                    print('restoring folder: {0}'.format(file_path))
                    create_folder(args, settings, file_path)
                if ext == 'datasource':
                    print('restoring datasource: {0}'.format(file_path))
                    create_datasource(args, settings, file_path)
                if ext == 'dashboard':
                    print('restoring dashboard: {0}'.format(file_path))
                    create_dashboard(args, settings, file_path)
                if ext == 'alert_channel':
                    print('restoring alert_channel: {0}'.format(file_path))
                    create_alert_channel(args, settings, file_path)

        restore_functions = { 'folder': create_folder,
                              'datasource': create_datasource,
                              'dashboard': create_dashboard,
                              'alert_channel': create_alert_channel }

        if arg_components:
            arg_components_list = arg_components.split(',')

            # Restore only the components that provided via an argument
            # but must also exist in extracted archive
            for ext in arg_components_list:
                for file_path in glob('{0}/**/*.{1}'.format(tmpdir, ext[:-1]), recursive=True):
                    print('restoring {0}: {1}'.format(ext, file_path))
                    restore_functions[ext[:-1]](args, settings, file_path)
        else:
            # Restore every component included in extracted archive
            for ext in restore_functions.keys():
                for file_path in glob('{0}/**/*.{1}'.format(tmpdir, ext), recursive=True):
                    print('restoring {0}: {1}'.format(ext, file_path))
                    restore_functions[ext](args, settings, file_path)
