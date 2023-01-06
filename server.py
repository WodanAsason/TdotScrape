from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
import scraping
import pandas as pd

app = Flask(__name__)

bootstrap = Bootstrap5(app)
scraper = scraping.Scraper()


@app.route('/')
def home():
    mtcc = scraper.read_csv('mtcc').to_dict(orient='records')
    sba = scraper.read_csv('sba').to_dict(orient='records')
    data = [mtcc, sba]
    return render_template('index.html', data=data)
