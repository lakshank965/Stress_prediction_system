from Operations import Database, Predictions, FaceEmotionTracking


def count_emotion(date, emp_id, emotion):
    db = Database('face-emotion-counting', 'eIWnBiQ1eIQuwO97')
    db.make_connection()

    emotion_count = FaceEmotionTracking.objects(date=date, emp_id=emp_id, emotion=emotion).count()
    print(emotion_count)

    db.close_connection()


count_emotion('2022-03-14', 'emp003', 'Neutral')
