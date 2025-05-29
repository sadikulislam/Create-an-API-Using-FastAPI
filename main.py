from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json

app = FastAPI()


class Patient(BaseModel):

    id: Annotated[str, Field(..., description="The ID of the patient", example="P001")]
    name: Annotated[str, Field(..., description="The name of the patient", example="Abul Kalam")]
    city: Annotated[str, Field(..., description="The city of the patient", example="Rajshahi")]
    age: Annotated[int, Field(...,  gt= 0, lt=120, description="The age of the patient", example=30)]
    gender: Annotated[Literal['male', 'female', 'other'], Field(..., description="Gender of the patient")]
    height: Annotated[float, Field(..., gt=0, description="Height of the patient in m", example=1.5)]
    weight: Annotated[float, Field(..., gt=0, description="Weight of the patient in kg", example=70.0)]



    @computed_field
    @property
    def bmi(self) -> float:
        """Calculate the Body Mass Index (BMI) of the patient."""
        bmi = round(self.weight / (self.height ** 2), 2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:

        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Normal'
        else:
            return 'Obese'

class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Literal['male', 'female', 'other'], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]


def load_data():
    # Simulate loading data from a JSON
    with open("patients.json", "r") as f:
        data = json.load(f)
    return data

def save_data(data):
    # Simulate saving data to a JSON
    with open("patients.json", "w") as f:
        json.dump(data, f, indent=4)


@app.get("/")
def hello_world():
    return {"message": "Patients Management System"}


@app.get("/about")
def about():
    return {"message": "This is a Patients Management System API."}


@app.get("/veiw")
def view():
    data = load_data()
    return {"patients": data}


@app.get("/patients/{patient_id}")
def get_patient(
    patient_id: str = Path( ..., description="The ID of the patient to view in DB", example="P001"),
):
    data = load_data()

    if patient_id in data:
        return {"patient": data[patient_id]}
    raise HTTPException(status_code=404, detail="patient not found")


@app.get("/sort")
def sort_patients(
    sort_by: str = Query(..., description="Sort on the basis of height, weight or BMI"),
    order: str = Query("asc", description="sort in asc or desc order"),
):
    valid_sort_keys = ["height", "weight", "bmi"]
    if sort_by not in valid_sort_keys:
        raise HTTPException(
            status_code=400,
            detail="Invalid sort parameter select from {valid_sort_keys}",
        )

    if order not in ["asc", "desc"]:
        raise HTTPException(
            status_code=400, detail="Invalid order parameter select between asc or desc"
        )

    data = load_data()

    sort_order = True if order == "desc" else False

    sorted_data = sorted(
        data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order
    )

    return sorted_data

@app.post("/create")
def add_patient(patient: Patient):
    data = load_data()

    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient already exists")

    data[patient.id] = patient.model_dump(exclude=['id'])

    save_data(data)

    return JSONResponse(status_code=201, content={'message':'Patient created successfully'})


@app.put("/update/{patient_id}")
def update_patient(patient_id: str, patient_update: PatientUpdate):
     data = load_data()

     if patient_id not in data:
         raise HTTPException(status_code=404, detail="Patient not found")

     patient_data = data[patient_id]

     # Update the fields if they are provided
     updated_patient_data = patient_update.model_dump(exclude_unset=True)

     for field, value in updated_patient_data.items():
         if value is not None:
             patient_data[field] = value

     data[patient_id] = patient_data

     save_data(data)

     return JSONResponse(status_code=200, content={'message': 'Patient updated successfully'})
     