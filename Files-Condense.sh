#!/bin/bash

set -o errexit
set -o nounset
set -o pipefail

# Check if the correct number of arguments is provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 SourceDirectory TargetDirectory"
    exit 1
fi

# Source and target directories
SOURCE_DIR="$1"
TARGET_DIR="$2"

# Function to create symbolic links for all valid files
create_or_update_links() {
    for file in "$SOURCE_DIR"/*; do
        if [ -f "$file" ]; then
            ln -sf "$(realpath "$file")" "$TARGET_DIR/$(basename "$file")"
        fi
    done
}

# Function to remove duplicate symbolic links
remove_duplicate_links() {
    printf "Removing duplicate symbolic links...\n"

    # Create a temporary file to track resolved file paths
    local temp_file
    temp_file=$(mktemp)

    # Loop through all symbolic links in the target directory
    find "$TARGET_DIR" -type l | while IFS= read -r symlink; do
        # Resolve the actual file path the link points to
        local target_file
        target_file=$(readlink -f "$symlink")

        # Check if the resolved file path is already in the temp file
        if grep -Fxq "$target_file" "$temp_file"; then
            printf "Duplicate link detected, removing: %s\n" "$symlink"
            rm -f "$symlink"
        else
            # Add the resolved file path to the temp file
            echo "$target_file" >> "$temp_file"
        fi
    done

    # Cleanup the temporary file
    rm -f "$temp_file"
}

# Function to remove broken symbolic links
remove_broken_links() {
    printf "Removing broken symbolic links...\n"

    # Find and remove all broken symbolic links in the target directory
    find "$TARGET_DIR" -xtype l -exec rm -f {} +
}

# Main function
main() {
    printf "Starting symbolic link maintenance...\n"

    # Step 1: Create or update symbolic links for source files
    create_or_update_links

    # Step 2: Remove duplicate symbolic links
    remove_duplicate_links

    # Step 3: Remove broken symbolic links
    remove_broken_links

    printf "Symbolic link maintenance completed.\n"
}

# Create target directory if it doesn't exist
mkdir -p "$TARGET_DIR"

# Run the main function
main