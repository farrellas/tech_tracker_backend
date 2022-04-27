from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash
from secrets import token_hex

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    api_token = db.Column(db.String, default=None, nullable=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    customer = db.relationship('Customer', backref='user', lazy=True)

    def __init__(self, email, password, first_name, last_name):
        self.email = email
        self.password = generate_password_hash(password)
        self.first_name = first_name
        self.last_name = last_name
        self.api_token = token_hex(32)

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "company_id": self.company_id,
            "token": self.api_token,
        }

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False, unique=True)
    street_address = db.Column(db.String(100), nullable=True)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    zip_code = db.Column(db.Integer, nullable=False)
    logo_url = db.Column(db.String(300))
    company_password = db.Column(db.String(100), nullable=False)
    admin_id = db.Column(db.Integer, nullable=False)
    user = db.relationship('User', backref='company', lazy=True)
    customer = db.relationship('Customer', backref='company', lazy=True)

    def __init__(self, company_name, street_address, city, state, zip_code, company_password):
        self.company_name = company_name
        self.street_address = street_address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.company_password = company_password
    
    def to_dict(self):
        return {
            "id": self.id,
            "company_name": self.company_name,
            "street_address": self.street_address,
            "city": self.city,
            "state": self.state,
            "zip_code": self.zip_code,
            "logo_url": self.logo_url,
            "company_password": self.company_password,
            "admin_id": self.admin_id
        }

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    street_address = db.Column(db.String(100), nullable=True)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    zip_code = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(150))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    system = db.relationship('System', backref='owner', lazy=True)
    work_order = db.relationship('WorkOrder', backref='owner', lazy=True)

    def __init__(self, name, street_address, city, state, zip_code, email, user_id):
        self.name = name
        self.street_address = street_address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.email = email
        self.user_id = user_id

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "street_address": self.street_address,
            "city": self.city,
            "state": self.state,
            "zip_code": self.zip_code,
            "email": self.email,
            "user_id": self.user_id,
            "company_id": self.company_id
        }

class System(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    area_served = db.Column(db.String(100), nullable=False)
    system_type = db.Column(db.String(100), nullable=False)
    heating = db.Column(db.Boolean, default=True, nullable=False)
    cooling = db.Column(db.Boolean, default=True, nullable=False)
    notes = db.Column(db.String(1000), nullable=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    equipment = db.relationship('Equipment', backref='system', lazy=True)
    work_order = db.relationship('WorkOrder', backref='system', lazy=True)

    def __init__(self, name, area_served, system_type, heating, cooling, notes, customer_id):
        self.name = name
        self.area_served = area_served
        self.system_type = system_type
        self.heating = heating
        self.cooling = cooling
        self.notes = notes
        self.customer_id = customer_id

    def to_dict(self):
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "name": self.name,
            "area_served": self.area_served,
            "system_type": self.system_type,
            "heating": self.heating,
            "cooling": self.cooling,
            "notes": self.notes
        }

class Equipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equipment_class = db.Column(db.String(50), nullable=False)
    brand = db.Column(db.String(100), nullable=False)
    model_no = db.Column(db.String(100), nullable=False)
    serial_no = db.Column(db.String(100), nullable=False)
    year = db.Column(db.String(10), nullable=False)
    equipment_type = db.Column(db.String(100), nullable=False)
    fuel_type = db.Column(db.String(20), nullable=True)
    refrigerant_type = db.Column(db.String(20), nullable=True)
    notes = db.Column(db.String(1000), nullable=True)
    system_id = db.Column(db.Integer, db.ForeignKey('system.id'), nullable=False)

    def __init__(self, brand, model_no, serial_no, year, equipment_type, notes, system_id, fuel_type='', refrigerant_type=''):
        self.equipment_class = 'packaged'
        self.brand = brand
        self.model_no = model_no
        self.serial_no = serial_no
        self.year = year
        self.equipment_type = equipment_type
        self.notes = notes
        self.system_id = system_id
        self.fuel_type = fuel_type
        self.refrigerant_type = refrigerant_type

    def to_dict(self):
        return {
            "id": self.id,
            "equipment_class": self.equipment_class,
            "brand": self.brand,
            "model_no": self.model_no,
            "serial_no": self.serial_no,
            "year": self.year,
            "equipment_type": self.equipment_type,
            "fuel_type": self.fuel_type,
            "refrigerant_type": self.refrigerant_type,
            "notes": self.notes,
            "system_id": self.system_id
        }

class WorkOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    system_id = db.Column(db.Integer, db.ForeignKey('system.id'), nullable=False)
    work_performed = db.Column(db.String(1000), nullable=False)
    order_type = db.Column(db.String(25), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, user_id, customer_id, system_id, order_type, work_performed):
        self.user_id = user_id
        self.customer_id = customer_id
        self.system_id = system_id
        self.order_type = order_type
        self.work_performed = work_performed

    def to_dict(self):
        return {
        "id": self.id,
        "user_id": self.user_id,
        "customer_id": self.customer_id,
        "system_id": self.system_id,
        "order_type": self.order_type,
        "work_performed": self.work_performed,
        "date_created": self.date_created.strftime("%m/%d/%Y")
    }