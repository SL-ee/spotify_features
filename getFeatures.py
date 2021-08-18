import spotipy
import requests
import pandas as pd

cid = 'Your client ID'
secret = 'Your client secret ID'
AUTH_URL = 'https://accounts.spotify.com/api/token'

# 토큰 얻기
auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': cid,
    'client_secret': secret,
})
auth_response_data = auth_response.json()
access_token = auth_response_data['access_token']

headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}

BASE_URL = 'https://api.spotify.com/v1/'

# 앨범에서 트랙 구하기
spotifyObject = spotipy.Spotify(access_token)

code_ids = []
tracks = []

# 앨범 코드를 입력해야 하는 부분
track_list = spotifyObject.album_tracks('26pelVOow8ODvBktJbDiua')
track_items = track_list['items']

for item in track_items:
    code_ids.append(item['uri'][14:])
    tracks.append(item['name'])

danceability = []
energy = []
speechiness = []
acousticness = []
liveness = []
valence = []

for code_id in code_ids:
    r = requests.get(BASE_URL + 'audio-features/' + str(code_id), headers=headers)
    ft_dic = r.json()
    try:
        danceability.append(ft_dic['danceability'])
        energy.append(ft_dic['energy'])
        speechiness.append(ft_dic['speechiness'])
        acousticness.append(ft_dic['acousticness'])
        liveness.append(ft_dic['liveness'])
        valence.append(ft_dic['valence'])
    except:
        danceability.append('N/A')
        energy.append('N/A')
        speechiness.append('N/A')
        acousticness.append('N/A')
        liveness.append('N/A')
        valence.append('N/A')

# 최종 데이터 추출
features = pd.DataFrame(
    {
        'track': tracks,
        'danceability': danceability,
        'energy': energy,
        'speechiness': speechiness,
        'acousticness': acousticness,
        'liveness': liveness,
        'valence': valence
    })

excel_test.to_excel("D:/test.xlsx", index=False)
