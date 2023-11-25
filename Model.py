# importing files
import pickle 
import nltk
from nltk.corpus import stopwords
import string

from nltk.stem.porter import PorterStemmer
ps=PorterStemmer()

def transform_text(origtext):
    text = origtext.lower()
    
    text = nltk.word_tokenize(text)
    
    y = []
    for i in text:
        if i.isalnum():
            y.append(i)
    
    text = y[:]
    y.clear()
    
    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)
            
    text = y[:]
    y.clear()
    
    for i in text:
        y.append(ps.stem(i))
    
            
    return " ".join(y)


def classify_email(text):
    tfidf=pickle.load(open('vectorizer.pkl','rb'))
    model=pickle.load(open('model.pkl','rb'))
    #transforming
    transformed_sms=transform_text(text)
    #vectorizer
    tf=tfidf.transform([transformed_sms])
    #predict
    result=model.predict(tf)[0]
  
    #result
    if result==1:
        return "Spam"
    elif result==0: 
       return "Normal"
    # else:
    #    return "Unknown Class" 

s=classify_email("Are you happy with your recent purchase? Thank You! RATE AND REVIEW MANIBAM IMPEX Sauce Set Plastic 1 2 3 4 5 Find all your reviews under My accounts > My ratings and reviews. We hope you enjoy emails from Flipkart. If you wish to unsubscribe, please click here. ")
print(s)