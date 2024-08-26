import streamlit as st
from joblib import load
import pandas as pd
import re
import string

# Load your logistic regression model and tdidfVectorizer 
lr_loaded = load('logistic_regression_model.joblib')
tv_loaded = load('tfidfVectorizer.joblib')

# Create a function to clean text
def wordopt(text):
    text = text.lower()  # Lower case 
    text = re.sub('\[.*?\]', '', text)  # Remove anything with and within brackets
    text = re.sub('\\W', ' ', text)  # Removes any character not a letter, digit, or underscore
    text = re.sub('https?://\S+|www\.\S+', '', text)  # Removes any links starting with https
    text = re.sub('<.*?>+', '', text)  # Removes anything with and within < >
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)  # Removes any string with % in it 
    text = re.sub('\n', '', text)  # Remove new lines
    text = re.sub('\w*\d\w*', '', text)  # Removes any string that contains at least a digit with zero or more characters
    return text

# Prediction function 
def news_prediction(news):
    testing_news = {"text": [news]}
    new_def_test = pd.DataFrame(testing_news)
    new_def_test['text'] = new_def_test['text'].apply(wordopt)
    new_x_test = new_def_test['text']
    new_tfidf_test = tv_loaded.transform(new_x_test)
    pred_lr = lr_loaded.predict(new_tfidf_test)
    
    if pred_lr[0] == 0:
        return "This is Fake News! Don't Listen what the kopitiam uncle and aunty say."
    else:
        return "The News seems to be True!"

# Streamlit application starts here 
def main():
    # Title of your web app
    st.title("Fake News Prediction System")
    user_text = st.text_area("Enter a sentence to check if it's true or fake:", height=350)
   
    if st.button("Predict"):
        if user_text.strip():  # Check if the input text is not just empty or spaces
            news_pred = news_prediction(user_text)
            if news_pred.startswith("This is Fake News!"):  # Adjusted condition here
                st.error(news_pred, icon="🚨")
            else:
                st.success(news_pred)
                st.balloons()
        else:
            st.error("Please enter some text before analyzing the news article!")  # Updated error message for clarity

if __name__ == "__main__":
    main()
