from mongoengine import (Document, StringField, DictField,
                         IntField, ListField, FloatField, BooleanField,
                         EmbeddedDocument, EmbeddedDocumentField)


class File(Document):
    name = StringField()
    folder = StringField()
    path = StringField()
    haveCaption = BooleanField()
    detection_name = StringField()
    __v = IntField()
    meta = {'collection': "files", 
            'strict': False}

    # Phương thức sửa image
    @classmethod
    def update_file(cls, file_id, detection_name):
        file = cls.objects(id=file_id).first()
        if file_id:
            if detection_name:
                file.detection_name = str(detection_name)
            file.save()
            return file
        return None

    @classmethod
    def get_file(cls, file_id):
        file = cls.objects(id=file_id).first()
        if file:
            return file
        return None

    def to_json(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "folder": self.folder,
            "path": self.path,
            "haveCaption": self.haveCaption,
            "detection_name": self.detection_name,
        }