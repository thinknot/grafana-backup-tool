from grafana_backup.create_folder import main as create_folder
from grafana_backup.create_datasource import main as create_datasource
from grafana_backup.create_dashboard import main as create_dashboard
from grafana_backup.create_alert_channel import main as create_alert_channel
from grafana_backup.crypto import decrypt
from glob import glob
import tarfile, tempfile, sys


def main(args, settings):
    arg_archive_file = args.get('<archive_file>', None)
    arg_encrypt_passphrase = args.get('--encrypt-passphrase', '')

    encrypt_passphrase = settings.get('ENCRYPT_PASSPHRASE')

    try:
        tarfile.is_tarfile(arg_archive_file)
    except IOError as e:
        print(str(e))
        sys.exit(1)

    # Ensure encrypt_passhrase gets set if argument is used...
    if arg_encrypt_passphrase:
        encrypt_passphrase = arg_encrypt_passphrase

    with tempfile.TemporaryDirectory() as tmpdir:
        tar = tarfile.open(arg_archive_file, 'r')
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
