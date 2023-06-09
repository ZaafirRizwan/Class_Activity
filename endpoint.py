from flask import Flask, request, jsonify,render_template
import pandas as pd
import os
from sklearn.linear_model import LinearRegression
import joblib

app = Flask(__name__,template_folder='/app')

print(os.getcwd())

# Load the dataset
data = pd.read_csv("Salary_Data.csv")

# Prepare the data
X = data["YearsExperience"].values.reshape(-1, 1)
y = data["Salary"].values

# Train the model
model = LinearRegression()
model.fit(X, y)

# Predict the salary for a given experience
experience = 5.5
predicted_salary = model.predict([[experience]])
print("Predicted salary for {} years of experience: {}".format(experience, predicted_salary[0]))
joblib.dump(model, 'linear_regression_model.pkl')

# Load the trained model
model = joblib.load('linear_regression_model.pkl')

@app.route("/")
def welcome():
    print("Welcome Page")
    return render_template("index.html")

@app.route("/predict", methods=['POST'])
def predict():
    experience = float(request.form['experience'])
    predicted_salary = model.predict([[experience]])
    return jsonify({"predicted_salary": predicted_salary[0]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000,debug=True)
