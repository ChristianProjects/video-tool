from typing import List, Dict, Any, Optional
from pytube import Playlist, YouTube, Stream
import os, cv2


class Video:
    title: str
    path: str
    stream: Optional[Stream]

    def __init__(self, title: str, path: str, stream: Optional[Stream] = None):
        self.title = title
        self.path = path
        self.stream = stream

    def index_video(self) -> None:
        # based on https://stackoverflow.com/questions/33311153/python-extracting-and-saving-video-frames
        # thanks to @fireant user and the cv2 guys for the answer
        # and @GShocked and @Chris users for the question 
        vid = cv2.VideoCapture(self.path)
        success,image = vid.read()
        i = 0
        # i = (30 * 60) * 100 + 30 * 54
        max_count = vid.get(cv2.CAP_PROP_FRAME_COUNT)
        framerate = 30
        minute = framerate * 60
        step = 1
        while success:
            # if i >= 60 * 60 * 240:
            #     break
            if i < minute * 10:
                i += step
                continue
            #     continue
            print('frames/frame%d.%d' % (i // minute, i % minute))
            vid.set(1, i)
            cv2.imwrite("frames/frame%d.%d.jpg" % (i // minute, i % minute), image)     # save frame as JPEG file      
            success,image = vid.read()
            print('Read a new frame: ', success)
            i += step

            # break
            # vid.set(1, i)
            
            
class Tool:
    name: str
    videos: List[Any]

    def __init__(self, name: str) -> None:
        self.name = name
        self.videos = []

    def download(self, playlist_url: str, start: int = 0, limit: int = 5, folder: Optional[str] = None) -> None:
        # invoke youtube and donwload up to limit
        # https://github.com/nficano/pytube docs and examples
        # based on this!
        
        playlist = Playlist(playlist_url)
        
        i = 0
        print(dir(playlist))
        print(playlist.title())
        print(playlist.video_urls)
        for video in playlist:
            print(i, start, start + limit)
            if i < start:
                i += 1
                continue
            if i >= start + limit:
                break
            # TODO parallel?
            print('downloading video: ', video)
            yt = YouTube(video)
            # print(type(yt.streams))
            stream = yt.streams.get_highest_resolution()
            stream.download(output_path=folder)
            yt.register_on_progress_callback(lambda *args: self.on_progress(*args))
            print('  completed ', yt.title)
            self.videos.append(Video(yt.title, stream.get_file_path(), stream))
            i += 1

    def on_progress(self, stream: Stream, chunk: bytes, bytes_remaining: int) -> None:
        print(chunk)
        print('  ', '.' * len(chunk))

    def index(self) -> None:
        for video in self.videos:
            video.index_video()
    



    def load_files(self, folder: str, extension: str) -> None:
        for (path, dirs, files) in os.walk(folder):
            for file in files:
                # print(file, extension)
                if file.endswith('.' + extension):
                    self.videos.append(Video(file.rpartition('.')[0], os.path.abspath(os.path.join(folder, file))))
            break

def run():
    print('run')
    tool = Tool('Emanuil')
    # tool.download('https://www.youtube.com/playlist?list=PLbytjJb6HRk4HgPCsHUvw4LIsVoADybWN', 0, 10, 'plovdiv/')
    tool.load_files('plovdiv/', 'mp4')
    # tool2 = Tool('test')
    # tool2.download('https://www.youtube.com/playlist?list=PLynhp4cZEpTbRs_PYISQ8v_uwO0_mDg_X', 4, 1)
    # 1.40.54
    tool.index()

run()

