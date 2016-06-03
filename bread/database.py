from datetime import datetime, timezone

from sqlalchemy.orm import relationship, backref
from sqlalchemy import (Column, DateTime, Integer, String,
                        ForeignKey, Float, Boolean, Text)
from flask.ext.security import RoleMixin, UserMixin
from flask.ext.security.utils import encrypt_password

from bread.extentions import db


def set_utc_zone(utc_dt):    # Tell the datetime object that it's in UTC time zone since
    # datetime objects are 'naive' by default
    return utc_dt.replace(tzinfo=timezone.utc)


def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)


class Base(db.Model):
    __abstract__ = True

    id = Column(db.Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Role(Base, RoleMixin):
    __tablename__ = "roles"

    name = Column(String(length=80), unique=True, nullable=False)
    description = Column(String(length=255))

    def __repr__(self):
        return "<Role {}>".format(self.name)


# Provide many-to-many between DbRole and DbUser
roles_users = db.Table('roles_users',
                       Column('user_id', Integer(), ForeignKey('users.id')),
                       Column('role_id', Integer(), ForeignKey('roles.id'))
                       )


class User(Base, UserMixin):
    __tablename__ = "users"

    # username = Column(String(80), nullable=False, unique=True)

    # Required by flask-security to be the ID
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    first_name = Column(String(80), nullable=False)
    last_name = Column(String(80), nullable=False)
    active = Column(Boolean())
    roles = relationship('Role', secondary=roles_users,
                         backref=backref('users', lazy='dynamic'))

    @staticmethod
    def create_user(email, password, given_name, family_name):
        from bread.framework.security import user_datastore
        return user_datastore.create_user(email=email,
                                          password=encrypt_password(password),
                                          given_name=given_name,
                                          family_name=family_name)

    @staticmethod
    def update_password(email, password):
        user = User.query.filter_by(email=email).one()
        user.password = encrypt_password(password)

    def print_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def __repr__(self):
        return "<User {} ({})>".format(self.id, self.email)


class DbProducer(Base):
    __tablename__ = 'producers'

    name = Column(String(80), nullable=False)
    description = Column(Text())

    def __repr__(self):
        return self.name


class DbItem(Base):
    __tablename__ = 'items'
    name = Column(String(80), unique=True, nullable=False)
    description = Column(Text())
    price = Column(Float(), nullable=False)
    producer_id = Column(Integer, ForeignKey('producers.id'), nullable=False)

    producer = relationship('DbProducer')

    def __repr__(self):
        return "{}".format(self.name)


class DbOrder(Base):
    __tablename__ = 'orders'
    name = Column(String(80), nullable=False)
    delivery_date_utc = Column(DateTime())
    close_date_utc = Column(DateTime())
    producer_id = Column(Integer, ForeignKey('producers.id'), nullable=False)

    producer = relationship('DbProducer')
    # backref order_items

    @staticmethod
    def compute_quantity(order_items):
        return sum([order_item.quantity for order_item in order_items])

    @staticmethod
    def compute_price(order_items):
        return sum([order_item.item.price * order_item.quantity for order_item in order_items])

    @property
    def close_date(self):
        return utc_to_local(set_utc_zone(self.close_date_utc))

    @property
    def delivery_date(self):
        return utc_to_local(set_utc_zone(self.delivery_date_utc))

    @property
    def total_quantity(self):
        return self.compute_quantity(self.order_items)

    @property
    def total_price(self):
        return self.compute_price(self.order_items)

    @property
    def is_closed(self):
        return set_utc_zone(datetime.utcnow()) > set_utc_zone(self.close_date_utc)

    def __repr__(self):
        return "{} ({})".format(self.name, self.delivery_date_utc)


class DbOrderItem(Base):
    __tablename__ = 'order_items'
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    quantity = Column(Integer, nullable=False, server_default='0')

    order = relationship('DbOrder', backref='order_items')
    item  = relationship('DbItem')
    user  = relationship('User')