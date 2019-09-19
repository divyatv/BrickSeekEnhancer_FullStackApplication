from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

app = Flask(__name__)

# setup mongo connection
conn = "mongodb://localhost:27017"
mongo = pymongo.MongoClient(conn)


# connect to mongo db and collection
db = mongo.mars_project
collection = db.mars_data


@app.route("/")
def index():
    # write a statement that finds all the items in the db and sets it to a variable

    mars_page_info = list(db.collection.find())
    mars_test = db.collection.find_one()

    #if len(mars_info):
        # render an index.html template and pass it the data you retrieved from the database
    #return render_template("index.html", my_mars_page=mars_page_info)
    return render_template("index.html",verify_data=mars_test)
    #else:
    #    return render_template("index.html", mars_data={""})

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_dict = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    db.collection.update({}, mars_dict, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
