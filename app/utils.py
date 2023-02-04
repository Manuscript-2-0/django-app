import os
import string
import random


def handle_uploaded_file(file, filename):
    if not os.path.exists('uploads/'):
        os.mkdir('uploads/')
    new_image_folder = f'{"".join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for i in range(7))}/'
    if not os.path.exists("uploads/" + new_image_folder):
        os.mkdir("uploads/" + new_image_folder)
    with open("uploads/" + new_image_folder + filename, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return new_image_folder + filename
