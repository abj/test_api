import pandas as pd
import os
from datetime import datetime
import string, random
from app import db, app

class File(db.Model):
    id = db.Column(db.String(30), primary_key=True)
    upload_date = db.Column(db.DateTime)
    processed_date = db.Column(db.DateTime)
    status = db.Column(db.String(30))
    result = db.Column(db.String(30))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = self._id_generator()
        self.upload_date = datetime.utcnow()
        self.status = 'Загружено'
    
    def as_dict(self):
        return {"id": self.id, "upload_date": self.upload_date, "processed_date": self.processed_date, "status": self.status, "result": self.result}

    def _id_generator(self, size=10, chars=string.ascii_lowercase + string.digits + string.ascii_uppercase):
        return ''.join(random.choice(chars) for _ in range(size))

    def process(self):
        f = pd.ExcelFile(os.path.join(app.config['UPLOAD_DIRECTORY'], '.'.join([self.id, self.extension])))
        self.status = 'Обрабатывается'
        for df in [f.parse(sheet) for sheet in f.sheet_names]:
            if 'after' in df.columns and 'before' in df.columns:
                print(df)
                x = df.before - df.after == 0
                idx = x.idxmin()
                msg = {'before': 'removed: {}', 'after' : 'added {}'}
                col = 'before'
                if df.after.count() > df.before.count():
                    col = 'after'
                self.processed_date = datetime.utcnow()
                self.status = 'Обработано'
                self.result =  msg[col].format(df[col][idx])
        db.session.commit()
