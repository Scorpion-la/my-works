#-------------------------------------------------------------------------------
# Name:        File_Organiser
# Purpose:     A program to sort all your files
#
# Author:      ADITYA
#
# Created:     22/02/2025
# Copyright:   (c) ADITYA 2025
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os
import shutil

# Define categories and their corresponding file extensions
CATEGORIES = {
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx"],
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
    "Videos": [".mp4", ".mov", ".avi", ".mkv"],
    "Music": [".mp3", ".wav", ".flac"],
    "Archives": [".zip", ".rar", ".tar", ".gz"],
    "Code": [".py", ".js", ".html", ".css", ".java"],
    "Others": []  # Default category for unmatched files
}
def create_folders(base_path):
    """Create folders for each category if they don't exist."""
    for category in CATEGORIES:
        folder_path = os.path.join(base_path, category)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
def sort_files_by_extension(source_path):
    """Sort files into folders based on their extensions."""
    for filename in os.listdir(source_path):
        file_path = os.path.join(source_path, filename)

        # Skip directories
        if os.path.isdir(file_path):
            continue

        # Get file extension
        _, file_extension = os.path.splitext(filename)
        file_extension = file_extension.lower()

        # Find the category for the file
        moved = False
        for category, extensions in CATEGORIES.items():
            if file_extension in extensions:
                destination_folder = os.path.join(source_path, category)
                shutil.move(file_path, os.path.join(destination_folder, filename))
                print(f"Moved {filename} to {category}")
                moved = True
                break

        # If no category matches, move to 'Others'
        if not moved:
            destination_folder = os.path.join(source_path, "Others")
            shutil.move(file_path, os.path.join(destination_folder, filename))
            print(f"Moved {filename} to Others")
def sort_files_by_keywords(source_path, keyword_rules):
    """Sort files into folders based on keywords in their filenames."""
    for filename in os.listdir(source_path):
        file_path = os.path.join(source_path, filename)

        # Skip directories
        if os.path.isdir(file_path):
            continue

        # Check for keywords
        for keyword, folder_name in keyword_rules.items():
            if keyword.lower() in filename.lower():
                destination_folder = os.path.join(source_path, folder_name)
                if not os.path.exists(destination_folder):
                    os.makedirs(destination_folder)
                shutil.move(file_path, os.path.join(destination_folder, filename))
                print(f"Moved {filename} to {folder_name} (Keyword: {keyword})")
                break
def main():
    # Set the source directory (current directory in this example)
    source_path = os.getcwd()

    # Create folders for each category
    create_folders(source_path)

    # Sort files by extensions
    sort_files_by_extension(source_path)

    # Sort files by keywords (optional)
    keyword_rules = {
        "invoice": "Invoices",
        "report": "Reports",
        "photo": "Personal_Photos"
    }
    sort_files_by_keywords(source_path, keyword_rules)

if __name__ == "__main__":
    main()