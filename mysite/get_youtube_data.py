# https://pythonchannel.com/myapp/youtuber/ のデータ取得用プログラム
import csv
import os
import time
import googleapiclient.discovery
from apiclient.discovery import build

count_day = 0

while True:
    try:
        api_key = "YouTube API Key" 
        my_youtube = build("youtube","v3",developerKey=api_key)
        request = my_youtube.search().list(
            part="snippet",
            type="channel",
            regionCode="JP",
            q="プログラミング",
            publishedBefore="2025-01-01T00:00:00Z",  #from  after  to  before
            publishedAfter="2019-12-01T00:00:00Z",
            maxResults=50,
            order= "date")

        response = request.execute()
        #total = response['pageInfo']['totalResults']
        total = len(response['items'])
        print('対象期間のチャンネル数： ' + str(total))

        i = 0
        channel_id_list = []
        channel_title_list = []
        channel_descriptions_list = []
        channel_subsc_list = []
        channel_video_id_list = []
        channel_video_img_list = []
        video_total = []
        video_total.append(total)

        while i < 50:
            print(i)
            try:
                channelID = response['items'][i]['snippet']['channelId']
                request2 = my_youtube.channels().list(
                    part="snippet,contentDetails,statistics",
                    id=channelID
                )
                response2 = request2.execute()
                channel_title = response2['items'][0]['snippet']['title']
                channel_descriptions = response2['items'][0]['snippet']['description']
                channel_subsc = response2['items'][0]['statistics']['subscriberCount']
                print(channel_title)

                channel_id_list.append(channelID)
                channel_title_list.append(channel_title)
                channel_descriptions_list.append(channel_descriptions)
                channel_subsc_list.append(channel_subsc)

                request3 = my_youtube.search().list(
                    part="snippet",
                    channelId=channelID,
                    order="date",
                    type="video"
                )
                response3 = request3.execute()
                video_id = response3['items'][0]['id']['videoId']
                video_img = response3['items'][0]['snippet']['thumbnails']['high']['url']
                channel_video_id_list.append(video_id)
                channel_video_img_list.append(video_img)

                i += 1
                time.sleep(5) #  LIMIT  100秒に 100 quotas
            except:
                print('ループ中に error ...')
                i += 1
                time.sleep(1)

        # Write CSV File
        with open('static/data/youtuber.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(channel_id_list)
            writer.writerow(channel_title_list)
            writer.writerow(channel_subsc_list)
            writer.writerow(channel_descriptions_list)
            writer.writerow(channel_video_id_list)
            writer.writerow(channel_video_img_list)
            writer.writerow(video_total)

        print( str(count_day) + "日目 ★FINISH★...")
        count_day += 1
        time.sleep(86400)
    
    except:
        print('error....')
        time.sleep(3)

    