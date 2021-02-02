from flask import Flask
import job_portal_handler_prototype
from job_portal_handler_prototype import start

app = Flask(__name__)

app.add_url_rule('/resume/',
                 view_func=job_portal_handler_prototype.resume, 
                 methods=['GET','POST'])

app.add_url_rule('/search/',
                 view_func=job_portal_handler_prototype.search, 
                 methods=['GET','POST'])

app.add_url_rule('/searchwithresume/',
                 view_func=job_portal_handler_prototype.search_with_resume, 
                 methods=['GET','POST'])

if __name__ == '__main__':
    start()
    app.run(debug=True)