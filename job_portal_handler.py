import nltk
import string
import pandas as pd
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask import request

def home_page():
    # global df
    # df = pd.read_csv('fullmonsters.csv')
    
    ##### to read dataset from MySQL #####
    from sqlalchemy import create_engine
    
    sqlEngine = create_engine('mysql+pymysql://root:<password>@localhost:3306/<schema>')
    with sqlEngine.connect() as conn, conn.begin():
        df = pd.read_sql_table('<table name>', conn);
    
    df['corpus'] = df['Job Title'] + ' ' + df['Job Description'] + ' ' + \
        df['Skills'].astype(str)
    
    corpus = df['corpus'].values
    
    global stop_words 
    stop_words = stopwords.words('english') 
    
    global lm 
    lm = nltk.stem.WordNetLemmatizer()
    
    docs = []
    global punc 
    punc = str.maketrans('','', string.punctuation)
    for doc in corpus:
        doc_no_punc = doc.translate(punc)
        words_lemmatized = [lm.lemmatize(w) for w in doc_no_punc.\
                            lower().split() if not w in stop_words]
        docs += [' '.join(words_lemmatized)]
    
    global tfidf_vec
    tfidf_vec = TfidfVectorizer(ngram_range=(1,1))
    tfidf_vec.fit(docs)
    
    global tfidf_wm
    tfidf_wm = tfidf_vec.transform(docs).toarray()
        
    features = tfidf_vec.get_feature_names()
    indexes = ['Job '+ str(i) for i in range(len(corpus))]
    
    global tfidf_df
    tfidf_df = pd.DataFrame(data=tfidf_wm, index=indexes, columns=features)
    
    with sqlEngine.connect() as conn, conn.begin():
        df_user = pd.read_sql_table("user", conn);
        
    user_id =  request.args.get('id')
    path = df_user.iloc[int(user_id)-1]['Path']
    
    if path.endswith('.pdf'):
        from tika import parser   
        parsed_pdf = parser.from_file(path) 
        resume_doc = parsed_pdf['content']
    else:
        from docx import Document
        doc = Document(path)
        fullText = []
        for para in doc.paragraphs:
            fullText.append(para.text)
        resume_doc = '\n'.join(fullText)
    
    query = resume_doc
    query = query.translate(punc)
    query_arr = [' '.join([lm.lemmatize(w) for w in query.lower().\
                           split()if not w in stop_words])]
    
    tfidf_wm2 = tfidf_vec.transform(query_arr).toarray()
    
    docs_similarity = cosine_similarity(tfidf_wm2, tfidf_wm)
    
    global query_similarity
    query_similarity = docs_similarity[0]
    
    series = pd.Series(query_similarity, index=tfidf_df.index)
    sorted_series = series.sort_values(ascending=False)
    sorted_series = sorted_series[sorted_series!=0]
    # print(sorted_series)
    
    ##### for Java GET request #####
    result = ""
    for index in sorted_series.index:
        result += index[4:] + ","
    
    return result
    
    # i = 0
    # df_result = pd.DataFrame(columns=['Job Title', 'Company Name', \
    #                                   'Job Description', 'Skills', 'Job Link'])
                             
    # for index in sorted_series.index:
    #     doc_idx = int(index[4:])
    #     df_result.loc[i] = df.loc[doc_idx]
    #     i += 1
     
    ##### for HTML result #####
    # return df_result.to_html()

    ##### for REST API calls #####
    # return df_result.to_json(orient="records")

def search():
    search =  request.args.get('query')
    search = search.translate(punc)
    search_arr = [' '.join([lm.lemmatize(w) for w in search.lower().\
                            split()if not w in stop_words])]
    
    tfidf_search = tfidf_vec.transform(search_arr).toarray()
    
    docs_similarity_search = cosine_similarity(tfidf_search, tfidf_wm)
    query_similarity_search = docs_similarity_search[0]
    
    series_weighted_search = pd.Series(query_similarity_search*(2/3) + \
                                       query_similarity*(1/3), \
                                           index=tfidf_df.index)
    sorted_series_weighted_search = series_weighted_search.\
        sort_values(ascending=False)
    sorted_series_weighted_search = sorted_series_weighted_search\
        [sorted_series_weighted_search!=0]
    # print(sorted_series_weighted_search)
    
    ##### for Java GET request #####
    result = ""
    for index in sorted_series_weighted_search.index:
        result += index[4:] + ","
    
    return result
    
    # i = 0
    # df_result_weighted_search = \
    #     pd.DataFrame(columns=['Job Title', 'Company Name', 'Job Description', \
    #                           'Skills', 'Job Link'])
                             
    # for index in sorted_series_weighted_search.index:
    #     doc_idx = int(index[4:])
    #     df_result_weighted_search.loc[i] = df.loc[doc_idx]
    #     i += 1
    
    ##### for HTML result #####
    # return df_result_weighted_search.to_html()

    ##### for REST API calls #####
    # return df_result_weighted_search.to_json(orient="records")