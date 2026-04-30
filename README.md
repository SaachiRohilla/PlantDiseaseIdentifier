# Plant Disease Identifier <br>
## Group 13: Saachi Rohilla (sr1902), Vivian Chung (vec43), Maya Zarcone (mez59) <br>

## How to run web application: <br>
To activate virtual environment run: source .venv/bin/activate <br>
To start flask application run: python3 src/app.py <br>
Click on the link to the development server or copy/paste the url into a trusted browser<br>
Press CTRL+C to quit the application <br>

## Directory Overview: <br>

**src/app.py** - main flask application <br>
**src/gettingkaggle.py** - import kaggle dataset and randomly samples files for training and testing <br>
**src/train.py** - loads dataset and model, does preprocessing on data, trains, evaluates, and saves model <br>
**randomdata (directory)** - stores the raw jpg images before they are processed into numpy arrays <br>
**src/vectorize.py** - converts jpg images into numpy arrays for model training <br>
**src/vectorize_data (directory)** - numpy arrays are placed in one of 5 sub-folders corresponding to their status as healthy or infected <br> 
**src/templates (directory)** - stores html files <br>
