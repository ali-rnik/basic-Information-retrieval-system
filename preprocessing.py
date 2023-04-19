import sys
import os.path
from stemmer import PorterStemmer
from scraping import ScrapeUtils


class Preprocessor:
    # function that allows you to change punctuation and special characters by spaces in the text passed as an argument
    def tokenization_and_punc_removal(self, content):
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

    # function that removes current words from the text passed as an argument
    def stopword_removal(self, content, swfile):
        f = open(swfile, "r")
        while line := f.readline():
            line = " " + line.strip() + " "
            while line in content:
                content = content.replace(line, " ")

        f.close()
        return content

    # Function that calls Porter's algorithm to perform the stemming on the text passed as an argument
    def stemming(self, content):
        p = PorterStemmer()
        words = content.split()
        new_content = ""
        for word in words:
            new_content += p.stem(word, 0, len(word) - 1) + " "

        return new_content

    def run(self, content, swfile):
        content = self.tokenization_and_punc_removal(content)
        content = self.stopword_removal(content, swfile)
        content = self.stemming(content)
        return content


def main(custom_args):
    if custom_args == None:
        infolder, outfolder, swfile = ScrapeUtils().parse_args(
            3, "python preprocessing.py <infolder> <outfolder> <stopwords file name>"
        )
    else:
        infolder, outfolder, swfile = custom_args
        

    files_paths = ScrapeUtils().dir_files_path(infolder)
    ScrapeUtils().create_dir(outfolder)

    for p in files_paths:
        infile = open(infolder + "/" + p, "r")
        content = str(infile.read())
        content = Preprocessor().run(content, swfile)
        infile.close()

        outfile = open(outfolder + "/" + p, "w")
        outfile.write(content)
        outfile.close()


if __name__ == "__main__":
    main()
