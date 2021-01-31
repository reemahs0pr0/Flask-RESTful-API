from flask import Flask
import job_portal_handler

app = Flask(__name__)

app.add_url_rule('/',view_func=job_portal_handler.home_page)

app.add_url_rule('/search/',
                 view_func=job_portal_handler.search, methods=['GET','POST'])

if __name__ == '__main__':
    app.run(debug=True)