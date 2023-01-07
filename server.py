from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
import scraping
import pandas as pd
from pprint import pprint

app = Flask(__name__)

bootstrap = Bootstrap5(app)
scraper = scraping.Scraper()


@app.route('/')
def home():
    data = {'MTCC': scraper.read_csv('mtcc').to_dict(orient='records'),
            'SBA': scraper.read_csv('sba').to_dict(orient='records'),
            'NPS': scraper.read_csv('nps').to_dict(orient='records')}

    return render_template('index.html', data=data)
