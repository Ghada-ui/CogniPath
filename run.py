# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from app import app, db
if __name__ == '__main__':
     app.run(host='localhost', port=3000,debug=True)