from mongoengine import (Document, StringField, DictField, 
                         IntField, ListField, FloatField,
                         EmbeddedDocument, EmbeddedDocumentField)


# Định nghĩa class cho bbox
class BBox(EmbeddedDocument):
    box = ListField(FloatField(), required=True)
    conf = FloatField(required=True)
    class_id = IntField(required=True)
    class_name = StringField(required=True)

# Định nghĩa class chính Image


class Images(Document):
    path_image = StringField(required=True)
    bbox = ListField(EmbeddedDocumentField(BBox))
    width = IntField()
    heigh = IntField()
    meta = {"collection": "Image"}
    # Phương thức thêm image
    @classmethod
    def add_image(cls, path_image, bbox_list):
        image = cls(path_image=path_image, bbox=bbox_list)
        image.save()
        return image

    # Phương thức sửa image
    @classmethod
    def update_image(cls, image_id, path_image=None, bbox_list=None):
        image = cls.objects(id=image_id).first()
        if image:
            if path_image:
                image.path_image = path_image
            if bbox_list:
                image.bbox = bbox_list
            image.save()
            return image
        return None

    # Phương thức xóa image
    @classmethod
    def delete_image(cls, image_id):
        image = cls.objects(id=image_id).first()
        if image:
            image.delete()
            return True
        return False

    # Phương thức lấy ra tất cả image
    @classmethod
    def get_all_images(cls):
        return cls.objects()

    # Phương thức lấy ra image theo id
    @classmethod
    def get_image_by_id(cls, image_id):
        return cls.objects(id=image_id).first()

    # Phương thức thêm mới một bbox
    @classmethod
    def add_bbox(cls, image_id, bbox):
        image = cls.objects(id=image_id).first()
        if image:
            image.bbox.append(bbox)
            image.save()
            return image
        return None

    # Phương thức xóa một bbox
    @classmethod
    def remove_bbox(cls, image_id, bbox_index):
        image = cls.objects(id=image_id).first()
        if image and 0 <= bbox_index < len(image.bbox):
            image.bbox.pop(bbox_index)
            image.save()
            return image
        return None
    
    # Phương thức sửa một bbox
    @classmethod
    def update_bbox(cls, image_id, bbox_index, new_bbox):
        image = cls.objects(id=image_id).first()
        if image and 0 <= bbox_index < len(image.bbox):
            image.bbox[bbox_index] = new_bbox
            image.save()
            return image
        return None
    
