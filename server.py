from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():
    # Load predictions
    df = pd.read_csv("nba_predictions.csv")

    # Convert to list of dictionaries for easy HTML rendering
    predictions = df.to_dict(orient="records")

    return render_template("index.html", predictions=predictions)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
