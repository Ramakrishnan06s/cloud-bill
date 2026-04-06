from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class ServicePlan(db.Model):
    __tablename__ = 'service_plans'
    plan_id = db.Column(db.Integer, primary_key=True)
    plan_name = db.Column(db.String(50), nullable=False)
    monthly_base_fee = db.Column(db.Float, nullable=False)
    customers = db.relationship('Customer', backref='plan', lazy=True)

class Resource(db.Model):
    __tablename__ = 'resources'
    resource_id = db.Column(db.Integer, primary_key=True)
    resource_name = db.Column(db.String(100), nullable=False)
    unit_price_inr = db.Column(db.Float, nullable=False)
    usage_logs = db.relationship('UsageLog', backref='resource', lazy=True)

class Customer(db.Model):
    __tablename__ = 'customers'
    cust_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey('service_plans.plan_id'), nullable=True)
    usage_logs = db.relationship('UsageLog', backref='customer', lazy=True)
    invoices = db.relationship('Invoice', backref='customer', lazy=True)

class UsageLog(db.Model):
    __tablename__ = 'usage_logs'
    log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cust_id = db.Column(db.Integer, db.ForeignKey('customers.cust_id'), nullable=False)
    resource_id = db.Column(db.Integer, db.ForeignKey('resources.resource_id'), nullable=False)
    units_used = db.Column(db.Float, nullable=False)
    usage_date = db.Column(db.Date, default=datetime.utcnow().date)

class Invoice(db.Model):
    __tablename__ = 'invoices'
    invoice_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cust_id = db.Column(db.Integer, db.ForeignKey('customers.cust_id'), nullable=False)
    billing_month = db.Column(db.String(50), nullable=False)
    total_amount_inr = db.Column(db.Float, nullable=False)
    payment_status = db.Column(db.String(20), default='Unpaid')
