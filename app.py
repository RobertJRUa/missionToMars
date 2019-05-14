#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

# The default port used by MongoDB is 27017
# https://docs.mongodb.com/manual/reference/default-mongodb-port/
# Use PyMongo to establish Mongo connection

# mars_db hasn't been created 
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")

# Create app index route 
@app.route("/")
def home():
    
    # Find one record of data from the mongo database
    mars_data = mongo.db.collection.find_one()
   
    # Return template and data
    return render_template("index.html", marsIndex = mars_data)
    
# Create app scrape route
@app.route("/scrape")
def scrape():
    
    # Run the scrape function 
     mars_app_scrape = scrape_mars.scrape_info()
    
    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_app_scrape, upsert=True)
   
    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
    
    # Now go to terminal and run the py file with mongo to put data into mars_db
