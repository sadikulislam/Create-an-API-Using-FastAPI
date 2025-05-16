from fastapi import FastAPI
import json

app = FastAPI()

def load_data():
    # Simulate loading data from a JSON
    with open('paitents.json', 'r') as f:
        data = json.load(f)
    return data

@app.get("/")
def hello_world():
    return {"message": "Paitents Management System"}

@app.get("/about")
def about():
    return {"message": "This is a Paitents Management System API."}

@app.get("/veiw")
def view():
    data = load_data()
    return {"paitents": data}