from fastapi import FastAPI, Path, HTTPException, Query
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

@app.get("/paitents/{paitent_id}")
def get_paitent(paitent_id: str = Path(..., description="The ID of the paitent to view in DB", example="P001")):
    data = load_data()

    if paitent_id in data:
        return {"paitent": data[paitent_id]}
    raise HTTPException(status_code=404, detail="Paitent not found")

@app.get("/sort")
def sort_paitents(sort_by: str = Query(..., description="Sort on the basis of height, weight or BMI"), order: str = Query("asc", description="sort in asc or desc order")):

    valid_sort_keys = ["height", "weight", "bmi"]
    if sort_by not in valid_sort_keys:
        raise HTTPException(status_code=400, detail="Invalid sort parameter select from {valid_sort_keys}")
    
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid order parameter select between asc or desc")
    
    data = load_data()

    sort_order = True if order == "desc" else False

    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)

    return sorted_data