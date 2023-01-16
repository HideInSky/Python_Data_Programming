# project: p4
# submitter: lin364
# partner: none
# hours: 8
import pandas as pd
from flask import Flask, request, jsonify, Response
import re, time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

app = Flask(__name__)
# df = pd.read_csv("main.csv")

home_visited = 0
from_a = 0
from_b = 0
a_or_b = -1

def create_svg():
    df = pd.read_csv("main.csv")
    hap = df['Happiness score']
    gdp = df['Explained by: GDP per capita']

    # adapted from https://matplotlib.org/3.5.0/gallery/shapes_and_collections/scatter.html#sphx-glr-gallery-shapes-and-collections-scatter-py
    np.random.seed(19680801)
    N = len(hap)
    colors = np.random.rand(N)

    fig, ax = plt.subplots()
    ax.scatter(x=hap, y=gdp, s=100, c=colors, alpha=0.4)
    fig.savefig("hap_gdp.svg")
    plt.close(fig)
    
@app.route('/')
def home():
    global home_visited, a_or_b
    home_visited += 1
    create_svg()
    # starting from 11 times, determine final version of A/B
    if home_visited == 11:
        a_or_b = 0 if from_a > from_b else 1
    # choose whether go to A/B
    if a_or_b == 0 or (a_or_b == -1 and home_visited % 2 == 1):
        with open("index.html") as f:
            html = f.read()
            html_a = html.replace("donate.html", "donate.html?from=A")
        return Response(html_a, headers={"Content-Type": "text/html"})
    else:
        with open("index.html") as f:
            html = f.read()
            html = html.replace("blue", "red")
            html_b = html.replace("donate.html", "donate.html?from=B")
        return Response(html_b, headers={"Content-Type": "text/html"})    

@app.route('/browse.html')
def browse():
    f = pd.read_csv("main.csv")
    h = f.to_html(index=True)
    html = """
         <h1>Browse</h1>
         {}
         """.format(h)
    return Response(html, headers={"Content-Type": "text/html"})

visitors = {}

@app.route('/browse.json')
def browse_json():
    global visitors
    ip = request.remote_addr
    if ip in visitors.keys():
        interval = time.time() - visitors.get(ip)
        if interval < 60:
            return Response(f"Please try after {60-interval}s", status = 429, headers={"Content-Type": "text/html", "Retry-After": 60-interval})
    visitors[ip]=time.time()
    df = pd.read_csv("main.csv")
    df_dict = df.to_dict(orient="index")
    df_json = jsonify(df_dict)
    return df_json

@app.route('/email', methods=["POST"])
def email():
    email = str(request.data, "utf-8")
    if re.match("\w*@\w*\.\w*", email): # 1
        with open("emails.txt", "a") as f: # open file in append mode
            f.write(email + '\n') # 2
        with open("emails.txt", "r") as f: 
            num_subscribed = len(f.readlines())
        return jsonify(f"thanks, you're subscriber number {num_subscribed}!")
    return jsonify("Error: invalid email address!") # 3

@app.route('/donate.html')
def donate():
    global from_a, from_b
    param = request.args.get("from")
    if param == 'A':
        from_a += 1
    if param == 'B':
        from_b += 1
    with open("donate.html") as f:
        html = f.read()
    return Response(html, headers={"Content-Type": "text/html"})
        
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, threaded=False) # don't change this line!

# NOTE: app.run never returns (it runs for ever, unless you kill the process)
# Thus, don't define any functions after the app.run call, because it will
# never get that far.