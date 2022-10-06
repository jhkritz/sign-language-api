from . import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    pass_hash = db.Column(db.String(256), nullable=False)


class UserRole(db.Model):
    __tablename__ = 'user_role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    libraryid = db.Column(db.Integer, db.ForeignKey('sign_language_library.id'), nullable=False)

    # options = true = admin,
    #          false = viewer
    admin = db.Column(db.Boolean, nullable=False)


# class Roles(db.Model):
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.String(256), nullable=False)


class APIKeys(db.Model):
    userid = db.Column(db.Integer, primary_key=True)
    api_key_hash = db.Column(db.String(256), nullable=False)


class SignLanguageLibrary(db.Model):
    __tablename__ = 'sign_language_library'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(256), nullable=False)
    description = db.Column(db.String(256), nullable=False)
    # One-to-many relationship between SignLanguageLibrary and Sign
    signs = db.relationship('Sign', backref='sign_language_library', cascade="all,delete")
    # ownerid = db.Column(db.Integer, nullable=False)


class Sign(db.Model):
    __tablename__ = 'sign'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    meaning = db.Column(db.String(256), nullable=False)
    image_filename = db.Column(db.String(256), nullable=False)
    library_id = db.Column(db.Integer, db.ForeignKey('sign_language_library.id'), nullable=False)

    def to_dict(self, url_base):
        lib_name = self.sign_language_library.name
        url = '{}?image_name={}+library_name={}'.format(url_base, self.image_filename, lib_name)
        return {
            'id': self.id,
            'meaning': self.meaning,
            'image_url': url
        }
