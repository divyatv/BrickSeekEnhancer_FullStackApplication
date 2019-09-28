from flask import Flask, jsonify, render_template
import json
import scrapebrickseekfinal

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['GET','POST'])
def scrapedmap():
    return render_template("Marker_Clusters.html", jsonvalue= json.dumps(scrapebrickseekfinal.scrape_all()))
    # return render_template("Marker_Clusters.html")

if __name__ == "__main__":
    app.run()
