import os


# each of the files in data/skipped contains the file names of the images that were skipped
# combine all the skipped file names into one file from each of the files in data/skipped
if __name__ == "__main__":
    
    # get all the skipped file names
    skipped_file_names = os.listdir("data/skipped")
    # sort the file names
    skipped_file_names.sort()
    # get the file paths
    skipped_file_paths = [os.path.join("data/skipped", file_name) for file_name in skipped_file_names]
    # read the skipped file names
    skipped_file_names = [open(file_path, 'r').read().split("\n") for file_path in skipped_file_paths]
    # flatten the list of skipped file names
    skipped_file_names = [file_name for file_names in skipped_file_names for file_name in file_names]
    # remove empty strings
    skipped_file_names = [file_name for file_name in skipped_file_names if file_name != ""]
    # sort the file names
    skipped_file_names.sort()
    # write the skipped file names to a file
    with open("data/aaa_complete_list.txt", 'w') as f:
        f.write("\n".join(skipped_file_names))
