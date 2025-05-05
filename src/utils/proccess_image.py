import face_recognition as fr
import cv2
from io import BytesIO


def proccess_image(image):
    img_loaded = fr.load_image_file(BytesIO(image))
    img_loaded = cv2.cvtColor(img_loaded, cv2.COLOR_BGR2RGB)
    return fr.face_encodings(img_loaded)