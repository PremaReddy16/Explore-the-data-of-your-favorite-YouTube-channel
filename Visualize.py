import streamlit as st
from sqlalchemy import create_engine
import plotly.express as px
import pandas as pd
import mysql.connector
conn = st.experimental_connection('youtube', 'sql',url="mysql://premareddy:myloveyash@127.0.0.1:3306/youtube")
con = mysql.connector.connect(user='premareddy',password='myloveyash',host='127.0.0.1',database='youtube')
cursor=con.cursor()
engine = create_engine("mysql://premareddy:myloveyash@127.0.0.1:3306/youtube")

def app():

    st.title('Visualize')
    st.write(':orange[Select any questions to get Insights]')
    questions = st.selectbox('Questions',['None','1. What are the names of all the videos and their corresponding channels?',
                                        '2. Which channels have the most number of videos, and how many videos do they have?',
                                        '3. What are the top 10 most viewed videos and their respective channels?',
                                        '4. How many comments were made on each video, and what are their corresponding video names?',
                                        '5. Which videos have the highest number of likes, and what are their corresponding channel names?',
                                        '6. What is the total number of likes for each video, and what are their corresponding video names?',
                                        '7. What is the total number of views for each channel, and what are their corresponding channel names?',
                                        '8. What are the names of all the channels that have published videos in the year 2022?',
                                        '9. What is the total number of playlists for each channel and their corresponding names?',
                                        '10. Which videos have the highest number of comments, and what are their corresponding channel names?'])

    if questions=='1. What are the names of all the videos and their corresponding channels?':
        df=conn.query("SELECT chss.Channel_name, video_ss.Video_name FROM chss INNER JOIN video_ss ON chss.Channel_id=video_ss.Channel_id;")
        st.dataframe(df) 
        
    elif questions=='2. Which channels have the most number of videos, and how many videos do they have?':
        cursor.execute("""SELECT Channel_name As Channel_Name, Total_videos as Total_Videos FROM chss ORDER BY Total_videos DESC""")
        df=pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
        st.write(df)
        st.write("### :green[Number of videos in each channel: ]")
        fig=px.bar(df, x=cursor.column_names[0], y=cursor.column_names[1],orientation='v', color=cursor.column_names[0])
        st.plotly_chart(fig,use_container_width=True)

    elif questions=='3. What are the top 10 most viewed videos and their respective channels?':
        cursor.execute("""SELECT Channel_name, Video_name, video_ss.Views FROM chss INNER JOIN video_ss ON chss.Channel_id=video_ss.Channel_id
                       ORDER BY Views DESC LIMIT 10""")
        df=pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
        st.write(df)
        st.write("### :green[Top 10 most viewed videos: ]")
        fig=px.bar(df, x=cursor.column_names[2], y=cursor.column_names[1],orientation='h', color=cursor.column_names[0])
        st.plotly_chart(fig,use_container_width=True)

    elif questions=='4. How many comments were made on each video, and what are their corresponding video names?':
        df=conn.query("SELECT Video_name AS Video_Name, TotalComments AS CommentCount FROM video_ss ORDER BY TotalComments DESC;")
        st.dataframe(df)
        
    elif questions=='5. Which videos have the highest number of likes, and what are their corresponding channel names?':
        cursor.execute("""SELECT Channel_name, Video_name, Likes FROM chss INNER JOIN video_ss ON chss.Channel_id=video_ss.Channel_id 
                       ORDER BY Likes DESC LIMIT 15""")
        df = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
        st.write(df)
        st.write("### :green[Top 15 most liked videos :]")
        fig = px.bar(df,x=cursor.column_names[2],y=cursor.column_names[1],orientation='h',color=cursor.column_names[0])
        st.plotly_chart(fig,use_container_width=True)
        
    elif questions=='6. What is the total number of likes for each video, and what are their corresponding video names?':        
        cursor.execute("""SELECT Video_name AS Video_Name, Likes AS LikeCount FROM video_ss ORDER BY Likes DESC""")
        df = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
        st.write(df)
         
    elif questions == '7. What is the total number of views for each channel, and what are their corresponding channel names?':
        cursor.execute("""SELECT Channel_name AS Channel_Name, Viewcount AS Views FROM chss ORDER BY Viewcount DESC""")
        df = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
        st.write(df)
        st.write("### :green[Channels vs Views :]")
        fig = px.bar(df,x=cursor.column_names[0],y=cursor.column_names[1],orientation='v',color=cursor.column_names[0])
        st.plotly_chart(fig,use_container_width=True)
        
    elif questions == '8. What are the names of all the channels that have published videos in the year 2022?':
        cursor.execute("""SELECT Channel_name, Published_date FROM chss INNER JOIN video_ss ON chss.Channel_id=video_ss.Channel_id
                            WHERE year(Published_date)=2022""")
        df = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
        st.write(df)

    elif questions == '9. What is the total number of playlists for each channel and their corresponding names?':
        cursor.execute("""SELECT Channel_name, Playlist_name, Playlist_count FROM chss INNER JOIN plss ON chss.Channel_id=plss.Channel_id""")
        df = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
        st.write(df)

    elif questions == '10. Which videos have the highest number of comments, and what are their corresponding channel names?':
        cursor.execute("""SELECT Channel_name, Video_name,TotalComments FROM chss INNER JOIN video_ss ON chss.Channel_id=video_ss.Channel_id 
                       ORDER BY TotalComments DESC LIMIT 10""")
        df = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
        st.write(df)
        st.write("### :green[Videos with most comments :]")
        fig = px.bar(df,x=cursor.column_names[1],y=cursor.column_names[2],orientation='v',color=cursor.column_names[0])
        st.plotly_chart(fig,use_container_width=True)

                
    