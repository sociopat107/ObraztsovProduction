import requests


def get_video(picture):
    files = {'upload_file': picture}
    values = {'no_resize': 1}

    text = requests.post("http://upload-soft.photolab.me/upload.php", files=files, data=values).text

    values = {
        'image_url[1]': text,
        'template_name': "2355",
        'animated': "1",
    }
    video_url = requests.post("http://api-soft.photolab.me/template_process.php", data=values).text
    return video_url

