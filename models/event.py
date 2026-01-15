# class Event:
#     def __init__(self, class_name, description, end_datetime):
#         self.class_name = class_name
#         self.end_datetime = end_datetime
#         self.description = description
    
#     def to_dict(self):
#         """Convert event to dictionary for Jinja templating"""
#         return {
#             "class_name": self.class_name,
#             "end_datetime": self.end_datetime,
#             "description": self.description
#         }
    
#     def __repr__(self):
#         return f"Event({self.class_name}, {self.end_datetime}, {self.description})"

from database import db
class Event(db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(100), nullable=False)
    end_datetime = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    # notes = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), nullable=False, default="not started")

    def __init__(self, class_name, end_datetime, description, status="not started"):
        self.class_name = class_name
        self.end_datetime = end_datetime
        self.description = description
        self.status = status

    def to_dict(self):
        """Convert event to dictionary for Jinja templating"""
        return {
            "id": self.id,
            "class_name": self.class_name,
            "end_datetime": self.end_datetime,
            "description": self.description,
            "status": self.status
        }

    def __repr__(self):
        return f"Event({self.class_name}, {self.end_datetime}, {self.description})"
