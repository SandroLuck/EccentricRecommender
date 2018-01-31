## Eccentric Recommender
This is the source code for an Eccentric Recommender System.
This work is mainly based on the theoretical work of,
https://arxiv.org/abs/1709.10060

## Install
To run this Python 3.x.x is needed. 
Various packages migth have to be installed,

 - numpy  
 - sk-learn 
 - contextlib  
 - pickle  
 - pathlib  
 - scipy  
 - tqdm

## Run

Run file CreateRecommendations.py with python,

    python CreateRecommendations.py

Most other files are just pre processing for the data sets. 
To create this for a new data set, 
follow the steps in the document. 
All functions are present the input-files might have to be renamed.
## Good to know
On the first run, the system will created the dictionaries, which will speed up computation on the following runs.
