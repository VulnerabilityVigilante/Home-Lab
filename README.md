# Home-Lab Automation Scripts

This repository contains scripts designed for automating tasks within a Home-Lab environment.


## Repository Contents

### Scripts

#### `Files-Condense.sh`
- **Purpose:**  
  Automates the creation and maintenance of symbolic links between a source and target directory.
- **Features:**
  - Creates or updates symbolic links for all valid files in the source directory.
  - Removes duplicate symbolic links pointing to the same target.
  - Identifies and deletes broken symbolic links.
- **Usage:**
  ```bash
  ./Files-Condense.sh SourceDirectory TargetDirectory

 #### `Files-Unique.sh`
- **Purpose:**  
  Scans a directory for duplicate files based on their content and removes duplicates.
- **Features:**
  - Computes a SHA-256 hash for each file's content.
  - Retains one copy of each file while deleting duplicates.
- **Usage:**
  ```bash
  ./Files-Unique.sh ParentDirectory

## Suggested Crontab Setup:
#check for duplicates at 4am daily

0 4 * * * /bin/bash /path/to/Files-Unique.sh  /path/to/parent/directory


#condense into folder at 6am daily

0 6 * * * /bin/bash /path/to/Files-Condense.sh /path/to/source/directory /path/to/condensed/directory
