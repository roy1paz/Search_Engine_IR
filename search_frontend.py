from flask import Flask, request, jsonify
from backend_final import *

class MyFlaskApp(Flask):
    def run(self, host=None, port=None, debug=None, **options):
        super(MyFlaskApp, self).run(host=host, port=port, debug=debug, **options)

app = MyFlaskApp(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False


@app.route("/search")
def search():
    ''' Returns up to a 100 of your best search results for the query. This is 
        the place to put forward your best search engine, and you are free to
        implement the retrieval whoever you'd like within the bound of the 
        project requirements (efficiency, quality, etc.). That means it is up to
        you to decide on whether to use stemming, remove stopwords, use 
        PageRank, query expansion, etc.

        To issue a query navigate to a URL like:
         http://YOUR_SERVER_DOMAIN/search?query=hello+world
        where YOUR_SERVER_DOMAIN is something like XXXX-XX-XX-XX-XX.ngrok.io
        if you're using ngrok on Colab or your external IP on GCP.
    Returns:
    --------
        list of up to 100 search results, ordered from best to worst where each 
        element is a tuple (wiki_id, title).
    '''
    res = []
    query = request.args.get('query', '')
    if len(query) == 0:
      return jsonify(res)
    # BEGIN SOLUTION
    # Query handling
    # word 2 vec
    query_for_word_to_vec = tokenize_word2vec(query)
    flag = 0
    if len(query_for_word_to_vec) <= 2 and query_for_word_to_vec != []:
        for token in query_for_word_to_vec:
            try:
                wiki_word2vec[token]
            except:
                flag = 1
        if flag == 0:
            terms_to_add = wiki_word2vec.most_similar(positive=query_for_word_to_vec, topn=10)
            for t in terms_to_add:
                if t[1] >= 0.89:
                    query += f' {t[0]}'
                else:
                    break

    queries_dict = {0: query}
    queries_data_not_binary = {k: tokenize(v) for k, v in queries_dict.items() if len(tokenize(v)) != 0}
    queries_data_binary = {k: tokenize_bin(v) for k, v in queries_dict.items() if len(tokenize_bin(v)) != 0}

    if len(queries_data_not_binary[0]) <= 2:
        title_result = {k: v for k, v in
                        search_binary(queries_data_binary[0], idx_title, bucket_name='title_bucket_roy_dudi')[:10]}
        merge_result = title_result
    else:
        body_result = fast_super_duper_cosine_main(queries_data_not_binary[0], idx_body,
                                                   bucket_name='body_bucket_roy_dudi')
        merge_result = body_result

    res = get_id_name_list_dict(merge_result, doc_title_pairs_dict)
    # END SOLUTION
    return jsonify(res)


@app.route("/search_body")
def search_body():
    ''' Returns up to a 100 search results for the query using TFIDF AND COSINE
        SIMILARITY OF THE BODY OF ARTICLES ONLY. DO NOT use stemming. DO USE the 
        staff-provided tokenizer from Assignment 3 (GCP part) to do the 
        tokenization and remove stopwords. 

        To issue a query navigate to a URL like:
         http://YOUR_SERVER_DOMAIN/search_body?query=hello+world
        where YOUR_SERVER_DOMAIN is something like XXXX-XX-XX-XX-XX.ngrok.io
        if you're using ngrok on Colab or your external IP on GCP.
    Returns:
    --------
        list of up to 100 search results, ordered from best to worst where each 
        element is a tuple (wiki_id, title).
    '''
    res = []
    query = request.args.get('query', '')
    if len(query) == 0:
      return jsonify(res)
    # BEGIN SOLUTION
    # word 2 vec
    query_for_word_to_vec = tokenize_word2vec(query)
    flag = 0
    if len(query_for_word_to_vec) <= 2 and query_for_word_to_vec != []:
        for token in query_for_word_to_vec:
            try:
                wiki_word2vec[token]
            except:
                flag = 1
        if flag == 0:
            terms_to_add = wiki_word2vec.most_similar(positive=query_for_word_to_vec, topn=10)
            for t in terms_to_add:
                if t[1] >= 0.89:
                    query += f' {t[0]}'
                else:
                    break

    queries_dict = {0: query}
    queries_data = {k: tokenize(v) for k, v in queries_dict.items() if len(tokenize(v)) != 0}
    query = queries_data[0]
    # calc cosine sim
    body_result = fast_super_duper_cosine_main(query, idx_body, bucket_name="body_bucket_roy_dudi")
    # END SOLUTION
    res = get_id_name_list_dict(body_result, doc_title_pairs_dict)
    return jsonify(res)


@app.route("/search_title")
def search_title():
    ''' Returns ALL (not just top 100) search results that contain A QUERY WORD 
        IN THE TITLE of articles, ordered in descending order of the NUMBER OF 
        QUERY WORDS that appear in the title. For example, a document with a 
        title that matches two of the query words will be ranked before a 
        document with a title that matches only one query term. 

        Test this by navigating to the a URL like:
         http://YOUR_SERVER_DOMAIN/search_title?query=hello+world
        where YOUR_SERVER_DOMAIN is something like XXXX-XX-XX-XX-XX.ngrok.io
        if you're using ngrok on Colab or your external IP on GCP.
    Returns:
    --------
        list of ALL (not just top 100) search results, ordered from best to 
        worst where each element is a tuple (wiki_id, title).
    '''
    res = []
    query = request.args.get('query', '')
    if len(query) == 0:
      return jsonify(res)
    # BEGIN SOLUTION
    # Query handling
    # word 2 vec
    query_for_word_to_vec = tokenize_word2vec(query)
    flag = 0
    if len(query_for_word_to_vec) <= 2 and query_for_word_to_vec != []:
        for token in query_for_word_to_vec:
            try:
                wiki_word2vec[token]
            except:
                flag = 1
        if flag == 0:
            terms_to_add = wiki_word2vec.most_similar(positive=query_for_word_to_vec, topn=10)
            for t in terms_to_add:
                if t[1] >= 0.89:
                    query += f' {t[0]}'
                else:
                    break

    queries_dict = {0: query}
    queries_data = {k: tokenize_bin(v) for k, v in queries_dict.items() if len(tokenize_bin(v)) != 0}
    query = queries_data[0]
    # calc
    bucket_name = 'title_bucket_roy_dudi'
    tite_result = search_binary(query, idx_title, bucket_name)
    # get names and ids
    res = get_id_name_list(tite_result, doc_title_pairs_dict)
    # END SOLUTION
    return jsonify(res)


@app.route("/search_anchor")
def search_anchor():
    ''' Returns ALL (not just top 100) search results that contain A QUERY WORD 
        IN THE ANCHOR TEXT of articles, ordered in descending order of the 
        NUMBER OF QUERY WORDS that appear in anchor text linking to the page. 
        For example, a document with a anchor text that matches two of the 
        query words will be ranked before a document with anchor text that 
        matches only one query term. 

        Test this by navigating to the a URL like:
         http://YOUR_SERVER_DOMAIN/search_anchor?query=hello+world
        where YOUR_SERVER_DOMAIN is something like XXXX-XX-XX-XX-XX.ngrok.io
        if you're using ngrok on Colab or your external IP on GCP.
    Returns:
    --------
        list of ALL (not just top 100) search results, ordered from best to 
        worst where each element is a tuple (wiki_id, title).
    '''
    res = []
    query = request.args.get('query', '')
    if len(query) == 0:
      return jsonify(res)
    # BEGIN SOLUTION
    # Query handling
    # word 2 vec
    query_for_word_to_vec = tokenize_word2vec(query)
    flag = 0
    if len(query_for_word_to_vec) <= 2 and query_for_word_to_vec != []:
        for token in query_for_word_to_vec:
            try:
                wiki_word2vec[token]
            except:
                flag = 1
        if flag == 0:
            terms_to_add = wiki_word2vec.most_similar(positive=query_for_word_to_vec, topn=10)
            for t in terms_to_add:
                if t[1] >= 0.89:
                    query += f' {t[0]}'
                else:
                    break

    queries_dict = {0: query}
    # tokenize query
    queries_data = {k: tokenize_bin(v) for k, v in queries_dict.items() if len(tokenize_bin(v)) != 0}
    query = queries_data[0]
    # calc sim
    bucket_name = "anchor_bucket_roy_dudi"
    anchor_result = search_binary(query, idx_anchor, bucket_name)
    res = get_id_name_list(anchor_result, doc_title_pairs_dict)
    # END SOLUTION
    return jsonify(res)


@app.route("/get_pagerank", methods=['POST'])
def get_pagerank():
    ''' Returns PageRank values for a list of provided wiki article IDs. 

        Test this by issuing a POST request to a URL like:
          http://YOUR_SERVER_DOMAIN/get_pagerank
        with a json payload of the list of article ids. In python do:
          import requests
          requests.post('http://YOUR_SERVER_DOMAIN/get_pagerank', json=[1,5,8])
        As before YOUR_SERVER_DOMAIN is something like XXXX-XX-XX-XX-XX.ngrok.io
        if you're using ngrok on Colab or your external IP on GCP.
    Returns:
    --------
        list of floats:
          list of PageRank scores that correrspond to the provided article IDs.
    '''
    res = []
    wiki_ids = request.get_json()
    if len(wiki_ids) == 0:
        return jsonify(res)
    # BEGIN SOLUTION
    res = [page_rank_dict[i] if i in page_rank_dict.keys() else 0 for i in wiki_ids]
    # END SOLUTION
    return jsonify(res)


@app.route("/get_pageview", methods=['POST'])
def get_pageview():
    ''' Returns the number of page views that each of the provide wiki articles
        had in August 2021.

        Test this by issuing a POST request to a URL like:
          http://YOUR_SERVER_DOMAIN/get_pageview
        with a json payload of the list of article ids. In python do:
          import requests
          requests.post('http://YOUR_SERVER_DOMAIN/get_pageview', json=[1,5,8])
        As before YOUR_SERVER_DOMAIN is something like XXXX-XX-XX-XX-XX.ngrok.io
        if you're using ngrok on Colab or your external IP on GCP.
    Returns:
    --------
        list of ints:
          list of page view numbers from August 2021 that correrspond to the 
          provided list article IDs.
    '''
    res = []
    wiki_ids = request.get_json()
    if len(wiki_ids) == 0:
        return jsonify(res)
    # BEGIN SOLUTION
    res = [page_views_dict[i] if i in page_views_dict.keys() else 0 for i in wiki_ids]
    # END SOLUTION
    return jsonify(res)


if __name__ == '__main__':
    # key: 2Js4bbloJxtIYNCo3zGSIYZCln8_wgetpiwb6zxbAikSSwWH
    # run the Flask RESTful API, make the server publicly available (host='0.0.0.0') on port 8080
    app.run(host='0.0.0.0', port=8080, debug=True)
