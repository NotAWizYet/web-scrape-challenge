# import necessary libraries
from flask import Flask, render_template, jsonify, redirect
import pymongo
import mars_scrape


# instantiate flask app
app = Flask(__name__)

client = pymongo.MongoClient()
db = client.mars_db
collection = db.mars_collection

# create route to render index.html 
@app.route("/")
def index():
    mars_collection_values = list(db.collection.find())
    print(mars_collection_values)
    mars_collection_values = mars_collection_values[0]
    return render_template("index.html", mars_collection_values = mars_collection_values)

@app.route('/scrape')
def scrape():
    data = mars_scrape.scrape()
    db.collection.delete_many({})
    db.collection.insert_one(data)
    return redirect("http://localhost:5000/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
