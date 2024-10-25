from flask import Flask, request, jsonify, redirect, url_for, render_template, make_response
from werkzeug.security import check_password_hash, generate_password_hash
import os
import json
from functools import wraps
import base64


app = Flask(__name__)

@app.route('/')
def login():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
