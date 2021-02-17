from flask import Flask
import job_portal_handler

app = Flask(__name__)
    
# http://127.0.0.1:5000/search/?query={keyword}
app.add_url_rule('/search/',
                 view_func=job_portal_handler.search, 
                 methods=['GET'])

# http://127.0.0.1:5000/resume/?id={userId}
app.add_url_rule('/resume/',
                 view_func=job_portal_handler.resume, 
                 methods=['GET'])

# http://127.0.0.1:5000/searchwithresume/?query={keyword}
app.add_url_rule('/searchwithresume/',
                 view_func=job_portal_handler.search_with_resume, 
                 methods=['GET'])

# http://127.0.0.1:5000/similarjobs/?jobid={jobId}
app.add_url_rule('/similarjobs/',
                 view_func=job_portal_handler.similar_jobs, 
                 methods=['GET'])

# http://127.0.0.1:5000/prefsurvey/?id={userId}
app.add_url_rule('/prefsurvey/',
                 view_func=job_portal_handler.pref_survey, 
                 methods=['GET'])

# http://127.0.0.1:5000/postjobs/
app.add_url_rule('/postjobs/',
                 view_func=job_portal_handler.post_jobs, 
                 methods=['POST'])

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)