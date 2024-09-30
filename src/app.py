# Import backend methods
from backend.custom_crawler import CustomCrawler
from backend.requests_functions import getRequest
from backend.filter_functions import applyFilter

# Import libraries
from flask import Flask, request, render_template, redirect, url_for, session
from cachelib.file import FileSystemCache
from datetime import datetime
from flask_session import Session
import secrets
import os

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
SESSION_TYPE = 'cachelib'
SESSION_SERIALIZATION_FORMAT = 'json'
SESSION_CACHELIB = FileSystemCache(cache_dir = f"{os.path.dirname(__file__)}/tmp/", threshold = 100, default_timeout = 600)
app.config.from_object(__name__)
Session(app)

crawler = CustomCrawler()

@app.route("/")
def init():
    return redirect(url_for('home'))

@app.route('/home/', methods=['GET'])
def home():
    return render_template('index.html')
    
@app.route('/download/', methods=['GET'])
def download():
    if request.method == 'GET':
        date = datetime.now().isoformat()
        requestResponse = getRequest('https://news.ycombinator.com/')
        if isinstance(request, str):
            return f"Unable to get data: {requestResponse}"
        crawler.parseHTML(requestResponse.content)
        resultsArray = crawler.getArrayResults()
        if not isinstance(resultsArray, list):
            return f"Unable to parse data"
        return {'crawl_data' : resultsArray, 'crawl_date' : date}
    
@app.route('/filter/', methods=['GET'])
def filter():
    if request.method == 'GET':
        filter_parameters = request.args
        resultsArray = crawler.getArrayResults()
        option_to_filter = filter_parameters.get("filter_option")
        if option_to_filter is None:
            return "Unable to filter data, no option selected"
        return applyFilter(resultsArray, int(option_to_filter))
    
@app.route('/save/', methods=['POST'])
def save():
    if request.method == 'POST':
        post_parameters = request.args
        post_body = request.json
        date = post_parameters.get('date')
        filter = post_parameters.get('filter_option')
        id = f"{date[:16]}_{filter}"
        if session.get(id) != None:
            return 'Data was already cached'
        else:
            cache_data = {'data' : post_body,
                        'date' : date,
                        'filter' : filter}
            session[id] = cache_data
            return 'Data saved in cache'

@app.route('/display/', methods=['GET'])
def display():
    if request.method == 'GET':
        cached_data = []
        for k, v in session.items():
            if k != '_permanent':
                cached_data.append(v)
        if len(cached_data) == 0:
            return 'No data in cache'
        return cached_data