#################### How to run ############################
python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload


app:app
first app : file name

second app :  our instance in code
app=FastAPI()

pip install -r requirements.txt


http://127.0.0.1:8000/
http://localhost:8000/

############## DOCKER ######################################
# Use official Python image as base
    #######################
    FROM python:3.11-slim
    ######################

Purpose: Sets the base image for your Docker container.

Why Python 3.11-slim:

python:3.11 gives you Python 3.11 installed.

-slim is a lightweight version of the image, smaller in size (~100MB), which reduces image bloat.

Effect: Your container starts with Python already installed, so you don’t need to install it manually.

# Step-2: Set working directory

       ###################
          WORKDIR /app
       ###################
 Purpose: Sets the default working directory inside the container.
 Example: If you later run python main.py, it will look for main.py in /app.

# Step-3: Copy requirements if you have one, or install dependencies directly

   ##############################
     COPY requirements.txt .
   ##############################

Purpose: Copies your requirements.txt from your local machine into the container.

. refers to the current directory inside the container (/app because of WORKDIR).

# Step-4: # Install dependencies

    #######################################################
      RUN pip install --no-cache-dir -r requirements.txt
    ########################################################
Purpose: Installs all Python packages listed in requirements.txt into the container.

# Step-5 : # Copy the rest of the app

  ############################
     COPY . .
  ###########################
Purpose: Copies all files from your local project directory into the container (/app).

# Step-6: Expose the port FastAPI will run on

  ##########################
      EXPOSE 8000
  ###########################

Purpose: Tells Docker that the container will listen on port 8000.

# Step-7: Command to run the app with uvicorn

###################################################################
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
#####################################################################


