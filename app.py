from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/nasa_mars_challenge"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/craigslist_app")


@app.route("/")
def index():
    nasa_data = mongo.db.data.find_one()
    return render_template("index.html", space=nasa_data)


@app.route("/scrape")
def scraper():
    datas = mongo.db.data
    datas_data = scrape_mars.scrape()
    datas.update({}, datas_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)


