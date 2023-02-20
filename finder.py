# Importing Libraries
import hashlib
import json
import os
import argparse
  
# Calculates MD5 hash of file
# Returns HEX digest of file
def get_hash(filename):
    h  = hashlib.md5()
    b  = bytearray(128*1024)
    mv = memoryview(b)
    with open(filename, 'rb', buffering=0) as f:
        while n := f.readinto(mv):
            h.update(mv[:n])
    return h.hexdigest()

def search_path(filepath):
    print(f"Searching: {filepath}")
    if any(os.scandir(filepath)):
        for item in os.scandir(filepath):
            if item.is_dir():
                # if the element is a directory, call function recursively
                search_path(item.path)
            else:
                # Iterate over any files
                print(f"Checking: {item.name}")
                # Generate a hash per file
                filehash = get_hash(item.path)
                if filehash in duplicates:
                    duplicates[filehash].append(item.path)
                else:
                    duplicates[filehash]=[]
    elif args.delete:
        print(f"Removing empty directory: {filepath}")
        os.rmdir(filepath)
    
def check_duplicates():
    for key in duplicates:
        if duplicates[key] == []:
            duplicates.pop(key)

    with open('duplicates.json', 'w') as convert_file:
        convert_file.write(json.dumps(duplicates))

def main():
    search_path(args.filepath)
    check_duplicates()

if __name__ == "__main__":
  
    duplicates = {}
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath", required=True)
    parser.add_argument('-d', '--delete', action='store_true', help="Remove empty directories")
    args = parser.parse_args()
    main()