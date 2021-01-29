from flask import Flask
import job_portal_handler

app = Flask(__name__)

app.add_url_rule('/',view_func=job_portal_handler.home_page)

app.add_url_rule('/search/',
                 view_func=job_portal_handler.search, methods=['GET','POST'])

if __name__ == '__main__':
    app.run(debug=True)
    
# Run file and access the server from your browser
# http://127.0.0.1:5000/

# For search results after accessing server from browser
# http://127.0.0.1:5000/search/?query={query}
# eg. http://127.0.0.1:5000/search/?query=computer%20science