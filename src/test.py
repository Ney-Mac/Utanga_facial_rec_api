import cv2
import face_recognition as fr
import os

def get_img(file_name):
    return os.path.abspath(f"src/assets/{file_name}")

img_elon = fr.load_image_file(get_img("elon_musk1.jpg"))
img_elon = cv2.cvtColor(img_elon, cv2.COLOR_BGR2RGB)

img_elon_test = fr.load_image_file(get_img("mac.jpeg"))
img_elon_test = cv2.cvtColor(img_elon_test, cv2.COLOR_BGR2RGB)

face_loc = fr.face_locations(img_elon)[0]
face_loc_test = fr.face_locations(img_elon_test)[0]

# print(face_loc)

cv2.rectangle(img_elon, (face_loc[3], face_loc[0]), (face_loc[1], face_loc[2]), (0,255,0), 2)
cv2.rectangle(img_elon_test, (face_loc_test[3], face_loc_test[0]), (face_loc_test[1], face_loc_test[2]), (0,255,0), 2)

encode_elon = fr.face_encodings(img_elon)[0]
encode_elon_test = fr.face_encodings(img_elon_test)[0]

print(encode_elon)

compare = fr.compare_faces([encode_elon], encode_elon_test)
distance = fr.face_distance([encode_elon], encode_elon_test)

print(compare, distance)

cv2.imshow('Elon', img_elon)
cv2.imshow('Elon Test', img_elon_test)
cv2.waitKey(0)