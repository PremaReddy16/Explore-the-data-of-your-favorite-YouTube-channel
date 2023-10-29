import streamlit as st
from streamlit_option_menu import option_menu
import Exploring, Migrate, Scrape, Visualize, Feedback

class MultiApp:
    def __init__(self):
        self.apps=[]
    def add_app(self,title,function):
        self.apps.append({"title": title, "function": function})
    def run():
        with st.sidebar:
            app=option_menu(menu_title='Analyzing',options=['Exploring','Scrape data', 'Flit data', 'Visualize data','Thanks'],
                icons=['chat-text-fill','chat-fill','info-circle-fill','bar-chart-fill','person-circle'],
                default_index=0, 
                styles={"icon": {"color": "purple", "font-size": "20px"}, 
                        "nav-link": {"color":"black","font-size": "18px", "text-align": "left", "margin":"0px", "--hover-color": "blue"},
                        "nav-link-selected": {"background-color": "#02ab21"},})

        if app == "Exploring":
            Exploring.app()
        if app == "Scrape data":
            Scrape.app()    
        if app == "Flit data":
            Migrate.app()        
        if app == 'Visualize data':
            Visualize.app()
        if app == 'Thanks':
            Feedback.app()                    
             
    run()            
