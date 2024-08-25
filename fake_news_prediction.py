import streamlit as st
from joblib import load
import pandas as pd
import re
import string

# load dataset
fake_sample= pd.read.csv(fake.csv)
true_sample=pd.read_csv(true.csv)



# Load your logistic regression model and tdidfVectorizer 
lr_loaded = load('logistic_regression_model.joblib')
tv_loaded = load('tfidfVectorizer.joblib')

 # create a function to clean text
def wordopt(text):
    text = text.lower() # lower case 
    text = re.sub('\[.*?\]','',text) # remove anything with and within brackets
    text = re.sub('\\W',' ',text) # removes any character not a letter, digit, or underscore
    text = re.sub('https?://\S+|www\.\S+','',text) # removes any links starting with https
    text = re.sub('<.*?>+','', text) # removes anything with and within < >
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text) # removes any string with % in it 
    text = re.sub('\n','',text) # remove next lines
    text = re.sub('\w*\d\w*','', text) # removes any string that contains atleast a digit with zero or more characters
    return text
  

# prediction function 
def news_prediction(news):
  testing_news = {"text":[news]}
   new_def_test = pd.DataFrame(testing_news)
   new_def_test['text'] = new_def_test['text'].apply(wordopt)
   new_x_test = new_def_test['text']
   new_tfidf_test = vc.transform(new_x_test)
   pred_lr = lr.predict(new_tfidf_test)
    
if (pred_lr[0] == 0):
      return "This is Fake News!"
   else:
      return "The News seems to be True!"
    
 # Streamlit application starts here 
 def main():
     # Title of your web app
     st.title("Fake News Prediction System")

     user_text = st.text_area("Enter a sentence to check if it's true or fake:")

 # predict buttom
 	if st.button('Article/News Analysis Result'):
 		if user_input:
		 news_pred = news_prediction(user_text)
		 if (news_pred == "This is Fake News!"):
    			 st.error(news_pred, icon="🚨")
   		else:
     		st.success(news_pred)
      	        st.balloons()

 if __name__ == '__main__':
     main()
