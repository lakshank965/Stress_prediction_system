import getpass

from keras.preprocessing.image import array_to_img
from Operations import find_user_type
from HumanOrNot import HumanOrNot
from Emotion import find_emotion, save_emotion


username = getpass.getuser()    # get username of loging user in computer


if find_user_type(username) == "employee":  # check status of the user by using username
    while True:
        human = HumanOrNot(0)
        detection = human.detection()

        # human detection confirmed
        if detection[0]:
            mtcnn_values = detection[0][0]
            confidence = mtcnn_values['confidence']
            face_box = mtcnn_values['box']

            print(f"confidence = {confidence}")
            print(f"face_box = {face_box}")

            # confidence = mtcnn_values['confidence']

            if confidence >= 0.999:
                human_image = detection[1]
                print("human detected..! image pass to recognize emotion")

                predict_emotion = find_emotion(human_image, face_box)

                save_emotion(username, predict_emotion)

            else:
                print("human detected..! But can not recognize emotion")

        else:
            print("human not detected..!")
