from urllib.parse import urlparse

import isodate
from django.conf import settings
from pyyoutube import Api

YOUTUBE_KEY = settings.YOUTUBE_KEY

api = Api(api_key=YOUTUBE_KEY)


def get_youtube_data(url):
    if "youtube.com/" in url:
        new_data = {}
        query_data = urlparse(url).query
        video_id = "".join(query_data.split("v=")).split("&")[0]
        video = api.get_video_by_id(video_id=video_id)
        video_data = video.items[0].to_dict()
        title = video_data["snippet"]["title"]
        description = video_data["snippet"]["description"]
        image_thumbnails = video_data["snippet"]["thumbnails"]
        if image_thumbnails["maxres"] is None:
            preview = image_thumbnails["high"]["url"]
        else:
            preview = image_thumbnails["maxres"]["url"]
        duration = isodate.parse_duration(
            video_data["contentDetails"]["duration"]
        )
        author = video_data["snippet"]["channelTitle"]
        date = video_data["snippet"]["publishedAt"]
        new_data.update(
            dict(
                video_id=video_id,
                title=title,
                description=description,
                preview=preview,
                author=author,
                duration=duration,
                date=date,
            )
        )
        return new_data
    return url
