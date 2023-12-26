import os
import shutil
import time
import argparse


# noinspection PyTypeChecker
def synchronize_folders(source_folder, replica_folder, log_file):
    try:
        # Check if source folder exists
        if not os.path.exists(source_folder):
            log_and_print(f"Source folder '{source_folder}' does not exist", log_file)
            return

        # Create replica folder if it doesnt exist
        if not os.path.exists(replica_folder):
            os.makedirs(replica_folder)
            log_and_print(f"Replica folder '{replica_folder}' created.", log_file)

        # Walk through the replica folder and remove any files or directories not in the source folder
        for root, dirs, files in os.walk(replica_folder):
            replica_root = root.replace(replica_folder, source_folder, 1)
            for file in files:
                replica_file_path = os.path.join(root, file)
                source_file_path = os.path.join(replica_root, file)

                if not os.path.exists(source_file_path):
                    os.remove(replica_file_path)
                    log_and_print(f"Removed: '{replica_file_path}'", log_file)

            for directory in dirs:
                replica_directory_path = os.path.join(root, directory)
                source_directory_path = os.path.join(replica_root, directory)

                if not os.path.exists(source_directory_path):
                    shutil.rmtree(replica_directory_path)
                    log_and_print(f"Removed directory: '{replica_directory_path}'", log_file)

        # Walk through the source folder and copy missing or newer files to replica folder
        for root, dirs, files in os.walk(source_folder):
            replica_root = root.replace(source_folder, replica_folder, 1)
            for file in files:
                source_file_path = os.path.join(root, file)
                replica_file_path = os.path.join(replica_root, file)

                if not os.path.exists(replica_file_path) or \
                        os.stat(source_file_path).st_mtime > os.stat(replica_file_path).st_mtime:
                    shutil.copy2(source_file_path, replica_file_path)
                    log_and_print(f"Copied: '{source_file_path}' to '{replica_file_path}'", log_file)

        log_and_print("Synchronization completed.", log_file)

    except Exception as e:
        log_and_print(f"An error occured: {e}", log_file)


def log_and_print(message, log_file):
    print(message)
    with open(log_file, 'a') as f:
        f.write(f"{message}\n")


def main():
    parser = argparse.ArgumentParser(description='Folder synchronization')
    parser.add_argument('source_folder', help='Path to source folder')
    parser.add_argument('replica_folder', help='Path to replica folder')
    parser.add_argument('log_file', help='Path to log file')
    parser.add_argument('interval', type=int, help='Synchronization interval in seconds')

    args = parser.parse_args()

    source_folder = args.source_folder
    replica_folder = args.replica_folder
    log_file = args.log_file
    interval = args.interval

    while True:
        synchronize_folders(source_folder, replica_folder, log_file)
        time.sleep(interval)


if __name__ == "__main__":
    main()
