from peewee import SqliteDatabase, Model, IntegerField, FloatField

db = SqliteDatabase("model_prediction_duration.db")


class ModelPredictionDuration(Model):
    model_id = IntegerField()
    start = FloatField()
    duration = FloatField()

    class Meta:
        database = db


db.create_tables([ModelPredictionDuration])
