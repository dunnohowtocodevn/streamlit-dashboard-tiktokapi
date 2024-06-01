import streamlit as st
from streamlit_option_menu import option_menu

#Import the pages
import home, chat, about
st.set_page_config(
        page_title="DATALASIS",
)


class MultiApp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, func):

        self.apps.append({
            "title": title,
            "function": func
        })

    def run():
        
        #Customise the sidebar
        with st.sidebar:        
            app = option_menu(
                menu_title='Data Analysis ',
                options=['Home','ChatBot','About'],
                icons=['house-fill','chat-fill','info-circle-fill'],
                menu_icon='chat-text-fill',
                default_index=1,
                styles={
                    "container": {"padding": "5!important","background-color":'black'},
                    "icon": {"color": "white", "font-size": "23px"}, 
                    "nav-link": {"color":"white","font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "blue"},
                    "nav-link-selected": {"background-color": "#02ab21"},}
                )

        
        if app == "Home":
            home.app()
        if app == "ChatBot":
            chat.app()    
        if app == 'About':
            about.app()    
             
          
            
    run()            
         