from flask import Flask
import pandas as pd
app = Flask(__name__)


@app.route('/')
def home():
    return "<h1>Temp</h1>"
