from fastapi import FastAPI, UploadFile, File
import pickle
import pandas as pd
import uvicorn  # It is a server to run FastAPI

# Initialize app
app = FastAPI()   

# Load model
with open("california_model.pkl", "rb") as f:
    classifier = pickle.load(f)

@app.get("/")   
def main_page():
    return('welcome')
# Predict from query parameters

@app.get("/predict")
def predict(MedInc:float,HouseAge:float,AveRooms:float, 
           Population:float, AveOccup:float, Latitude:float):
    input_data = [[MedInc,HouseAge,AveRooms, 
           Population, AveOccup, Latitude]]
    prediction = classifier['model'].predict(input_data)
    return {"prediction": float(prediction[0])}

# Predict from uploaded CSV file
@app.post("/predict_file")
def predict_file(file: UploadFile = File(...)):
    df_test = pd.read_csv(file.file)
    prediction = classifier['model'].predict(df_test)
    return {"predictions": prediction.tolist()}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
