# META DATA - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

     # Developer details: 
        # Name: Harshita and Prachi
        # Role: Architects
    # Version:
        # Version: V 1.0 (20 September 2024)
            # Developers: Harshita and Prachi
            # Unit test: Pass
            # Integration test: Pass
     
    # Description: This code snippet preprocesses the data for a machine learning model by scaling
    # numerical columns, encoding categorical columns, and extracting date components for before feeding it to train the model
        # PostgreSQL: Yes

# CODE - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

    # Dependency: 
        # Environment:     
            # Python 3.11.5
            # Pandas 2.2.2
            # Scikit-learn 1.5.0
import numpy as np
import pandas as pd     # Importing pandas for data manipulation
from sqlalchemy import create_engine
from sklearn.preprocessing import LabelEncoder  # Importing tools for data preprocessing
import spacy
from pymongo import MongoClient

def preprocess_mongo_data(data):
    data.drop_duplicates(inplace=True)
    data.dropna(inplace=True)
    # Load spaCy model
    nlp = spacy.load("en_core_web_sm") 

    def preprocess(text):
        doc = nlp(text)
        filtered_tokens = []
        for token in doc:
            # Skip stopwords and punctuation
            if not token.is_stop and not token.is_punct:
                filtered_tokens.append(token.lemma_)  # Lemmatize the token
                
        return " ".join(filtered_tokens)
    
    data['Preprocessed Text'] = data['tweet_content'].apply(preprocess) 
    # Encode categorical columns
    le = LabelEncoder() # Initialize the LabelEncoder
    data['sentiment'] = le.fit_transform(data['sentiment']) # Encode sentiment column
    return data

    
def load_and_preprocess_data(mongdb_host, mongodb_port, mongodb_db):
    client = MongoClient(host=mongdb_host, port=mongodb_port)
    db = client[mongodb_db]
    collection = db["tweet_data"]

    # Fetch data from MongoDB and convert it to a pandas DataFrame
    data = list(collection.find())
    df = pd.DataFrame(data)

    # Drop the MongoDB ObjectId column (optional)
    df.drop(columns=["_id"], inplace=True)
    
    data_preprocessed = preprocess_mongo_data(df)
    
    data_dict = data_preprocessed.to_dict(orient="records")
    
    new_collection = db["preprocessed_tweet_data"]
    
    # Insert the data into the MongoDB collection
    new_collection.insert_many(data_dict)