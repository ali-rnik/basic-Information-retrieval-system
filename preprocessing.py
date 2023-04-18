import sys
import os.path

def scraped_data_files_paths(dir_path):
    files_path_list = []
    if not os.path.exists(dir_path):
        print("No folder named "+ sys.argv[1] + " that contains scraped data files!")
        sys.exit()

    for root, _, files in os.walk(dir_path):
        for f in files:
            if f.startswith("D"):
                files_path_list.append(os.path.join( root[len(dir_path):], f ))

    return files_path_list

def tokenization_and_punc_removal(content):
    content = content.replace("\\n", " ")
    content = content.replace("\\xa0", " ")
    content = content.replace("&amp", " ")
    content = content.replace("\\u200b", " ")
    content = content.replace("\\", "")

    new_content = ""
    for c in content:
        if c.isascii() and (c.isalpha() or  c.isspace()):
            new_content += c.lower()
    while '  ' in new_content:
        new_content = new_content.replace('  ', ' ')

    return new_content

def stopword_removal(content):
    return content

def stemming(content):
    return content

if len(sys.argv) != 4:
    print("Please insert directory paths: python preprocessing.py <infolder> <outfolder> <stopwords file name>")

infolder = sys.argv[1]
outfolder = sys.argv[2]
swfolder = sys.argv[3]


for p in scraped_data_files_paths(infolder):
    f = open(infolder+"/"+p, "r")
    content = str(f.read())
    content = tokenization_and_punc_removal(content)
    content = stopword_removal(content)
    content = stemming(content)
    print(content)
    exit()



