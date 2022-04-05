from Operations import Database, Predictions, FaceEmotionTracking


# ----------------------------------------------------------------------------------------------------------------------
def emotion_counts_find(date, emp_id, emotion):
    db = Database('face-emotion-counting', 'eIWnBiQ1eIQuwO97')
    db.make_connection()

    specific_emotion_count = FaceEmotionTracking.objects(date=date, emp_id=emp_id, emotion=emotion).count()
    all_emotion_count = FaceEmotionTracking.objects(date=date, emp_id=emp_id).count()

    # specific_emotion_percentage = (specific_emotion_count / all_emotion_count) * 100.0

    db.close_connection()
    return specific_emotion_count, all_emotion_count
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
def make_predictions(date, emp_id):
    predictions = {date: date, emp_id: emp_id}
    emo_counts = {}
    emo_percentages = {}

    emotions = ['Anger', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']
    for emotion in emotions:
        counts = emotion_counts_find(date, emp_id, emotion)
        specific_emo_count = counts[0]
        all_emo_count = counts[1]

        emo_counts[emotion] = specific_emo_count

        percentage = (specific_emo_count / all_emo_count) * 100.0
        emo_percentages[emotion] = percentage

    effective_emotions = emo_counts['Anger'] + emo_counts['Disgust'] + emo_counts['Fear'] + emo_counts['Sad']
    stress_percentage = (effective_emotions / all_emo_count) * 100.0

    predictions['emo_counts'] = emo_counts
    predictions['emo_percentages'] = emo_percentages
    predictions['stress_percentage'] = stress_percentage

    return predictions
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
def write_predictions(predictions):
    db = Database('predictions-write', 'BJ6AUFlFu1SnJFKI')
    db.make_connection()

    pred = Predictions()
    pred.date = predictions['date']
    pred.emp_id = predictions['emp_id']
    pred.emo_percentages = predictions['emo_percentages']
    pred.stress_percentage = predictions['stress_percentage']
    pred.save()

    db.close_connection()

    return 'predictions data updated.'
# ----------------------------------------------------------------------------------------------------------------------