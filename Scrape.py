import time
import streamlit as st
import googleapiclient.discovery
from datetime import datetime
import pymongo
connection_string=f"""mongodb+srv://premavinayaki:Ursyash8@cluster0.ijigeb9.mongodb.net/?retryWrites=true&w=majority&appName=AtlasApp"""
client = pymongo.MongoClient(connection_string)

def app():    

    st.title('Scrape & Store')
    st.write('_Extract and store your channel data by just giving the channel id_')
    st.write("(_Hint: Goto channel's home page > click about > share > copy channel id_)")                  
    
 # BUILDING CONNECTION WITH YOUTUBE API
    api_service_name= "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyBjLgKtdAMdYqRx0Dpi60RFsIrcfcWZKv4"
    youtube = googleapiclient.discovery.build(
                api_service_name, api_version, developerKey = DEVELOPER_KEY)

# FUNCTION TO GET CHANNEL DETAILS
    def channeldetails(channel_id):

        request = youtube.channels().list(
            part="snippet,contentDetails,statistics",
            id=channel_id)    
        response = request.execute()
        c_stats=dict(Channel_id=response['items'][0]['id'],
                    Channel_name=response['items'][0]['snippet']['title'],
                    Channel_description=response['items'][0]['snippet']['description'],
                    Viewcount=response['items'][0]['statistics']['viewCount'],
                    Subscribers=response['items'][0]['statistics']['subscriberCount'],
                    Total_videos=response['items'][0]['statistics']['videoCount'],
                    Upload_id=response['items'][0]['contentDetails']['relatedPlaylists']['uploads'])
        return c_stats    

# FUNCTION TO GET PLAYLIST DETAILS
    def playlists(channel_id):
        pls=[]          
        request = youtube.playlists().list(
                    part="snippet,contentDetails",
                    channelId=channel_id,
                    maxResults=50)                            
        response = request.execute()                
        for k in range(len(response['items'])):    
            p_stats=dict(Channel_id=response['items'][k]['snippet']['channelId'],
                        Playlist_id=response['items'][k]['id'],
                        Playlist_name=response['items'][k]['snippet']['title'],
                        Playlist_count=response['items'][k]['contentDetails']['itemCount'])
            pls.append(p_stats)                    
        return pls    

# FUNCTION TO GET VIDEO IDS
    def get_video_ids(Upload_id):
        video_ids=[]    
        request = youtube.playlistItems().list(
            part="snippet,contentDetails",
            maxResults=50,
            playlistId=Upload_id)
        response = request.execute()    
        for i in range(len(response['items'])):
            video_ids.append(response['items'][i]['contentDetails']['videoId'])        
        next_page_token=response.get('nextPageToken')
        more_pages=True    
        while more_pages:
            if next_page_token is None:
                more_pages=False
            else:
                request=youtube.playlistItems().list(
                        part='contentDetails',
                        playlistId=Upload_id,
                        maxResults=50,
                        pageToken=next_page_token)
                response=request.execute()            
                for i in range(len(response['items'])):
                    video_ids.append(response['items'][i]['contentDetails']['videoId'])                    
                next_page_token=response.get('nextPageToken')               
        return video_ids    

# FUNCTION TO GET VIDEO DETAILS
    def get_video_details(youtube, video_ids):
        all_video_stats = []    
        for j in range(0, len(video_ids), 50):
            request = youtube.videos().list(
                part="snippet,contentDetails,statistics",
                id=",".join(video_ids[j:j+50]))
            response = request.execute()        
            for i in range(len(response['items'])):
                v_stats=dict(Video_id=response['items'][i]['id'],
                                Channel_id=response['items'][i]['snippet']['channelId'],
                                Title=response['items'][i]['snippet']['title'],
                                Video_description=response['items'][i]['snippet']['description'],
                                Thumbnails=response['items'][i]['snippet']['thumbnails'].get('url'),
                                Published_date=datetime.fromisoformat(response['items'][i]['snippet']['publishedAt'].replace('z','')),
                                Views=response['items'][i]['statistics']['viewCount'],
                                Likes=response['items'][i]['statistics'].get('likeCount'),
                                Comments=response['items'][i]['statistics'].get('commentCount'))
                all_video_stats.append(v_stats)
        return all_video_stats    

# FUNCTION TO GET COMMENT DETAILS
    def get_comment_details(video_ids):
            allcomments=[]
            for j in video_ids:
                try:     
                    request = youtube.commentThreads().list(
                                part="snippet,replies",
                                videoId=j,
                                maxResults=100)
                    response = request.execute()                    
                    for i in range(len(response['items'])):
                            cm_stats=dict(Comment_id=response['items'][i].get('id'),
                                            Video_id=response['items'][i]['snippet']['videoId'],
                                        Comments=response['items'][i]['snippet']['topLevelComment']['snippet'].get('textOriginal'),
                                        Comment_author=response['items'][i]['snippet']['topLevelComment']['snippet'].get('authorDisplayName'),
                                        Commented_on=datetime.fromisoformat(response['items'][i]['snippet']['topLevelComment']['snippet'].get('publishedAt').replace('z','')))                                 
                            allcomments.append(cm_stats)
                except:
                    pass                
            return allcomments    

# FUNCTION THAT COMBINES THE ABOVE FUNCTIONS
    def main(channel_id):
        datacombo=channeldetails(channel_id)
        pl=playlists(channel_id)
        video_ids=get_video_ids(datacombo['Upload_id'])
        vs=get_video_details(youtube, video_ids)
        cm=get_comment_details(video_ids)
        
        data = {'Channel details': datacombo,
                'Playlists': pl,
                'Video details': vs,
                'Comment details': cm}
        return data    

#USER INPUT THAT EXTRACTS AND DISPLAY THE DATA
    channel_id = st.sidebar.text_input('Enter Channel Id')
    if st.sidebar.button("Scrape"):
       d=main(channel_id)
       st.write(d)

#FUNCTION TO STORE THE EXTRACTED DATA IN MONGODB
    if 'clicked' not in st.session_state:
        st.session_state.clicked = False

    def click_button():
# Bridging a connection with MongoDB Atlas and the database
        connection_string=f"""mongodb+srv://premavinayaki:Ursyash8@cluster0.ijigeb9.mongodb.net/?retryWrites=true&w=majority&appName=AtlasApp"""
        client = pymongo.MongoClient(connection_string)
        db = client.get_database('YT-db')
        collections=db.ChannelStatistics
        collections.insert_one(d)
        st.session_state.clicked = True 
    
    st.button("Save", on_click=click_button)
    
    if st.session_state.clicked:
            with st.spinner('Please wait...'):
                time.sleep(5)
            st.success("Channel Saved in MongoDB Successfully😎!!")
    
                
        



    
    

