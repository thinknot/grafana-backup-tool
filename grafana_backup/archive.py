from grafana_backup.crypto import encrypt
from glob import glob
import tarfile, shutil


def main(args, settings):
    arg_encrypt_passphrase = args.get('--encrypt-passphrase', '')

    backup_dir = settings.get('BACKUP_DIR')
    timestamp = settings.get('TIMESTAMP')
    encrypt_passphrase = settings.get('ENCRYPT_PASSPHRASE')

    archive_file = '{0}/{1}.tar.gz'.format(backup_dir, timestamp)
    backup_dirs = list()
    backup_files = list()

    for folder_name in ['folders', 'datasources', 'dashboards', 'alert_channels']:
        backup_path = '{0}/{1}/{2}'.format(backup_dir, folder_name, timestamp)

        for dir_path in glob(backup_path):
            backup_dirs.append(dir_path)

        for file_path in glob('{0}/**/*.{1}'.format(backup_dir, folder_name[:-1]), recursive=True):
            backup_files.append(file_path)

    # Ensure encrypt_passhrase gets set if argument is used...
    if arg_encrypt_passphrase:
        encrypt_passphrase = arg_encrypt_passphrase

    with tarfile.open(archive_file, "x:gz") as tar:
        if encrypt_passphrase:
            print("Encrypting backup using supplied passphrase... Don't forget to write it down!")
            for file_path in backup_files:
                with open(file_path, 'r+') as f:
                    data = f.read()
                    encrypted_data = encrypt(encrypt_passphrase, data)
                    f.seek(0)
                    f.write(encrypted_data.decode('utf-8'))
                    f.truncate()
        for dir_path in backup_dirs:
            tar.add(dir_path)
            shutil.rmtree(dir_path)
    tar.close()
    print('created archive: {0}'.format(archive_file))
