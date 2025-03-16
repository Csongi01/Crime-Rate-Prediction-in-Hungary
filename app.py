from flask import Flask, request, render_template , jsonify
import joblib,  dj
from ValidateForm import CrimeFormValidator

app = Flask(__name__)
# Load the model using joblib
with open('Model/model.pkl', 'rb') as f:
    model = joblib.load(f)
    
#get the model prediction
@app.route('/predict', methods=['POST'])
def predict_result():

    #determine model input data
    year = request.form['year']    
    city_code = dj.get_city_code(request.form['city'] ) 
    crime = request.form['crime']
    
    validator = CrimeFormValidator(year, city_code, crime)
    errors = validator.validate()
    # If there are errors, render the template with error messages
    if errors:
        return render_template("index.html", errors=errors)
    
    # Adjust population for the given year
    population = dj.get_population(city_code)  
 
    pop = dj.get_adjusted_population(city_code, int(year))
    future= int(year) + 5
    past= int(year) - 5

    cityCategory = dj.get_citycateg(city_code)
   
    #Get the prediction
    crime_rate = model.predict([[crime, city_code, year, pop, cityCategory]])[0]
    crime_rate_plus = model.predict([[crime, city_code, future, dj.get_adjusted_population(city_code, future), cityCategory]])[0]
    crime_rate_minus = model.predict([[crime, city_code, past,dj.get_adjusted_population(city_code, past), cityCategory]])[0]


    #Pass adational information to the predict page
    city_name =request.form['city']
   
    crime_type = dj.get_crime(request.form['crime'] )
    city_categ = dj.get_city_category(city_code)
    out_of_value = dj.get_out_of_valuec(city_categ)
    crime_categ = dj.get_crimecategory(city_categ, crime_rate)  

    return render_template('result.html', city_name=city_name, crime_type=crime_type, year=year, city_categ=city_categ , crime_rate=crime_rate, out_of_value=out_of_value ,crime_categ=crime_categ, population=population,
                            crime_rate_plus=crime_rate_plus, crime_rate_minus=crime_rate_minus)

# About the app english version
@app.route('/About', methods=['GET'])
def about():
    return render_template("about.html")

# About the app hungarian version
@app.route('/About_hun')
def about_hun():
    return render_template('about_hun.html')


#Get crimes related to the selected city
@app.route('/crimes', methods=['GET'])
def crimes():
    city = request.args.get('city')
    crime_types = dj.get_city_crime_types(city)
    return jsonify(crime_types)

#Autocomplete city input
@app.route('/autocomplete-cities', methods=['GET'])
def autocomplete_cities():
    query = request.args.get('query', '').lower()
    if not query:
        return jsonify([])

    con = dj.get_db_connection()
    cursor = con.cursor()
    cursor.execute('SELECT City FROM City WHERE LOWER(City) LIKE ?', ('%' + query + '%',))
    rows = cursor.fetchall()
    con.close()

    cities = [row['City'] for row in rows]
    return jsonify(cities)

#index page            
@app.route('/')
def index():
    return render_template("index.html", errors={})

if __name__ == '__main__': 
    app.run(debug=True)

