import sys
import os.path
import math

if len(sys.argv) != 4:
    print("Please check arguments: python cosine_similarity.py <infile> D1 D2")
    sys.exit()

infile = sys.argv[1]
first_doc = sys.argv[2]
second_doc = sys.argv[3]


def calculate_vec_length(matrix, doc):
    vec_length = 0
    for word in matrix.keys():
        vec_length += matrix[word][doc] ** 2
    return math.sqrt(float(vec_length))


def dot_product(matrix, doc1, doc2):
    dot_product = 0
    for word in matrix.keys():
        dot_product += matrix[word][doc1] * matrix[word][doc2]
    return dot_product

def cosine_sim(matrix, doc1, doc2):
    doc1_vlen = calculate_vec_length(matrix, doc1)
    doc2_vlen = calculate_vec_length(matrix, doc2)
    dp = dot_product(matrix, doc1, doc2)
    result = float(dp)/(doc1_vlen*doc2_vlen)
    return result

if not os.path.isfile(infile):
    print("Please select a file that is exist.")
    sys.exit()

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

print(cosine_sim(matrix, first_doc, second_doc))