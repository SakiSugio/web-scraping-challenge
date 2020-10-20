from flask import Flask, render_template
import Scrap_Mars

from pymongo import MongoClient
mongo = MongoClient("mongodb://localhost:27017/mars_db")
app = Flask(__name__)
@app.route("/")
def index(): 
    mars_coll = mongo.db.mars.find_one()
    return render_template("index.html", mars = mars_coll)

@app.route("/scrape")
def scrape(): 
    mars_data = scrape_mars.scrape()
    mars_coll.update({},mars_data, upsert=True)
    return "scraping successful !"

if __name__ == "__main__": 
    app.run(debug=True)
