import streamlit as st
import json
import os

#NLP PKGS
from spacy.lang.en import English
from spacy.matcher import Matcher

def load_nlp(data):
    nlp = English()
    matcher = Matcher(nlp.vocab)
    for key, patterns in data.items():
        #st.write(patterns)
        matcher.add(key,patterns)
    return nlp,matcher

def text_analyzer(my_text,nm):
    nlp,m = nm
    doc =nlp(my_text)
    tokens = [token.text for token in doc]
    return tokens

def match_analyzer(my_text,nm):
    nlp,matcher = nm
    doc =nlp(my_text)
    matches = matcher(doc)

    temp = {doc[start:end] : doc.vocab.strings[match_id] for match_id, start, end in matches}
    res = {val : [k for k,v in temp.items() if val == v ] for key, val in temp.items()}

    return res



def main():

    os.system( "taskset -pc 0-1 %d > /dev/null" % os.getpid() )
    

    st.title("Test Match")

    uploaded_file = st.file_uploader("Choose a file",type=['json'])
    if uploaded_file is not None:
        #data = json.load(uploaded_file)
        file_details = {"FileName":uploaded_file.name,"FileType":uploaded_file.type,"FileSize":uploaded_file.size}
        st.write(file_details)
        data = json.load(uploaded_file) 
        #st.success(data)
        

    

    Text = st.text_area("Enter Your Text","Type Here")
   
    #Tokenization
    if st.checkbox("Show Tokens"):
        st.success(text_analyzer(Text,load_nlp(data)))
    if st.checkbox("Show Matches"):
        st.success(match_analyzer(Text,load_nlp(data)))
    
if __name__ == '__main__':
    main()