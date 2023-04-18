import sys
import os.path


def preprocessed_files_paths(dir_path):
    files_path_list = []
    if not os.path.exists(dir_path):
        print("No folder named " + dir_path + " that contains scraped data files!")
        sys.exit()

    for root, _, files in os.walk(dir_path):
        for f in files:
            if f.startswith("D"):
                files_path_list.append(os.path.join(root[len(dir_path) :], f))

    return files_path_list


if len(sys.argv) != 3:
    print("Please check arguments: python inverted_index.py <infolder> <outfilename>")
    sys.exit()

infolder = sys.argv[1]
inv_ind_file = sys.argv[2]

if os.path.isfile(inv_ind_file):
    print("Choose another file name for Inverted Index file.")
    sys.exit()

inverted_index_dict = {}
for p in preprocessed_files_paths(infolder):
    doc_dict = {}
    f = open(infolder + "/" + p, "r")
    content = str(f.read()).split()
    loc = 0

    for word in content:
        if inverted_index_dict.get(word) == None:
            inverted_index_dict[word] = {}
            inverted_index_dict[word][p] = {}
            inverted_index_dict[word][p]["index"] = []
            inverted_index_dict[word][p]["count"] = 0
        if inverted_index_dict.get(word).get(p) == None:
            inverted_index_dict[word][p] = {}
            inverted_index_dict[word][p]["index"] = []
            inverted_index_dict[word][p]["count"] = 0
        inverted_index_dict[word][p]["index"].append(loc)
        inverted_index_dict[word][p]["count"] = len(
            inverted_index_dict[word][p]["index"]
        )
        loc += 1


# print(inverted_index_dict)

f = open(inv_ind_file, "a")
for word in inverted_index_dict:
    f.write(word + "\t")
    for doc in inverted_index_dict[word]:
        f.write(doc + "[" + str(inverted_index_dict[word][doc]["count"]) + "] \t")

    f.write("\n")
f.close()
