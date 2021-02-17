import nltk
import string
import pandas as pd
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask import request
from csv_to_mysql import insert_jobs
from graphs_to_mysql import generate_graphs

def start():
    insert_jobs()
    from sqlalchemy import create_engine
    
    global sqlEngine, df
    sqlEngine = create_engine('mysql+pymysql://root:password@localhost:3306/jinder')
    with sqlEngine.connect() as conn, conn.begin():
        df = pd.read_sql_table('jobs', conn);
    
    df['corpus'] = df['jobTitle'] + ' ' + df['jobDescription'] + ' ' + \
        df['skills'].astype(str) + ' ' + df['companyName']
    
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
    
    sorted_df = pd.DataFrame(data = docs, columns=["col"])
    generate_graphs(sorted_df)

def search(): 
    if request.headers['Authorization'] == 'Jinder':
        search =  request.args.get('query')
        search = search.replace('+', ' ')
        search = search.translate(punc)
        search_arr = [' '.join([lm.lemmatize(w) for w in search.lower().\
                                split()if not w in stop_words])]
        
        tfidf_search = tfidf_vec.transform(search_arr).toarray()
        
        docs_similarity_search = cosine_similarity(tfidf_search, tfidf_wm)
        query_similarity_search = docs_similarity_search[0]
        
        series_weighted_search = pd.Series(query_similarity_search, \
                                               index=tfidf_df.index)
        sorted_series_weighted_search = series_weighted_search.\
            sort_values(ascending=False)
        sorted_series_weighted_search = sorted_series_weighted_search\
            [sorted_series_weighted_search!=0]
        
        result = ""
        for index in sorted_series_weighted_search.index:
            result += index[4:] + ","
        
        return result
    
def resume():    
    if request.headers['Authorization'] == 'Jinder':
        with sqlEngine.connect() as conn, conn.begin():
            df_user = pd.read_sql_table("jobseeker", conn);
            
        user_id =  request.args.get('id')
        path = df_user.iloc[int(user_id)-1]['resumeUrl']
        
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
    
        result = ""
        for index in sorted_series.index:
            result += index[4:] + ","
        
        return result

def search_with_resume():
    if request.headers['Authorization'] == 'Jinder':
        search =  request.args.get('query')
        search = search.replace('+', ' ')
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
        
        result = ""
        for index in sorted_series_weighted_search.index:
            result += index[4:] + ","
        
        return result

def similar_jobs():
    if request.headers['Authorization'] == 'Jinder':
        job_id = request.args.get('jobid')
        job_details = df.iloc[int(job_id)]['corpus']
        job_details = job_details.translate(punc)
        job_details_arr = [' '.join([lm.lemmatize(w) for w in job_details.lower().\
                                split()if not w in stop_words])]
        
        tfidf_job_match = tfidf_vec.transform(job_details_arr).toarray()
        
        docs_similarity_job_match = cosine_similarity(tfidf_job_match, tfidf_wm)
        query_similarity_job_match = docs_similarity_job_match[0]
        
        series_job_match = pd.Series(query_similarity_job_match, \
                                               index=tfidf_df.index)
        sorted_series_job_match = series_job_match.sort_values(ascending=False)
        sorted_series_job_match = sorted_series_job_match[1:11]
        
        result = ""
        for index in sorted_series_job_match.index:
            result += index[4:] + ","
        
        return result

def pref_survey():
    if request.headers['Authorization'] == 'Jinder':
        with sqlEngine.connect() as conn, conn.begin():
            df_pref = pd.read_sql_table("user_preference", conn);
            df_pref_job_title = pd.read_sql_table("user_preference_preferredjobtitle", \
                                                  conn);
            df_pref_job_role = pd.read_sql_table("user_preference_preferredjobrole", \
                                                 conn);
                
        user_id =  request.args.get('id')
        
        preferred_tech = df_pref[df_pref['user_id']==int(user_id)]\
            ['preferredTechnologies']
        preferred_tech = preferred_tech.values[0]
        preferred_tech = ' '.join(preferred_tech.split(','))
        
        pref_id = df_pref[df_pref['user_id']==int(user_id)]['id']
        pref_id = pref_id.values[0]
        
        preferred_job_title = ' '.join(df_pref_job_title[df_pref_job_title\
                                                         ['User_Preference_id']==pref_id]\
                                       ['preferredJobTitle'].values)
        preferred_job_role = ' '.join(df_pref_job_role[df_pref_job_role\
                                                       ['User_Preference_id']==pref_id]\
                                      ['preferredJobRole'].values)
        
        pref_doc = preferred_tech + ' ' + preferred_job_title + ' ' + preferred_job_role
        pref_doc = pref_doc.translate(punc)
        pref_doc_arr = [' '.join([lm.lemmatize(w) for w in pref_doc.lower().\
                                split()if not w in stop_words])]
        
        tfidf_pref = tfidf_vec.transform(pref_doc_arr).toarray()
        
        docs_similarity_pref = cosine_similarity(tfidf_pref, tfidf_wm)
        query_similarity_pref = docs_similarity_pref[0]
        
        series_pref = pd.Series(query_similarity_pref, \
                                               index=tfidf_df.index)
        sorted_series_pref = series_pref.sort_values(ascending=False)
        sorted_series_pref = sorted_series_pref[:20]
        
        result = ""
        for index in sorted_series_pref.index:
            result += index[4:] + ","
        
        return result

def post_jobs():
    if request.headers['Authorization'] == 'Jinder':
        start()
        return "200 OK"