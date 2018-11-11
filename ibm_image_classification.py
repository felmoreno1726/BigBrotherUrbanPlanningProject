import requests

url = 'https://s3-external-1.amazonaws.com/media.twiliocdn.com/ACddc59696c52e6d717778a4621d700dc1/f139ae88147b7b7cba895dc601a436a8'
r = requests.get(url, allow_redirects=True)
open('google.jpg', 'wb').write(r.content)




import json
from watson_developer_cloud import VisualRecognitionV3

visual_recognition = VisualRecognitionV3(
    '2018-03-19',
    iam_apikey='ojkv2WbTgyksiFHUeXmmPsYDBoVM2GmVJN9HdsbSF7lw')

with open('./google.jpg', 'rb') as images_file:
    classes = visual_recognition.classify(
        images_file,
        threshold='0.6').get_result()
    print(json.dumps(classes, indent=2))
