
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    # NEW FIELDS FOR ADMIN AND RESET
    is_approved = db.Column(db.Boolean, default=False)
    reset_token = db.Column(db.String(100), nullable=True)
    reset_token_expiry = db.Column(db.DateTime, nullable=True)


class Workstation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    roll = db.Column(db.String(20))
    course = db.Column(db.String(20))
    year = db.Column(db.String(10))
    faculty = db.Column(db.String(100))
    staff_incharge = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    room_lab_name = db.Column(db.String(50))
    cubicle_no = db.Column(db.String(10))
    manufacturer = db.Column(db.String(100))
    otherManufacturer = db.Column(db.String(100))
    model = db.Column(db.String(100))
    serial = db.Column(db.String(100))
    os = db.Column(db.String(50))
    otherOs = db.Column(db.String(50))
    processor = db.Column(db.String(100))
    cores = db.Column(db.String(10))
    ram = db.Column(db.String(20))
    otherRam = db.Column(db.String(20))
    storage_type1 = db.Column(db.String(50))
    storage_capacity1 = db.Column(db.String(20))
    storage_type2 = db.Column(db.String(50))
    storage_capacity2 = db.Column(db.String(20))
    gpu = db.Column(db.String(100))
    vram = db.Column(db.String(10))
    issue_date = db.Column(db.String(20))
    system_required_till = db.Column(db.String(20))
    po_date = db.Column(db.String(20))
    source_of_fund = db.Column(db.String(100))
    keyboard_provided = db.Column(db.String(10))
    keyboard_details = db.Column(db.String(100))
    mouse_provided = db.Column(db.String(10))
    mouse_details = db.Column(db.String(100))
    monitor_provided = db.Column(db.String(20))
    monitor_details = db.Column(db.String(100))
    monitor_size = db.Column(db.String(10))
    monitor_serial = db.Column(db.String(100))


class Equipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    manufacturer = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    serial_number = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    purchase_date = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    po_date = db.Column(db.String(20), nullable=False)
    intender_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    department_code = db.Column(db.String(100), unique=True, nullable=False)

class ProvisioningRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mac_address = db.Column(db.String(32), nullable=False)
    ip_address = db.Column(db.String(32), nullable=False)
    os_image = db.Column(db.String(64), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

