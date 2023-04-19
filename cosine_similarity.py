import sys
import os.path
import math
from scraping import ScrapeUtils


class CosineSim:
    def calculate_vec_length(self, matrix, doc):
        vec_length = 0
        for word in matrix.keys():
            vec_length += matrix[word][doc] ** 2
        return math.sqrt(float(vec_length))

    def dot_product(self, matrix, doc1, doc2):
        dot_product = 0
        for word in matrix.keys():
            dot_product += matrix[word][doc1] * matrix[word][doc2]
        return dot_product

    def cosine_sim(self, matrix, doc1, doc2):
        doc1_vlen = self.calculate_vec_length(matrix, doc1)
        doc2_vlen = self.calculate_vec_length(matrix, doc2)
        dp = self.dot_product(matrix, doc1, doc2)
        result = float(dp) / (doc1_vlen * doc2_vlen)
        return result

    def parse_tfidf_file(self, infile):
        f = open(infile, "r")
        matrix = {}
        first_row = True
        docs_list = {}

        while line := f.readline():
            words = line.split()
            cnt = 0
            term = ""
            if first_row:
                docs_list = words
                first_row = False
                continue

            for word in words:
                if cnt == 0:
                    term = word
                    matrix[term] = {}
                else:
                    matrix[term][docs_list[cnt - 1]] = float(word)

                cnt += 1
        f.close()

        return matrix


def main(custom_args):
    if custom_args == None:
        infile, first_doc, second_doc = ScrapeUtils().parse_args(
            3, "python cosine_similarity.py <infile> D1 D2"
        )
    else:
        infile, first_doc, second_doc = custom_args

    ScrapeUtils().exit_on_file_missing(infile)
    matrix = CosineSim().parse_tfidf_file(infile)

    sim = CosineSim().cosine_sim(matrix, first_doc, second_doc)
    print(sim)
    return sim


if __name__ == "__main__":
    main()
