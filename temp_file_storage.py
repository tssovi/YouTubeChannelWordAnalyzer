import re
import os


class TempStorage():

    def __init__(self, video_id, language: 'en'):
        self.video_id = video_id
        self.language = language

    def get_temp_file_path(self):
        if re.search(r'[^\w-]', self.video_id):
            raise ValueError('Invalid video id attempting to write to filesystem')

        return 'subtitle_{0}.{1}.vtt'.format(
            re.sub(r'[^\w-]', '', self.video_id), self.language)

    def remove_temp_file(self):
        os.remove(self.get_temp_file_path())

