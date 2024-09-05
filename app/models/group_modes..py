# # app/models/group_models.py
# from ..extensions import db
# from datetime import datetime
# import uuid
# # This table will store groups data not to be used for now for later scaling with group learning functionality
# class Group(db.Model):
#     __tablename__ = "groups"
#     id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
#     name = db.Column(db.String(100), nullable=False)
#     created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
#     updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
#     def __repr__(self):
#         return f'<Group {self.id}>'

# # This table will store the mapping of users to groups
# class UsersGroup(db.Model):
#     __tablename__ = "users_groups"
#     id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
#     user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
#     group_id = db.Column(db.String(36), db.ForeignKey('group.id'), nullable=False)