import sys
import os.path
from stemmer import PorterStemmer


def scraped_data_files_paths(dir_path):
    files_path_list = []
    if not os.path.exists(dir_path):
        print("No folder named " + dir_path + " that contains scraped data files!")
        sys.exit()

    for root, _, files in os.walk(dir_path):
        for f in files:
            if f.startswith("D"):
                files_path_list.append(os.path.join(root[len(dir_path) :], f))

    return files_path_list


def tokenization_and_punc_removal(content):
    content = content.replace("\\n", " ")
    content = content.replace("\\xa0", " ")
    content = content.replace("&amp", " ")
    content = content.replace("\\u200b", " ")
    content = content.replace("\\", "")

    new_content = ""
    for c in content:
        if c.isascii() and (c.isalpha() or c.isspace()):
            new_content += c.lower()
        else:
            new_content += " "
    while "  " in new_content:
        new_content = new_content.replace("  ", " ")

    return new_content


def stopword_removal(content):
    f = open(swfile, "r")
    while line := f.readline():
        line = " " + line.strip() + " "
        while line in content:
            content = content.replace(line, " ")

    f.close()
    return content


def stemming(content):
    p = PorterStemmer()
    words = content.split()
    new_content = ""
    for word in words:
        new_content += p.stem(word, 0, len(word) - 1) + " "

    return new_content


# Create a new folder for saving the fetched files and check whether the folder already exists. If the folder exists, the script will exit
def cleanup_and_create_folder(dirname):
    if os.path.exists(dirname):
        print("folder you specified already exists! Please remove it first")
        sys.exit()

    os.makedirs(dirname)


if len(sys.argv) != 4:
    print(
        "Please insert directory paths: python preprocessing.py <infolder> <outfolder> <stopwords file name>"
    )
    sys.exit()

infolder = sys.argv[1]
outfolder = sys.argv[2]
swfile = sys.argv[3]

cleanup_and_create_folder(outfolder)

for p in scraped_data_files_paths(infolder):
    f = open(infolder + "/" + p, "r")
    content = str(f.read())
    content = tokenization_and_punc_removal(content)
    content = stopword_removal(content)
    content = stemming(content)
    f.close()

    f = open(outfolder + "/" + p, "w")
    f.write(content)
    f.close()
