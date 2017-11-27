
from harvestmedia.api.cloudsearch import CloudSearch
from harvestmedia.api.client import Client

api_key = 'e1d5d645d2d984e499e816a7a314dfbd610149f124c3373455c37ad75ab3ffccf444a04a10953b62'
webservice_url = 'https://service.harvestmedia.net/HMP-WS.svc'

client = Client(api_key=api_key, debug_level='DEBUG')

search_term_bundle = {'st_keyword_aggregated': '%'}
result_view = {'limit': '6', 'view': 'album', 'sort_predefined': 'ReleaseDate_Desc'}
recent_albums = CloudSearch.query.search_albums(search_term_bundle, result_view, client)

album_ids = []

for album in recent_albums:
    print album.name
    album_ids.append(album.id)

search_term_bundle = {'st_keyword_aggregated': '%', 'st_album': ','.join(album_ids)}
result_view = {'limit': '100', 'view': 'track'}
recent_tracks = CloudSearch.query.search_tracks(search_term_bundle, result_view, client)

for track in recent_tracks:
    print track.displaytitle