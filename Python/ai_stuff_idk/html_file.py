from flask import Flask, render_template, url_for
from google import genai

client = genai.Client(api_key= "AIzaSyDrQ99Qq8dc9PaTY7ACXBZmUjZ6s_qoYa0")

app = Flask(__name__)

@app.route('/')
def index():
    response = client.models.generate_content(
    model="gemini-2.5-flash", contents=f"""For 
    the Eastern Henrico Government Center at Virginia 23223, 
    the Broad Rock Branch - Richmond Public Library at 4820 Old Warwick Rd, Richmond, VA 23224,
    the Best Plaza at 1400 Best Plz Dr, Richmond, VA 23227,
    the Annie Marie Giles Community Resource & Training Center at 1400 Oliver Hl Wy, Richmond, VA 23219,
    and the Kroger Marketplace at 9000 Staples Mill Rd, Henrico, VA 23228,
    use information from the web, such as traffic, time, and news to predict the probability that each location will be able to provide water in the case of a boil water advisory. 
    Return the results as a json file in with the keys ehgc, library, best_plaza, annie_marie_giles, and kroger conaining a single float value from 0 to 1 containg 3 decimal places representing the probability that each location will be able to provide water. 
    There should be nothing else in the response other than the json file.""",
)
    
    # json_dict = dict(response.text)
    keys = ["ehgc", "library", "best_plaza", "annie_marie_giles", "kroger"]
    probability_list = [0.90, 0.10, 1, 1, 0.70]
    # for key in keys:
    #     probability_list.append(json_dict.get(key, 0))
    
    return render_template('index.html', probabilities=probability_list)