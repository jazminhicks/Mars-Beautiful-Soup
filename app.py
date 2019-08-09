from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create flask instance
app = Flask(__name__)


# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


@app.route("/scrape")
def import_scrape():

    mars_info = scrape_mars.scrape()    
    
    #update database
    mongo.db.collection.update({}, mars_info, upsert = True)

    print(mars_info)

    return redirect("/", code=302)

@app.route("/")
def index(): 
    mission_data = mongo.db.collection.find_one()

    return render_template("index.html", mission_data=mission_data)

if __name__== "__main__":
    app.run(debug=True)