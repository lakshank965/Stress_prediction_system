import cv2
import datetime
from datetime import date, time
import numpy as np
import tensorflow as tf

from random import shuffle

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.utils import save_img
from keras.preprocessing.image import array_to_img, img_to_array
from Operations import FaceEmotionTracking, Database


def find_emotion(image_array, face_box):
    # Cropping an image
    cropped_image = image_array[face_box[1]:(face_box[1] + face_box[3]), face_box[0]:(face_box[0] + face_box[2])]
    # cropped_image = cv2.cvtColor(cropped_image, cv2.COLOR_RGB2GRAY)

    # Display cropped image
    cv2.imshow("cropped", cropped_image)

    cv2.waitKey(2000)

    # ---------------------------------------------------------------------------------------------------

    emotions = ['Anger', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

    predict_value = 0.
    # ---------------------------------------------------------------------------------------------------
    # # img = save_img(cropped_image)
    # path = 'AF34AFS.png'
    # img = image.load_img(path, target_size=(72, 72), color_mode='rgb')
    # img = array_to_img(cropped_image)
    # ---------------------------------------------------------------------------------------------------

    img = tf.image.rgb_to_grayscale(cropped_image)
    new_image_array = img_to_array(img)

    new_image_array = cv2.resize(new_image_array, (48, 48))
    reshape_new_image_array = new_image_array.reshape(1, 48, 48, 1)

    model = load_model("models/FERmodified_net3.hdf5")
    prediction = model.predict(reshape_new_image_array)
    print(prediction)

    for i in range(0, len(prediction[0])):
        # print(prediction[0][i])
        if predict_value < prediction[0][i]:
            # print(f'pred --- i ---- {prediction[0][i]}')
            predict_value = prediction[0][i]
            # print(f'prediction_value = {predict_value}')
            predict_emotion = emotions[i]

    print(f'predicted emotion is {predict_emotion}')
    return predict_emotion


# ------------------------------------------------------------------------------------------

def save_emotion(username, predict_emotion, date):
    db = Database("face-emotion-tracking", "Nzvy38zLtRAGqXuQ")
    db.make_connection()
    # current_time = datetime.datetime.now()
    # year = current_time.year
    # month = current_time.month
    # day = current_time.day
    # hour = current_time.hour
    # minute = current_time.minute
    tracking_emotion = FaceEmotionTracking()
    tracking_emotion.emp_id = username
    tracking_emotion.emotion = predict_emotion
    # tracking_emotion.date = date.today()
    tracking_emotion.date = date
    tracking_emotion.save()

    db.close_connection()

    return "emotion saved!"


# for d in range(6, 31):
#     for i in range(50):
#         emotions = ['Anger', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']
#         employee = ['emp001', 'emp002', 'emp003', 'emp004', 'emp005']
#         shuffle(emotions)
#         shuffle(employee)
#         date = f'2022-03-{d}'
#         save_emotion(employee[0], emotions[0], date)
