# ml-coding-assignment

This is the productionized code for my NEISS Survey Data model. 

## Usage
I originally planned to implement a command line interface and an API, but I only had enough time for the API.  This API was envisioned as accessible by a mobile application, so that an individual can enter his or her 'diagnosis' (i.e. injury symptoms) and stats and obtain a prediction of their ER outcome. You can access the
endpoint at http://34.192.12.23/api with GET requests corresponding to columns in the NEISS sample survey data. 

* Valid columns:
  * trmt_date - MM/DD/YYYY format
  * stratum - (single-character code)
  * age - (continuous or int)
  * sex - (int)
  * race - (int)
  * diag - (int)
  * body_part (int)
  * location (int)
  * prod1 (int)

Any invalid columns or values will be imputed with NaN values. Missing columns will also be imputed with NaN values, but the model will decrease in accuracy.

Example GET request: http://34.192.12.23/api?age=20&body_part=31&diag=62&trmt_date=11/12/2016&location=1&race=1&stratum=S&prod1=1411&sex=1

The GET request returns its disposition prediction code (1,2,4,5,8, or 9) for the given input parameters. Please contact me if the server happens to be down.

## Build
Requirements: Python-2.7.X and most up-to-date pip.

To build and deploy your own Neiss scoring server from this repo:
```
# clone repo
git clone "https://github.com/bkvillalobos/ct-neiss-ml.git"
cd ct-neiss-ml/neiss/

# unzip seralized model
gunzip models/20161205-01-43-30_rf_weighted_resampling.pkl.gz 

# install requirements
virtualenv venv # not required, but recommended
source venv/bin/activate # not required, but recommended
pip install -r requirements.txt

# start FLASK server
export FLASK_APP="[absolute_path]/neiss/neiss_server.py" 
# $FLASK_APP is only defined for the length of the session, so it should be added to .bashrc or .bash_profile
flask run --host=0.0.0.0 --port:80 # port 80 exposes to http access
```

The http://34.192.12.23/api build is hosted on an Ubuntu AWS EC2 instance. See my email for the .pem file to take a peek under the hood.

## Project Structure
This is the overall design of the project:
![Alt text](project_organization.JPG?raw=true "Planned ML backend")
All the modules with * are implemented in this project. With another day, I would've liked to implement a productionized/automated version of the training module - **the current productionized model was pre-trained and serialized in research_and_dev.ipynb**.

Implemented components:
* Scoring server
  * **neiss/neiss_server.py** - very simple Flask server implementation for demonstration purposes
* Scoring Module (neiss/scorer/)
  * **scorer.py** - object-oriented Scorer class, used by API and CLI to make predictions from inputs
  * **scorer_constants.py** - stores constants objects, so that any changes in input module design (i.e. model codes) can propogate instantly
  * **scorer_cli.py** - UNFINSHED IMPLEMENTATION of CLI interface for scorer.py
  * **tests/*** - scoring module pytests
* Feature Extraction Module (neiss/etl_utils/)
  * **feature_extractor.py** - object-oriented FeatureExtraction class that orchestrates feature extraction. Only needs to be minorly extended for use with future implementation of training module.
  * **etl_constants.py** - stores constants objects, so that any changes in input data design (i.e. column names) can propogate instantly
  * **tests/*** feature extraction module pytests
  * **resources/***  resources necessary for feature extraction. Specifically, serialized (pickled) dictionaries of frequency counts of prod1 values during training to extract bayesian likelihood features from prod1 values in input data.
  
* Serialized Model (models/)
  * **20161205-01-43-30_rf_weighted_resampling.pkl.gz** - serialized and compressed skicit-learn model object. Currently holds a weighted resampled Random Forest trained on 12/05/2015, but it's designed to hold multiple versions and different kinds of models. Only most recent model of type [model_type] is used.

## Model Accuracy Summary
**See my email attachement for a longer discussion on model methodology & development.**

The model has an out-of-sample predictive accuracy of ~96.6%. Raw model accuracy can be misleading with this type of unbalanced data (91% of observations are of disposition 1, so you can get 91% accuracy for just predicting 1 for everything!). So, I've included a breakdown of accuracy conditioned upon disposition:

  ![Alt text](RF weighted sampling with replacement.png?raw=true "Results for RF weighted sampling with replacement")

As you can see, the model has a greater than 50% chance of correctly predicting any disposition category - even disposition 9, which was only observed 32 times out of the entire NEISS survey of ! Performance dramatically increases with the more slightly more frequent catgories of 2 and 4 (each < 6% of training data), and is virtually perfect for dispositon category 1.

These results were obtained (and can be reproduced end-to-end from the raw NEISS data) in **research_and_dev.ipynb**.
