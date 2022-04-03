from mtcnn import MTCNN
import cv2
import tensorflow


class HumanOrNot:
    def __init__(self, camera):
        # define a video capture object
        self.camera = camera
        self.vid = cv2.VideoCapture(self.camera)

    def detection(self):
        # Capture the video frame by frame
        ret, frame = self.vid.read()

        # # Display the resulting frame
        # cv2.imshow('frame', frame)
        # # Frame wait two seconds
        # cv2.waitKey(2000)

        # frame added to variable
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # When everything done, release the capture
        self.vid.release()
        cv2.destroyAllWindows()

        # make instance by MTCNN and detect human face
        detector = MTCNN()
        face_detect = (detector.detect_faces(img))

        return face_detect, img


print("HumanOrNot class working...")
