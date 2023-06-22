import os
import shutil

def test_deleteLogsAndDownloads():
    delete_files_in_directory("..\\Logs\\")
    delete_files_in_directory("..\\OutputFiles\\")

def delete_files_in_directory(directory):
    # Iterate over the files and subdirectories in the directory
    for root, dirs, files in os.walk(directory):
        # Exclude the .gitkeep file from deletion
        if ".gitkeep" in files:
            files.remove(".gitkeep")
        
        # Delete all files in the current directory
        for file in files:
            file_path = os.path.join(root, file)
            os.remove(file_path)

        # Delete all subdirectories (including empty ones)
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            shutil.rmtree(dir_path)

        # Clear the subdirectories list to prevent further traversal
        dirs.clear()