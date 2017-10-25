
from harvestmedia.api.cloud_search import CloudSearch
from harvestmedia.api.client import Client

api_key = 'e1d5d645d2d984e499e816a7a314dfbd610149f124c3373455c37ad75ab3ffccf444a04a10953b62'
webservice_url = 'https://service.harvestmedia.net/HMP-WS.svc'

client = Client(api_key=api_key, debug_level='DEBUG')

recent_albums = CloudSearch.query.get_recent_albums(client)

album_ids = []

for album in recent_albums:
    print album.name
    album_ids.append(album.id)

recent_tracks = CloudSearch.query.get_tracks_by_albums(album_ids, client)

for track in recent_tracks:
    print track.displaytitle