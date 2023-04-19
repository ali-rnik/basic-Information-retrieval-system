import sys
import os.path
import math
from scraping import ScrapeUtils


class TF_IDF:
    def parse_inverted_mat_file(self, infile):
        f = open(infile, "r")  # open the file in read mode
        # create 3 dictionaries
        freq_max = {}
        matrix = {}
        n = {}

        while line := f.readline():  # read each word from the input file
            words = line.split()  # the words read are put in a list
            cnt = 0
            term = ""
            if len(words) <= 0:
                return
            for word in words:  # iterate over each word in the list
                if (
                    cnt == 0
                ):  # if the word is counted for the first time then add the term to the dictionaries
                    term = word
                    matrix[term] = {}
                    n[term] = len(words) - 1

                else:  # if the word has already appeared update the dictionaries
                    chunk = word.split("[")
                    doc = chunk[0]
                    freq = chunk[1].strip("]")

                    if freq_max.get(doc) == None:
                        freq_max[doc] = 0
                    freq_max[doc] = max(freq_max[doc], int(freq))
                    matrix[term][doc] = int(freq)
                cnt += 1  # update counter
        f.close()

        return freq_max, matrix, n

    # calculate the TF-IDF weight for each term in a text file and store the results in an output file
    def cal_TF_IDF_and_write(self, outfile, freq_max, matrix, n):
        docs_list = []
        for k in freq_max.keys():
            docs_list.append((int(k.strip("D")), k))
        docs_list = sorted(docs_list)
        f = open(outfile, "a")
        f.write("{:<20}".format(""))
        for _, doc in docs_list:
            f.write(" " + "{:<5}".format(doc))
        f.write("\n")
        for term in n.keys():
            f.write("{:<20}".format(term) + " ")
            for _, doc in docs_list:
                if matrix[term].get(doc) == None:
                    matrix[term][doc] = 0

                N = len(docs_list)
                n_i = n[term]
                freq_ij = matrix[term][doc]
                max_freq_j = freq_max[doc]

                tf_ij = float(freq_ij) / max_freq_j
                idf_i = math.log(float(N) / n_i, 10)

                w_ij = round(tf_ij * idf_i, 3)
                f.write("{:<5}".format(w_ij) + " ")
            f.write("\n")


def main():
    infile, outfile = ScrapeUtils().parse_args(2, "python TF_IDF.py <infile> <outfile>")

    # check if input file exists
    ScrapeUtils().exit_on_file_missing(infile)

    # check if the output file exists
    ScrapeUtils().exit_on_file_existence(outfile)

    freq_max, matrix, n = TF_IDF().parse_inverted_mat_file(infile)
    TF_IDF().cal_TF_IDF_and_write(outfile, freq_max, matrix, n)

