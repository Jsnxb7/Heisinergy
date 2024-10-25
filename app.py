from flask import Flask, request, jsonify, redirect, url_for, render_template, make_response
from flask_cors import CORS
from werkzeug.security import check_password_hash, generate_password_hash
import os
import json
from functools import wraps
import base64


app = Flask(__name__)
CORS(app)   

@app.route('/')
def login():
    return render_template('index.html')

@app.route('/test')
def test():
    return "Server is running"

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
