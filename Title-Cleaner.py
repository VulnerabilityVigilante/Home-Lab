#!/usr/bin/env python3
import os
import re
import sys

def sanitize_filenames(directory):
    # Compile regex to search for SxxExx (case-insensitive)
    pattern = re.compile(r'(S\d{2}E\d{2})', re.IGNORECASE)
    
    # Check if the provided directory exists
    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a valid directory.")
        return
    
    # Iterate over all files in the directory
    for filename in os.listdir(directory):
        old_path = os.path.join(directory, filename)
        # Skip if it's not a file
        if not os.path.isfile(old_path):
            continue
        
        # Search for the SxxExx pattern in the file name
        match = pattern.search(filename)
        if match:
            episode_code = match.group(1).upper()  # Convert to uppercase (e.g., S01E01)
            # Preserve the original file extension
            _, ext = os.path.splitext(filename)
            new_filename = episode_code + ext
            new_path = os.path.join(directory, new_filename)
            
            try:
                os.rename(old_path, new_path)
                print(f"Renamed: {filename} -> {new_filename}")
            except Exception as e:
                print(f"Failed to rename {filename}: {e}")
        else:
            print(f"Pattern not found in: {filename}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python sanitize_filenames.py <directory>")
        sys.exit(1)
    
    input_directory = sys.argv[1]
    sanitize_filenames(input_directory)
