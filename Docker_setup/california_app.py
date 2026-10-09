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
            :root {
                color-scheme: light;
                font-family: Inter, "Segoe UI", Arial, sans-serif;
                color: #172554;
                background: #f1f5f9;
            }

            * { box-sizing: border-box; }

            body {
                min-height: 100vh;
                margin: 0;
                padding: 64px 24px;
                background:
                    radial-gradient(ellipse at 15% 0%, #dbeafe 0, transparent 42%),
                    #f1f5f9;
            }

            h1, h2, p { margin-top: 0; }

            h1 {
                margin-bottom: 12px;
                color: #0f172a;
                font-size: clamp(2rem, 5vw, 3.25rem);
                letter-spacing: -0.045em;
                text-align: center;
            }

            h1::after {
                display: block;
                width: 56px;
                height: 4px;
                margin: 18px auto 36px;
                border-radius: 999px;
                background: #2563eb;
                content: "";
            }

            .container {
                display: grid;
                width: min(100%, 900px);
                margin: 0 auto;
                grid-template-columns: repeat(auto-fit, minmax(min(100%, 320px), 1fr));
                gap: 24px;
            }

            .box {
                padding: 30px;
                border: 1px solid #e2e8f0;
                border-radius: 20px;
                background: rgba(255, 255, 255, 0.92);
                box-shadow: 0 16px 40px rgba(15, 23, 42, 0.08);
            }

            h2 {
                margin-bottom: 22px;
                color: #1e3a8a;
                font-size: 1.2rem;
            }

            input, button {
                width: 100%;
                min-height: 46px;
                margin: 0 0 12px;
                padding: 11px 14px;
                border-radius: 10px;
                font: inherit;
            }

            input {
                border: 1px solid #cbd5e1;
                background: #fff;
                color: #0f172a;
                transition: border-color 150ms ease, box-shadow 150ms ease;
            }

            input::placeholder { color: #94a3b8; }

            input:focus {
                border-color: #3b82f6;
                outline: none;
                box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.16);
            }

            input[type="file"] {
                height: auto;
                padding: 9px;
                color: #475569;
            }

            input[type="file"]::file-selector-button {
                margin-right: 12px;
                padding: 8px 12px;
                border: 0;
                border-radius: 7px;
                background: #e2e8f0;
                color: #1e293b;
                cursor: pointer;
            }

            button {
                margin-top: 4px;
                border: 0;
                background: #2563eb;
                color: #fff;
                font-weight: 650;
                cursor: pointer;
                transition: background 150ms ease, transform 150ms ease;
            }

            button:hover {
                transform: translateY(-1px);
                background: #1d4ed8;
            }

            button:focus-visible {
                outline: 3px solid #93c5fd;
                outline-offset: 3px;
            }

            .result {
                min-height: 24px;
                margin-top: 8px;
                color: #166534;
                font-weight: 650;
                overflow-wrap: anywhere;
            }

            @media (max-width: 480px) {
                body { padding: 40px 16px; }
                .box { padding: 22px; }
            }
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
