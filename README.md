# About  
    This Project implements a complete pipeline of an Information Retrieval system.  
  Each step is implemented in a specefic file specified by its step name.  
  The IR system file is named after its applications and that is IR.py which runs all steps implemented.  

# Installation  
    You need Python interpreter to run this project, also I recommend to use virtualenv to install all necessary depencies by running:
```
    pip install -r requirements.txt
```
    Thats it. Now run all files step by step or use IR.py to run them at once.  

# Usage  
    You can see how you can run each script by only run it without any arugment:
```
    $ python <scriptname>
```
    Then you can see the number of arguments you should provide and then run it with argumets provided.  

    For Example to Scrape Griffith college university website you can run in the following order:
```
    $ python scraping.py scraped_folder 
    $ python preprocessing.py scraped_folder/ preprocced_folder/ stop_words_english.txt 
    $ python inverted_index.py preprocced_folder/ inverted_matrix  
    $ python TF_IDF.py inverted_matrix tf_idf_matrix  
```  
    
    By Having TF_IDF weights in tf_idf_matrix file, you can compare cosine similarity between two documents:
```  
    $ python cosine_similarity.py tf_idf_matrix  D1 D2
```  
    
    Or you can query in all scraped documents and find your query similarity:  
```  
    $ python IR.py preprocced_folder/ "college" stop_words_english.txt  
```    
    
