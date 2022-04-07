from Operations import Database, Predictions, DailyPredictions, FaceEmotionTracking


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
    predictions = {'date': date, 'emp_id': emp_id}
    emo_counts = {}
    emo_percentages = {}

    emotions = ['Anger', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']
    for emotion in emotions:
        counts = emotion_counts_find(date, emp_id, emotion)
        print(f'COUNTS-----------------> = {counts}')
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
    db = Database('predictions-write', 'yBAGoHEuXurabm63')
    db.make_connection()

    data = Predictions.objects(date=predictions['date'], emp_id=predictions['emp_id']).first()

    if data:
        data.update(emo_counts=predictions['emo_counts'], emo_percentages=predictions['emo_percentages'], stress_percentage=predictions['stress_percentage'])
        db.close_connection()

        db = Database('daily-predictions', 'b1xvQn1CBeoBf2a6')
        db.make_connection()

        daily_report = DailyPredictions.objects(date=predictions['date']).first()
        if daily_report:
            all_emo_counts = {}
            all_emo_percentages = {}
            all_count = 0

            for emotion in daily_report.all_emo_counts.keys():
                specific_emo_count = daily_report.all_emo_counts[emotion] + predictions['emo_counts'][emotion]
                all_emo_counts[emotion] = specific_emo_count
                all_count += specific_emo_count

            for emotion in daily_report.all_emo_percentages.keys():
                all_emo_percentages[emotion] = (all_emo_counts[emotion] / all_count) * 100.0

            all_effective_emotions = all_emo_counts['Anger'] + all_emo_counts['Disgust'] + all_emo_counts['Fear'] + all_emo_counts['Sad']
            average_stress_percentage = (all_effective_emotions / all_count) * 100.0

            daily_report.update(all_emo_counts=all_emo_counts, all_emo_percentages=all_emo_percentages, average_stress_percentage=average_stress_percentage)

        else:
            emotions = ['Anger', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']
            all_emo_counts = {}
            all_emo_percentages = {}
            all_count = 0

            for emotion in emotions:
                specific_emo_count = predictions['emo_counts'][emotion]
                all_emo_counts[emotion] = specific_emo_count
                all_count += specific_emo_count

            for emotion in emotions:
                all_emo_percentages[emotion] = (all_emo_counts[emotion] / all_count) * 100.0

            all_effective_emotions = all_emo_counts['Anger'] + all_emo_counts['Disgust'] + all_emo_counts['Fear'] + all_emo_counts['Sad']
            average_stress_percentage = (all_effective_emotions / all_count) * 100.0

            daily_pred = DailyPredictions()
            daily_pred.date = predictions['date']
            daily_pred.all_emo_counts = all_emo_counts
            daily_pred.all_emo_percentages = all_emo_percentages
            daily_pred.average_stress_percentage = average_stress_percentage
            daily_pred.save()

        db.close_connection()

    else:
        db = Database('predictions-write', 'yBAGoHEuXurabm63')
        db.make_connection()

        pred = Predictions()
        pred.date = predictions['date']
        pred.emp_id = predictions['emp_id']
        pred.emo_counts = predictions['emo_counts']
        pred.emo_percentages = predictions['emo_percentages']
        pred.stress_percentage = predictions['stress_percentage']
        pred.save()

        db.close_connection()

        db = Database('daily-predictions', 'b1xvQn1CBeoBf2a6')
        db.make_connection()

        daily_report = DailyPredictions.objects(date=predictions['date']).first()
        if daily_report:
            all_emo_counts = {}
            all_emo_percentages = {}
            all_count = 0

            for emotion in daily_report.all_emo_counts.keys():
                specific_emo_count = daily_report.all_emo_counts[emotion] + predictions['emo_counts'][emotion]
                all_emo_counts[emotion] = specific_emo_count
                all_count += specific_emo_count

            for emotion in daily_report.all_emo_percentages.keys():
                all_emo_percentages[emotion] = (all_emo_counts[emotion] / all_count) * 100.0

            all_effective_emotions = all_emo_counts['Anger'] + all_emo_counts['Disgust'] + all_emo_counts['Fear'] + all_emo_counts['Sad']
            average_stress_percentage = (all_effective_emotions / all_count) * 100.0

            daily_report.update(all_emo_counts=all_emo_counts, all_emo_percentages=all_emo_percentages, average_stress_percentage=average_stress_percentage)

        else:
            emotions = ['Anger', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']
            all_emo_counts = {}
            all_emo_percentages = {}
            all_count = 0

            for emotion in emotions:
                specific_emo_count = predictions['emo_counts'][emotion]
                all_emo_counts[emotion] = specific_emo_count
                all_count += specific_emo_count

            for emotion in emotions:
                all_emo_percentages[emotion] = (all_emo_counts[emotion] / all_count) * 100.0

            all_effective_emotions = all_emo_counts['Anger'] + all_emo_counts['Disgust'] + all_emo_counts['Fear'] + all_emo_counts['Sad']
            average_stress_percentage = (all_effective_emotions / all_count) * 100.0

            daily_pred = DailyPredictions()
            daily_pred.date = predictions['date']
            daily_pred.all_emo_counts = all_emo_counts
            daily_pred.all_emo_percentages = all_emo_percentages
            daily_pred.average_stress_percentage = average_stress_percentage
            daily_pred.save()

        db.close_connection()

    return 'predictions data updated.'
# ----------------------------------------------------------------------------------------------------------------------
