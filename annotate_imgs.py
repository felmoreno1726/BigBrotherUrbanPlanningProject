import os
import argparse
import io

from google.cloud import vision
from google.cloud.vision import types
from PIL import Image, ImageDraw

def localize_objects(path):
    """Localize objects in the local image.

    Args:
    path: The path to the local file.
    """
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    with open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)

    objects = client.object_localization(
        image=image).localized_object_annotations

    print('Number of objects found: {}'.format(len(objects)))
    for object_ in objects:
        print('\n{} (confidence: {})'.format(object_.name, object_.score))
        print('Normalized bounding polygon vertices: ')
        for vertex in object_.bounding_poly.normalized_vertices:
            print(' - ({}, {})'.format(vertex.x, vertex.y))
    return objects

def annotate_to(image, objects, output_filename):
    """ Draws a polygon around the detected objects
    """
    if objects:
        print("Objects: ", objects)
        im = Image.open(image)
        draw = ImageDraw.Draw(im)
        for obj in objects:
            print("poly vertices: ", obj.bounding_poly.normalized_vertices)
            #box = [(vertex.x, vertex.y) for vertex in obj.bounding_poly.normalized_vertices]
            box = []
            vertices = obj.bounding_poly.normalized_vertices
            for vertex in vertices:
                box.append(int(vertex.x * 640))
                box.append(int(vertex.y * 640))
            count = 0
            for vertex in vertices:
                if count == 1:
                    break
                else:
                    box.append(int(vertex.x * 640))
                    box.append(int(vertex.y * 640))
                    count += 1
            #box.append[vertices[0].x, vertices[0].y]
            #draw.line(box + [box[0]], width = 20, fill='#00ff00')
            draw.line(tuple(box) , width = 5, fill='#00ff00')
        im.save(output_filename)

if __name__ == "__main__":
    print(os.listdir('.'))
    input_dir = "./images_input/"
    output_dir= "./output_images/"
    images = os.listdir(input_dir)
    for img in images:
        path_to_img = input_dir + img
        print(path_to_img)
        objs = localize_objects(path_to_img)
        print("Writing to: ", output_dir + img)
        annotate_to(path_to_img, objs, output_dir + img)
        #input("Press Enter to continue...")