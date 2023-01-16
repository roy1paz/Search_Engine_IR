# Search_Engine_IR
Information retrieval project - A search engine project that utilizes Google Cloud Platform (GCP) services. It includes all necessary scripts and configurations for setting up a search index and querying it using GCP.<br />
In this project we need to retrieve documents ids based on a given query from the corpus of documents wididumps202108 which contains more than 6 million documents.<br /><br />
We use the search_frontend.py file which contains 5 functions to retrieve information:<br />

`search()`: This function retrieve up to a 100  documents ids from the most relevant documents in decent order according to a given query based on calculation of cosine similarity if the length of the tokenize query is bigger than 2 words or else returns documents ids with binary function that calculate the joint words from the query and the title doc.<br />

`search_body()`: This function retrieve up to a 100  documents ids from the most relevant documents in decent order according to a given query based only on the calculation of cosine similarity.<br />

`search_title()`: This function retrieve all the relevant documents ids from the most relevant documents in decent order according to a given query based on only binary function that calculate the joint words from the query and the title doc.<br />

`search_anchor()`: This function retrieve all the relevant documents ids from the most relevant documents in decent order according to a given query based on only binary function that calculate the joint words from the query and the title doc.<br />

`get_pagerank()`: This function retrieve the Page Rank of documents ids if exist from from a given documents ids.<br />

`get_pageview()`: This function retrieve the number of views of a given doc_id from the corpus.<br />

How to deploy the app:<br />
in order to operate this you need to open instance in GCP , and then copy the commands from the `run_frontend_in_gcp.sh` file which let you open an instance in GCP, after that you need to upload serval files: `inverted_index_gcp.py` , `search_frontend.py` and `backend_final.py`, and then you can run `search_frontend.py` in order to operate the all thing, after that you can test this with `test.ipynb` file and use the `new_train.json` file. 
