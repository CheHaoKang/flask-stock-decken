import sys, os
from flask import Flask, render_template
from flask import request
import glob
import pymysql.cursors
import re

app = Flask(__name__)

def get_potential_stocks():
    try:
        # Execute the SQL command
        conn = pymysql.connect(host='192.168.2.55', port=3306, user='root', passwd='89787198', db='stockevaluation', charset="utf8")
        cursor = conn.cursor()
        cursor.execute('SELECT stockcode,stockName,stockIsYesterdayPotential,stockIsTodayPotential FROM stocktable WHERE stockIsYesterdayPotential=1 OR stockIsTodayPotential=1')
        # Fetch all the rows in a list of lists.
        stock_potential_info = {}
        if_potential_dict = {0:'不是', 1:'是'}
        results = cursor.fetchall()
        for row in results:
            stock_potential_info[row[0]] = [row[1], if_potential_dict[int(row[2])], if_potential_dict[int(row[3])]]

    except:
        print("Error: unable to fecth data")

    cursor.close()
    conn.commit()
    conn.close()

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