import os
import re
import sys

def sanitize_filenames(directory):
    patterns = [
        re.compile(r"S(\d{2})\s*[xX×]\s*E(\d{2})", re.IGNORECASE),
        re.compile(r"EP-(\d{2})\s+.*?S(\d{1,2})", re.IGNORECASE),
        re.compile(r"S(\d{1,2})_Ep_(\d{2})", re.IGNORECASE),  # Matches format like S3_Ep_06
        re.compile(r"S(\d{1,2})\s*Ep[-_ ](\d{2})", re.IGNORECASE),  # Matches format like S3 Ep-01
        re.compile(r"S(\d{2})E(\d{2})", re.IGNORECASE)  # Matches format like S04E14
    ]
    
    for filename in os.listdir(directory):
        try:
            match = None
            for pattern in patterns:
                match = pattern.search(filename)
                if match:
                    break
            
            if match:
                season = match.group(1).zfill(2)
                episode = match.group(2).zfill(2)
                
                base, ext = os.path.splitext(filename)
                while '.' in base:
                    base, ext = os.path.splitext(base)
                
                new_name = f"S{season}E{episode}{ext}"
                
                old_path = os.path.join(directory, filename)
                new_path = os.path.join(directory, new_name)
                
                if old_path != new_path:
                    os.rename(old_path, new_path)
                    print(f"Renamed: {filename} -> {new_name}")
                else:
                    print(f"Skipped (already formatted): {filename}")
            else:
                print(f"Skipped (no match): {filename}")
        except Exception as e:
            print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python sanitize_filenames.py <directory>")
        sys.exit(1)
    
    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print("Error: Directory not found.")
        sys.exit(1)
    
    sanitize_filenames(directory)
