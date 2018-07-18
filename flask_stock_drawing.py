import sys, os
from flask import Flask, render_template
from flask import request
import glob
import pymysql.cursors
import re
import json

app = Flask(__name__)

def get_potential_stocks():
    with open('potential_stocks.json', encoding='utf8') as f:
        stock_potential_info = json.load(f)
    return stock_potential_info

@app.route('/', methods=['GET', 'POST'])
def user():
    png_files = []
    for png_file in glob.glob('static/stockDrawing_*.png'):
        stockcode = png_file.replace('\\', '/').replace('static/stockDrawing_', '').replace('.png', '')
        png_files.append({'stockcode':stockcode, 'filename':png_file.replace('\\', '/').replace('static/', '')})

    stock_potential_info = get_potential_stocks()

    png_files = sorted(png_files, key=lambda k: k['stockcode']) 
    return render_template('stock_drawing.html', re=re, png_files=png_files, stock_potential_info=stock_potential_info)

if __name__ == '__main__':
    app.debug = True
    app.run(host= '0.0.0.0')