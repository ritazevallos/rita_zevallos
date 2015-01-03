from django.core.management.base import BaseCommand
from because.models import Beginning, Ending
import musixmatch.ws
import re

class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def _populate(self):

        apikey = '5a4d1599e0142ad780153d73bae73145'
        because_re = re.compile('because', re.IGNORECASE)
        because_phrase1_re = re.compile("^[Bb]ecause[A-Za-z'\"\\s]+[,\\s\n]+ [A-Za-z,;'\"\\s]+[.?!]$")
        because_phrase2_re = re.compile('', re.IGNORECASE)

        try:
            search_response = musixmatch.ws.track.search(q_lyrics='because', apikey=apikey, page_size='10')
            track_list = search_response['body']
            for track in track_list:
                info = track['track']
                track_name = info['track_name']
                artist_name = info['artist_name']
                track_id = info['track_id']

                lyrics_response = musixmatch.ws.track.lyrics.get(track_id=track_id, apikey=apikey)
                lyrics_json = lyrics_response['body']['lyrics']
                lyrics_body = lyrics_json['lyrics_body']

                if lyrics_body and re.search(because_re, lyrics_body):
                    lyrics_copyright = lyrics_json['lyrics_copyright']
                    tracking = lyrics_json['script_tracking_url'] # html_tracking_url, #pixel_tracking_url
                    phrase_matches = re.findall(because_phrase1_re, lyrics_body)
                    phrase_matches.extend(re.findall(because_phrase2_re, lyrics_body))
        except musixmatch.api.Error, e:
            pass

        beginning = Beginning(text='testing populate beginning')
        beginning.save()

        ending = Ending(text='testing ending', beginning=beginning)
        ending.save()

    def handle(self, *args, **options):
        self._populate()