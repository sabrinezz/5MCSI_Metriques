from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html') 

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")
@app.route("/Histogramme/")
def histogramme():
    return render_template("histogramme.html")

def get_commits():
    url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"
    response = requests.get(url)
    commits = response.json()
    return commits

def extract_minutes(commits):
    minutes = []
    for commit in commits:
        date_string = commit['commit']['author']['date']
        date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
        minutes.append(date_object.minute)
    return Counter(minutes)

@app.route('/commits/')
def show_commits():
    return render_template('commits.html')

@app.route('/commits/data')
def get_commits_data():
    commits = get_commits()
    counter = extract_minutes(commits)
    return jsonify(counter)

if __name__ == '__main__':
    app.run(debug=True)
  
@app.route("/contact/")
def MaPremiereAPI():
    return render_template("contact.html")
@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)
  
if __name__ == "__main__":
  app.run(debug=True)
