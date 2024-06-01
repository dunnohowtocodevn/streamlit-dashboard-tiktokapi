import streamlit as st
from data import collect_data
from dashboard import analyse_data

#Ask for the user's id and analyse data
def app():
    st.title('TikTok Shop Data Analysis')

    # Collect data
    user_id = st.text_input('Enter TikTok User ID')
    if st.button('Collect Data'):
        collect_data(user_id)
        st.success('Data collected successfully!')

        # Analyse data
        if st.button('Analyse Data'):
            analysis_result = analyse_data()
            st.write('Analysis Result:')
            st.write(analysis_result)
