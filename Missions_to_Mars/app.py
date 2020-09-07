from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars as scrape
import sys
import pprint
pp = pprint.PrettyPrinter(indent=4)

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mission_to_mars"
mongo = PyMongo(app)

@app.route("/")
def index():
    mission = mongo.db.mission.find_one()
    pp.pprint(mission)
    return render_template("index.html", mission=mission)


@app.route("/scrape")
def scraper():
    mission = mongo.db.mission
    mission_data = scrape.scrape()
    mission.update({}, mission_data, upsert=True)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)