#!/usr/bin/env python

# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Demonstrates web detection using the Google Cloud Vision API.
Example usage:
  python web_detect.py https://goo.gl/X4qcB6
  python web_detect.py ../detect/resources/landmark.jpg
  python web_detect.py gs://your-bucket/image.png
"""
# [START vision_web_detection_tutorial]
# [START vision_web_detection_tutorial_imports]
import argparse
import io

from google.cloud import vision
from google.cloud.vision import types
# [END vision_web_detection_tutorial_imports]
import os
import pandas as pd
from urllib import parse

print('Credendtials from environ: {}'.format(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')))

def annotate(path):
    """Returns web annotations given the path to an image."""
    # [START vision_web_detection_tutorial_annotate]
    client = vision.ImageAnnotatorClient()

    if path.startswith('http') or path.startswith('gs:'):
        image = types.Image()
        image.source.image_uri = path

    else:
        with io.open(path, 'rb') as image_file:
            content = image_file.read()

        image = types.Image(content=content)

    web_detection = client.web_detection(image=image).web_detection
    # [END vision_web_detection_tutorial_annotate]

    return web_detection

def annotate_urls(list_of_urls):
    """
        Params: a list of url strings
    Returns a python dataframe object with the url, image annotatio and its score
    """
    client = vision.ImageAnnotatorClient()
    df = pd.DataFrame(columns =('url', 'location', 'score'))
    idx_counter = 0
    for url in list_of_urls:
        if url.startswith('http') or url.startswith('gs: '):
            image = types.Image()
            image.source.image_uri = url
        else:
            with io.open(url, 'rb') as image_file:
                content = image_file.read()

            image = types.Image(content = content)
        web_detection = client.web_detection(image=image).web_detection
        for entity in web_detection.web_entities:
            parsed_url = dict(parse.parse_qsl(parse.urlsplit(url).query))
            location = parsed_url["location"]
            df.loc[idx_counter] = [location, entity.description, entity.score]
            idx_counter += 1
        return df

def export_to_csv(df):
    """
        Params:
            df: a pandas datafame object
        Returns: a csv file named annotations.csv
    """
    df.to_csv("output_report.csv", sep="|")

def report(annotations):
    """Prints detected features in the provided web annotations."""
    # [START vision_web_detection_tutorial_print_annotations]
    if annotations.pages_with_matching_images:
        print('\n{} Pages with matching images retrieved'.format(
            len(annotations.pages_with_matching_images)))

        for page in annotations.pages_with_matching_images:
            print('Url   : {}'.format(page.url))

    if annotations.full_matching_images:
        print('\n{} Full Matches found: '.format(
              len(annotations.full_matching_images)))

        for image in annotations.full_matching_images:
            print('Url  : {}'.format(image.url))

    if annotations.partial_matching_images:
        print('\n{} Partial Matches found: '.format(
              len(annotations.partial_matching_images)))

        for image in annotations.partial_matching_images:
            print('Url  : {}'.format(image.url))

    if annotations.web_entities:
        print('\n{} Web entities found: '.format(
              len(annotations.web_entities)))

        for entity in annotations.web_entities:
            print('Score      : {}'.format(entity.score))
            print('Description: {}'.format(entity.description))
    # [END vision_web_detection_tutorial_print_annotations]


if __name__ == '__main__':

    # [START vision_web_detection_tutorial_run_application]
	#parser = argparse.ArgumentParser(
	#	description=__doc__,
	#formatter_class=argparse.RawDescriptionHelpFormatter)
	#path_help = str('The image to detect, can be web URI, '
	#	'Google Cloud Storage, or path to local file.')
	#parser.add_argument('image_url', help=path_help)
    #args = parser.parse_args()
    report(annotate(args.image_url))
    #sample_urls = ['https://maps.googleapis.com/maps/api/streetview?location=42.352126880933916%2C-71.12346594024035&key=AIzaSyCVx6Vms7Sm1tvsm8NdvLt2FNdWdX7bicA&size=640x640', 'https://maps.googleapis.com/maps/api/streetview?location=42.352126880933916%2C-71.12346594024035&key=AIzaSyCVx6Vms7Sm1tvsm8NdvLt2FNdWdX7bicA&size=640x640', 'https://maps.googleapis.com/maps/api/streetview?location=42.352126880933916%2C-71.12346594024035&key=AIzaSyCVx6Vms7Sm1tvsm8NdvLt2FNdWdX7bicA&size=640x640', 'https://maps.googleapis.com/maps/api/streetview?location=42.352126880933916%2C-71.12346594024035&key=AIzaSyCVx6Vms7Sm1tvsm8NdvLt2FNdWdX7bicA&size=640x640', 'https://maps.googleapis.com/maps/api/streetview?location=42.352126880933916%2C-71.12346594024035&key=AIzaSyCVx6Vms7Sm1tvsm8NdvLt2FNdWdX7bicA&size=640x640', 'https://maps.googleapis.com/maps/api/streetview?location=42.352126880933916%2C-71.12346594024035&key=AIzaSyCVx6Vms7Sm1tvsm8NdvLt2FNdWdX7bicA&size=640x640', 'https://maps.googleapis.com/maps/api/streetview?location=42.352126880933916%2C-71.12346594024035&key=AIzaSyCVx6Vms7Sm1tvsm8NdvLt2FNdWdX7bicA&size=640x640', 'https://maps.googleapis.com/maps/api/streetview?location=42.352126880933916%2C-71.12346594024035&key=AIzaSyCVx6Vms7Sm1tvsm8NdvLt2FNdWdX7bicA&size=640x640', 'https://maps.googleapis.com/maps/api/streetview?location=42.352126880933916%2C-71.12346594024035&key=AIzaSyCVx6Vms7Sm1tvsm8NdvLt2FNdWdX7bicA&size=640x640', 'https://maps.googleapis.com/maps/api/streetview?location=42.352126880933916%2C-71.12346594024035&key=AIzaSyCVx6Vms7Sm1tvsm8NdvLt2FNdWdX7bicA&size=640x640']
    sample_urls = ['https://maps.googleapis.com/maps/api/streetview?size=640x640&location=42.349018433310675%2C-71.09757458041415&key=AIzaSyCVx6Vms7Sm1tvsm8NdvLt2FNdWdX7bicA&heading=0', 'https://maps.googleapis.com/maps/api/streetview?size=640x640&location=42.349018433310675%2C-71.09757458041415&key=AIzaSyCVx6Vms7Sm1tvsm8NdvLt2FNdWdX7bicA&heading=90', 'https://maps.googleapis.com/maps/api/streetview?size=640x640&location=42.349018433310675%2C-71.09757458041415&key=AIzaSyCVx6Vms7Sm1tvsm8NdvLt2FNdWdX7bicA&heading=180', 'https://maps.googleapis.com/maps/api/streetview?size=640x640&location=42.349018433310675%2C-71.09757458041415&key=AIzaSyCVx6Vms7Sm1tvsm8NdvLt2FNdWdX7bicA&heading=270']
    #img_path = './output_images/streetview1.jpeg'
    #annotations = annotate(img_path)
    #print(annotations)
    #report(annotations)
    report = annotate_urls(sample_urls)
    print(report)
    export_to_csv(report)
    # [END vision_web_detection_tutorial_run_application]
# [END vision_web_detection_tutorial]