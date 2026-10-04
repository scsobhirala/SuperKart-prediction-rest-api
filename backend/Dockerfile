FROM python:3.9-slim

#set the working direcgtory inside the container 
WORKDIR /app

#Copy the requirements.txt file to the container 
COPY requirements.txt ./

##install the dependenies from the requirements file without using cache to reduce 
##image  size 
RUN pip install --no-cache-dir-upgrade -r requirements.txt
# Define the command to start the application using Gunicorn with 4 worker processes
# - `-w 4`: Uses 4 worker processes for handling requests
# - `-b 0.0.0.0:7860`: Binds the server to port 7860 on all network interfaces
# - `app:app`: Runs the Flask app (assuming `app.py` contains the Flask instance named `app`)
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:7860", "app:rental_price_predictor_api"]
