import pymongo
from mongoengine import connection
from mongoengine import connect, Document, disconnect
from mongoengine.fields import StringField, DateTimeField, EmailField, DictField, FloatField
import datetime


class Database():
    """ Connect to a mongoDB Atlas """

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.connection_uri = f"mongodb+srv://{self.username}:{self.password}@spm-cluster.g8ddv.mongodb.net/spmdb?retryWrites=true&w=majority"
        self.database_name = "spmdb"

    def make_connection(self):
        print(self.connection_uri)
        print(self.username)
        connection.connect('spmdb', 'default', host=self.connection_uri)

    def close_connection(self):
        print("connection close start")
        connection.disconnect()
        print("connection close end")


class FaceEmotionTracking(Document):
    """ face_emotion_tracking collection document defining"""
    # connection_URI = "mongodb+srv://face-emotion-tracking:Nzvy38zLtRAGqXuQ@spm-cluster.g8ddv.mongodb.net/spmdb?retryWrites=true&w=majority"
    # connect(host=connection_URI)
    db = Database("face-emotion-tracking", "Nzvy38zLtRAGqXuQ")
    db.make_connection()

    date = DateTimeField(default=datetime.date.today())
    emp_id = StringField(required=True, unique=False, max_length=40, index=True)
    emotion = StringField(required=True, unique=False)

    db.close_connection()


class Employees(Document):
    db = Database('find-user-type', 'PAvO0FAVjc4KXkiE')
    db.make_connection()

    emp_id = StringField(required=True, unique=True, max_length=40, index=False)
    status = StringField(required=True, unique=False, max_length=20, index=False)
    email = EmailField(required=True, unique=True)

    db.close_connection()


class Predictions(Document):
    db = Database('predictions-write','hcLSaL51IP3VgRGH')
    db.make_connection()

    date = DateTimeField(default=datetime.date.today())
    emp_id = StringField(required=True, unique=False, max_length=40, index=True)
    emo_counts = DictField()
    emo_percentages = DictField()
    stress_percentage = FloatField()

    db.close_connection()
# ------------------------------------------------------------------------------------------------------------


# def connect_db(username, password):
#     """Connect to a database"""
#     client = pymongo.MongoClient(
#         f"mongodb+srv://{username}:{password}@spm-cluster.g8ddv.mongodb.net/spmdb?retryWrites=true&w=majority")
#     db = client.spmdb
#     return db


# -----------------------------------------------------------------------------------------------------------

def find_user_type(emp):
    """finding user status in company"""
    db = Database('find-user-type', 'PAvO0FAVjc4KXkiE')
    db.make_connection()
    employee = Employees.objects(emp_id=emp).first()

    if employee:
        if employee.status == "employee":
            status = "employee"
        else:
            status = "manager"

    db.close_connection()
    # db = connect_db('find-user-type', 'PAvO0FAVjc4KXkiE')
    # collection = db["users"]  # users data
    # user_result = collection.find({"emp_id": emp_id})
    #
    # # memory value change to dictionary
    # if user_result:
    #     for result in user_result:
    #         user = result
    #
    # if user["status"] == "employee":
    #     status = "employee"
    #
    # else:
    #     status = "manager"

    return status

# -----------------------------------------------------------------------------------------------------------
