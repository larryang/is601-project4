""" define models """
from datetime import datetime
import enum
from sqlalchemy.types import Enum
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from app.db import db


class User(UserMixin, db.Model):
    """ User model """
    # pylint: disable = no-member, invalid-overridden-method
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False, unique=True)
    about = db.Column(db.String(300), nullable=True, unique=False)
    authenticated = db.Column(db.Boolean, default=False)
    registered_on = db.Column('registered_on', db.DateTime)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
    is_admin = db.Column('is_admin', db.Boolean(), nullable=False, server_default='0')

    transactions = db.relationship("Transaction", back_populates="user", cascade="all, delete")

    # `roles` and `groups` are reserved words that *must* be defined
    # on the `User` model to use group- or role-based authorization.

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.registered_on = datetime.utcnow()

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def set_password(self, password):
        """ take password and store hash """
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """ check password against hash """
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.email}>'


@enum.unique
class TransactionTypeEnum(enum.Enum):
    """ Enum for column """
    CREDIT = 'CREDIT'
    DEBIT = 'DEBIT'


class Transaction(db.Model):
    """ Account Transaction Database """
    # pylint: disable=no-member
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.DECIMAL, nullable=False, default=0)
    description = db.Column(db.String(300), nullable=True, unique=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    transaction_type = db.Column(Enum(TransactionTypeEnum), nullable=True, unique=False)

    user = relationship("User", back_populates="transactions", uselist=False)

    def __init__(self, amount, transaction_type):
        self.amount = amount
        self.transaction_type = transaction_type

    @staticmethod
    def csv_headers():
        """ returns tuple of CSV header """
        transaction_types = ( 'AMOUNT', 'TYPE' )
        return transaction_types
