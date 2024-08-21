from flask import Flask, render_template, request
from DataVisForFlask import generateGraphs

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    
    country = request.form['country']
    sport = request.form['sport']

    print(f"Received country: {country}, sport: {sport}")  # Debugging line

    return generateGraphs(country, sport)

if __name__ == "__main__":
    app.run(debug=True)
