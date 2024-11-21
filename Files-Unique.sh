#!/bin/bash

set -o errexit
set -o nounset
set -o pipefail

# Function to calculate hash for a file based on its contents
calculate_hash() {
    local file="$1"
    sha256sum "$file" | awk '{print $1}'
}

# Function to detect and remove duplicates based on content hashes
remove_duplicates() {
    local dir="$1"
    declare -A content_hashmap

    # Find all files recursively in the directory
    find "$dir" -type f -print0 | while IFS= read -r -d '' file; do
        printf "Processing file: %s\n" "$file"

        # Calculate the content hash
        local hash
        hash=$(calculate_hash "$file")

        # If the hash exists in the map, delete the duplicate
        if [[ -n "${content_hashmap[$hash]:-}" ]]; then
            printf "Duplicate detected:\n  - Keeping: %s\n  - Deleting: %s\n" "${content_hashmap[$hash]}" "$file"
            rm -f "$file"
        else
            # Otherwise, store the hash and the file path
            content_hashmap["$hash"]="$file"
        fi
    done

    printf "Duplicate removal completed in directory '%s'.\n" "$dir"
}

# Main function
main() {
    if [[ "$#" -ne 1 ]]; then
        printf "Usage: $0 ParentDirectory\n" >&2
        exit 1
    fi

    local parent_dir="$1"

    if [[ ! -d "$parent_dir" ]]; then
        printf "Error: '%s' is not a directory.\n" "$parent_dir" >&2
        return 1
    fi

    printf "Scanning directory '%s' for content-based duplicates...\n" "$parent_dir"
    remove_duplicates "$parent_dir"
    printf "Duplicate removal completed in '%s'.\n" "$parent_dir"
}

# Call main with all script arguments
main "$@"