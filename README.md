# MsC
Master's Degree

## Installation and running

Requirements:
- Python 3.8 or higher
- Node.js (tested on v16.14.2)

### Requirements.txt file

We have the `requirements.txt` file in `src` directory. To install all libraries, just digit the command:

```pip install requirements.txt```

### Backend

This backend is made in Python language. The main reason that Python is the chosen language is because the main ML libraries are written in Python

To run the backend part of application, just digit the command:

```python3 flask_start.py```

It starts the Flask service on 8080 port

### Pipeline

If you want to test the pipeline, just digit the command:

```python3 main.py```

In this file you can execute all possible pipelines and the MAPE-K (See: MAPE-K, Autonomic Computing) part, to guarantee an automatic choice to pipeline based on previous metrics (obtained in manual pipeline executions)

### Frontend

The frontend requires [Flask backend](#Backend) in execution

### Package.json file

We have the `package.json` file in `ml-ui` directory. To install all libraries, just digit the command:

```npm install```

To run the frontend part of application, just digit the command:

```npm start```

It starts the React application