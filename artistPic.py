import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


spootify = spotipy.Spotify(
    client_credentials_manager = SpotifyClientCredentials(
        client_id="",
        client_secret=""
    )
)
 
def getArtistPic(x):
    results = spootify.search(q='artist:' + x, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        artist = items[0]
        if len(artist['images']) > 0:
            yz = artist['images'][0]['url']
        else:
            yz = "https://images.squarespace-cdn.com/content/v1/5c475f7136099bab807042c6/1577432047348-GAZPK9UUPLH07FH7T3QT/ke17ZwdGBToddI8pDm48kGC1EuUbdtdTk4BzQJRibQR7gQa3H78H3Y0txjaiv_0fDoOvxcdMmMKkDsyUqMSsMWxHk725yiiHCCLfrh8O1z5QHyNOqBUUEtDDsRWrJLTmG94TGNuzCcCPVStE9JyN8GpaXZ48x6mVY7HcqmFkgkOAZupcJ-6kHFSGoa_96eZM/SquareSpace+Cover.jpg?format=1000w"
    else:
        yz = "https://images.squarespace-cdn.com/content/v1/5c475f7136099bab807042c6/1577432047348-GAZPK9UUPLH07FH7T3QT/ke17ZwdGBToddI8pDm48kGC1EuUbdtdTk4BzQJRibQR7gQa3H78H3Y0txjaiv_0fDoOvxcdMmMKkDsyUqMSsMWxHk725yiiHCCLfrh8O1z5QHyNOqBUUEtDDsRWrJLTmG94TGNuzCcCPVStE9JyN8GpaXZ48x6mVY7HcqmFkgkOAZupcJ-6kHFSGoa_96eZM/SquareSpace+Cover.jpg?format=1000w"
    return yz

    

