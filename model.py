from app import db


class Member(db.Model):
    __tablename__ = 'member'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.String)
    phone = db.Column(db.String)
    email = db.Column(db.String)

    def __init__(self, name, age, phone, email):
        self.name = name
        self.age = age
        self.phone = phone
        self.email = email

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'phone': self.phone,
            'email': self.email,
        }
