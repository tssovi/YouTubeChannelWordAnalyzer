import re
import youtube_dl
from pycaption import WebVTTReader
from os import remove
from urllib.parse import urlencode

from temp_file_storage import TempStorage


class Download():

    def __init__(self, options: dict = {}):
        self.base_url = 'http://www.youtube.com/watch?v='
        self.options = {
            'skip_download': True,
            'writeautomaticsub': True,
            'outtmpl': 'subtitle_%(id)s',
        }
        self.options.update(options)
        self.logs = []

    def get_closed_captions(self, video_id, language: 'en'):
        result = self.get_subtitles(video_id, language)
        sub_str = ""

        if result != 0:
            message = 'Unable to download and extract captions: {0}'.format(result)
            self.logs.append(message)

        storage = TempStorage(video_id, language)
        file_path = storage.get_temp_file_path()
        try:
            with open(file_path) as f:
                sub_str = self.get_captions_from_output(f.read(), language)
            storage.remove_temp_file()

            message = 'Successfully scraped closed captions for this {0} video id.'.format(video_id)
            self.logs.append(message)
        except:
            message = 'No closed captions found for this {0} video id.'.format(video_id)
            self.logs.append(message)
            pass
        return sub_str, self.logs

    def get_subtitles(self, video_id, language: 'en'):
        options = self.options
        if language:
            options['subtitleslangs'] = [*options.get('subtitleslangs', []), language]

        with youtube_dl.YoutubeDL(options) as ydl:
            try:
                return ydl.download([self.generate_url_from_video_id(video_id)])
            except youtube_dl.utils.DownloadError as error:
                message = "Unable to download captions: {0}".format(str(error))
                self.logs.append(message)
            except youtube_dl.utils.ExtractorError as error:
                message = "Unable to extract captions: {0}".format(str(error))
                self.logs.append(message)
            except Exception as error:
                message = "Unknown exception occurred downloading and extracting captions: {0}".format(str(error))
                self.logs.append(message)

    def generate_url_from_video_id(self, video_id):
        return '{0}{1}'.format(self.base_url, video_id)

    def get_captions_from_output(self, sub_str, language: 'en'):
        reader = WebVTTReader()

        temp_final = ''
        for caption in reader.read(sub_str, language).get_captions(language):
            stripped = self.remove_time_from_caption(str(caption).replace(r'\n', "\n"))
            temp_final += stripped

        final = ''
        previous = ''
        for line in temp_final.split("\n"):
            if previous != line:
                final += "\n" + line
            previous = line

        return final.replace("\n", ' ')[1:]

    def remove_time_from_caption(self, caption):
        caption = caption[1:-1]
        return re.sub(r"^.*?\n", "\n", caption)

