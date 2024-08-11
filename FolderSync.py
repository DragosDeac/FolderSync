import os
import shutil  
import hashlib
import time
import argparse

def sync_folders(source_dir, replica_dir, log_file):
    # Create copy of source folder if it doesn't exist
    if not os.path.exists(replica_dir):
        os.makedirs(replica_dir)

    # Get the list of files and folders in the source directory
    source_list = os.listdir(source_dir)
    
    #Deleting and/or copying:
        
    # Copy files from source to replica folder
    for source_file in source_list:
        source_path = os.path.join(source_dir, source_file)
        replica_path = os.path.join(replica_dir, source_file)

        # Check if the file is a folder or a file
        if os.path.isdir(source_path):
            # Recursively copy the folder
            sync_folders(source_path, replica_path, log_file)
        else:
            # Copy the file to the replica folder
            shutil.copy2(source_path, replica_path)

            # Write to the log file and console output
            log_file.write("Copied file from {} to {}\n".format(source_path, replica_path))
            print("Copied file from {} to {}".format(source_path, replica_path))

    # Delete files in replica folder that are not in source folder
    replica_list = os.listdir(replica_dir)
    for replica_file in replica_list:
        replica_path = os.path.join(replica_dir, replica_file)
        source_path = os.path.join(source_dir, replica_file)

        if not os.path.exists(source_path):
            # Delete the file from the replica folder
            os.remove(replica_path)

            # Write to the log file and console output
            log_file.write("Deleted file {}\n".format(replica_path))
            print("Deleted file {}".format(replica_path))

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Sync two folders - main with a copy')
    parser.add_argument('source_dir', type=str, help=r'NewTextDocument.txt') #Source Dir
    parser.add_argument('replica_dir', type=str, help=r'NewTextDocument(2).txt') #Replica Dir
    parser.add_argument('interval', type=int, help=r'5') #Clock
    parser.add_argument('log_file', type=str, help=r'Logs.txt')#Log Dir
    args = parser.parse_args()

    # Loop indefinitely 
    while True:
        # Sync the folders
        with open(args.log_file, 'a') as log_file:
            sync_folders(args.source_dir, args.replica_dir, log_file)

        # Wait for the sync interval
        time.sleep(args.interval)

if __name__ == '__main__':
    main()
