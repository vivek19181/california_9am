from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
import pickle
import pandas as pd
import uvicorn

# Initialize app
app = FastAPI()

# Load model
with open("california_model.pkl", "rb") as f:
    classifier = pickle.load(f)

@app.get("/", response_class=HTMLResponse)
def main_page():
    # HTML UI for input and file upload
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>California Housing Price Predictor</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            input, button { padding: 8px; margin: 5px 0; width: 100%; max-width: 300px; }
            .container { display: flex; gap: 50px; flex-wrap: wrap; }
            .box { border: 1px solid #ccc; padding: 20px; border-radius: 10px; width: 350px; }
            .result { margin-top: 10px; font-weight: bold; }
        </style>
    </head>
    <body>
        <h1>California Housing Price Predictor</h1>
        <div class="container">
            <div class="box">
                <h2>Predict from Input</h2>
                <input type="number" step="0.01" id="MedInc" placeholder="Median Income">
                <input type="number" step="0.01" id="HouseAge" placeholder="House Age">
                <input type="number" step="0.01" id="AveRooms" placeholder="Average Rooms">
                <input type="number" step="0.01" id="Population" placeholder="Population">
                <input type="number" step="0.01" id="AveOccup" placeholder="Average Occupancy">
                <input type="number" step="0.01" id="Latitude" placeholder="Latitude">
                <button onclick="predict()">Predict</button>
                <div class="result" id="result"></div>
            </div>
            <div class="box">
                <h2>Predict from CSV File</h2>
                <input type="file" id="csvFile">
                <button onclick="predictFile()">Upload & Predict</button>
                <div class="result" id="fileResult"></div>
            </div>
        </div>
        <script>
            async function predict() {
                const MedInc = parseFloat(document.getElementById("MedInc").value);
                const HouseAge = parseFloat(document.getElementById("HouseAge").value);
                const AveRooms = parseFloat(document.getElementById("AveRooms").value);
                const Population = parseFloat(document.getElementById("Population").value);
                const AveOccup = parseFloat(document.getElementById("AveOccup").value);
                const Latitude = parseFloat(document.getElementById("Latitude").value);

                const response = await fetch(`/predict?MedInc=${MedInc}&HouseAge=${HouseAge}&AveRooms=${AveRooms}&Population=${Population}&AveOccup=${AveOccup}&Latitude=${Latitude}`);
                const data = await response.json();
                document.getElementById("result").innerText = "Predicted Price: " + data.prediction.toFixed(2);
            }

            async function predictFile() {
                const fileInput = document.getElementById("csvFile");
                const file = fileInput.files[0];
                const formData = new FormData();
                formData.append("file", file);

                const response = await fetch('/predict_file', {
                    method: 'POST',
                    body: formData
                });
                const data = await response.json();
                document.getElementById("fileResult").innerText = "Predictions: " + data.predictions.join(", ");
            }
        </script>
    </body>
    </html>
    """

# Predict from query parameters
@app.get("/predict")
def predict(MedInc: float, HouseAge: float, AveRooms: float,
            Population: float, AveOccup: float, Latitude: float):
    input_data = [[MedInc, HouseAge, AveRooms, Population, AveOccup, Latitude]]
    prediction = classifier['model'].predict(input_data)
    return {"prediction": float(prediction[0])}

# Predict from uploaded CSV file
@app.post("/predict_file")
def predict_file(file: UploadFile = File(...)):
    df_test = pd.read_csv(file.file)
    prediction = classifier['model'].predict(df_test)  # Use classifier['model'] if it's a dict
    return {"predictions": prediction.tolist()}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
