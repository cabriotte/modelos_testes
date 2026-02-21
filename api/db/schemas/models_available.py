from peewee import SqliteDatabase, Model, CharField, DateTimeField, IntegerField, BooleanField

db = SqliteDatabase('models_available.db')

class ModelsAvailable(Model):
    ticker = CharField()
    created_at = DateTimeField()
    time_series_used = CharField()
    janela = IntegerField()
    epochs = IntegerField()
    batch = IntegerField()
    patience = IntegerField()
    activated = BooleanField(default=True)
    filename = CharField()

    class Meta:
        database = db

db.create_tables([ModelsAvailable])