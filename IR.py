import scraping, preprocessing, inverted_index, TF_IDF, cosine_similarity

def query_as_doc_injection(dirname, query_string):
    f = open(dirname+"/QUERY", "w")
    f.write(query_string)
    f.close()


def main():
    folder_name, query, stopword_file = scraping.ScrapeUtils().parse_args(
        3, "python IR.py <folder_name> <query sentence> <stopwords file>"
    )

    preprocessing_outfolder = "preprocessing_outfolder.tmp"
    inverted_index_outfile = "inverted_index_outfile.tmp"
    tf_idf_outfile = "tf_idf_outfile.tmp"

    open(inverted_index_outfile, "w").close()
    open(tf_idf_outfile, "w").close()

    query_as_doc_injection(folder_name, str(query))

    preprocessing.main([folder_name, preprocessing_outfolder, stopword_file])
    inverted_index.main([preprocessing_outfolder, inverted_index_outfile])

    docnames = TF_IDF.main([inverted_index_outfile, tf_idf_outfile])

    result = []
    for docname in docnames.keys():
        if docname != "QUERY":
            result.append((docname, cosine_similarity.main([tf_idf_outfile, "QUERY", docname])))

    result = sorted(result, key=lambda tup: tup[1], reverse=True)

    for elem in result:
        print("{:<4}".format(elem[0]), " ", "{:<4}".format(elem[1]))
    


if __name__ == "__main__":
    main()
