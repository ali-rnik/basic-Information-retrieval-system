import sys
import os.path
from scraping import ScrapeUtils

class InvertIndex:
    def invertindex_gen(self, files_paths, infolder):
        inverted_index_dict = {}
        for p in files_paths:
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
            f.close()
        return inverted_index_dict

    def save_mat(self, mat, outfilename):
        f = open(outfilename, "w")
        for word in mat:
            f.write('{:<15}'.format(word+" "))
            for doc in mat[word]:
                f.write('{:<10}'.format(doc + "[" + str(mat[word][doc]["count"]) + "]"+" "))

            f.write("\n")
        f.close()

def main(custom_args=None):

    if custom_args == None:   
        infolder, outfilename = ScrapeUtils().parse_args(
            2, "python inverted_index.py <infolder> <outfilename>"
        )
    else:
        infolder, outfilename = custom_args

    files_paths = ScrapeUtils().dir_files_path(infolder)
    inverted_index_dict = InvertIndex().invertindex_gen(files_paths, infolder)

    ScrapeUtils().exit_on_file_existence(outfilename)
    InvertIndex().save_mat(inverted_index_dict, outfilename)

if __name__ == "__main__":
    main()
