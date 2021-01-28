from flask import Flask
import handler1

app = Flask(__name__)

app.add_url_rule('/',view_func=handler1.home_page)

app.add_url_rule('/search/',
                 view_func=handler1.search, methods=['GET','POST'])

if __name__ == '__main__':
    app.run(debug=True)
    
# Access the server from your browser
# http://127.0.0.1:5000/

# For search results after accessing server from browser
# http://127.0.0.1:5000/search/?query={query}