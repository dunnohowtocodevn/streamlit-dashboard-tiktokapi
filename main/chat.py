import pandas as pd
import streamlit as st 
import pandasai
from pandasai import SmartDataframe
from pandasai.llm.openai import OpenAI
from pandasai.responses.response_parser import ResponseParser

#Integrate ChatGPT into the chat using OpenAI API
def app():

    #Parse different types of response
    class StreamlitResponse(ResponseParser):
        def init(sel, context) -> None:
            super().init(context)
        def format_dataframe(self, result):
            st.dataframe(result["value"])
            return
        def format_plot(self, result):
            st.image(result["value"])
        def format_other(self, result):
            st.write(result["value"])
    
    st.write("CHAT WITH YOUR DATABASE")
  
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
    history = []
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the uploaded CSV file
        df = pd.read_csv(uploaded_file)

        # Display the data
        st.write("### CSV File")
     

        # Perform actions on the data
        
        with st.expander("Dataframe Preview"):
            st. write(df.tail(5))

        query = st.text_area("Work with dataframe")

        #Send the query to the ChatGPT
        if query:
            try:
                llm = OpenAI ()
                query_engine = pandasai.SmartDataframe(df, config={"llm":llm, "response_parser": StreamlitResponse})

                result = query_engine.chat(query)
                history.append({"Query": query, "Result": result})
                
            except Exception as e:
                st.error(f"An error occured: {str(e)}")


    else:
        st.warning("Upload a CSV file to get started.")
        df = pd.read_csv("avocado.csv")

    

    


 