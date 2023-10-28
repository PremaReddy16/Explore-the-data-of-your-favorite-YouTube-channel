from pydoc import doc
import time
import streamlit as st
import mysql.connector
import pymongo
conn = st.experimental_connection('youtube', 'sql',url="mysql://premareddy:myloveyash@127.0.0.1:3306/youtube")
con = mysql.connector.connect(user='premareddy',password='myloveyash',host='127.0.0.1',database='youtube')
cursor=con.cursor()

def app():

    st.title('Transformation')
    st.write('_Here the saved channel data will be flitted to Mysql from MondoDB_')     
    client = pymongo.MongoClient(f"""mongodb+srv://premavinayaki:Ursyash8@cluster0.ijigeb9.mongodb.net/?retryWrites=true&w=majority&appName=AtlasApp""")
    db = client['YT-db']
    collections=db['ChannelStatistics']
                
    def channel_names():   
        Channels = []             
        for i in collections.find():
            Channels.append(i['Channel details']['Channel_name'])
        return Channels
    names=channel_names()
    
    def insertdocs(details):
        sql_ch='''INSERT INTO CHSS(CHANNEL_ID, CHANNEL_NAME, CHANNEL_DESCRIPTION, Viewcount, SUBSCRIBERS, TOTAL_VIDEOS, UPLOAD_ID) values (%s, %s, %s, %s, %s, %s, %s)'''
        val=tuple(details['Channel details'].values())
        cursor.execute(sql_ch, val)

        plys_list ='''INSERT INTO PLSS(CHANNEL_ID, PLAYLIST_ID, PLAYLIST_NAME, PLAYLIST_COUNT) values (%s, %s, %s, %s)'''
        for i in details['Playlists']:
            val=tuple(i.values())
            cursor.execute(plys_list, val)
        
        vslist ='''INSERT INTO VIDEO_SS(VIDEO_ID, CHANNEL_ID, VIDEO_NAME, DESCRIPTION, THUMBNAILS, PUBLISHED_DATE, VIEWS, LIKES, TOTALCOMMENTS)values (%s, %s, %s, %s, %s, %s, %s, %s, %s)'''
        for j in details['Video details']:
            val=tuple(j.values())
            cursor.execute(vslist, val)
            
        cmdss ='''INSERT INTO COMMENTSS(COMMENT_ID, VIDEO_ID, COMMENTS, COMMENT_AUTHOR, COMMENTED_ON) values (%s, %s, %s, %s, %s)'''
        for k in details['Comment details']:
            val=tuple(k.values())
            cursor.execute(cmdss, val)
        con.commit()

    ch=st.sidebar.selectbox('Select channel', options=names)
    if st.sidebar.button('Submit'):
        doc=collections.find_one({'Channel details.Channel_name':ch},{'_id':0})
        st.write(doc)   
       
    if 'clicked' not in st.session_state:
            st.session_state.clicked = False

    def click_button():
            doc=collections.find_one({'Channel details.Channel_name':ch},{'_id':0})
            insertdocs(doc)
            st.session_state.clicked = True

    st.button("Go to sql", on_click=click_button)

    if st.session_state.clicked:
        with st.spinner('Please wait...'):
            time.sleep(5)
            st.success("Channel Migrated Successfully😎!!")
    

    