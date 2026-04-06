import os
from flask import Flask
from models import db, ServicePlan, Resource, Customer, UsageLog, Invoice
from datetime import date

def init_db():
    app = Flask(__name__)
    if not os.path.exists(app.instance_path):
        os.makedirs(app.instance_path)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cloud_bill.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        db.drop_all()
        db.create_all()

        # Service Plans (With more details for our comparison grid)
        plans = [
            ServicePlan(plan_id=1, plan_name='Basic', monthly_base_fee=200.00),
            ServicePlan(plan_id=2, plan_name='Developer', monthly_base_fee=1000.00),
            ServicePlan(plan_id=3, plan_name='Enterprise', monthly_base_fee=5000.00)
        ]
        db.session.add_all(plans)

        # Expanded Hypercloud Resource Catalog
        resources = [
            # Entry/Standard Tier
            Resource(resource_id=1, resource_name='RTX 3050 (Basic 4GB)', unit_price_inr=40.00),
            Resource(resource_id=4, resource_name='Standard Storage (GB)', unit_price_inr=0.50),
            
            # Mid/Pro Tier
            Resource(resource_id=5, resource_name='RTX 4060 (Pro 8GB)', unit_price_inr=60.00),
            Resource(resource_id=2, resource_name='RTX 4090 (Gaming 24GB)', unit_price_inr=80.00),
            
            # Elite/AI Tier
            Resource(resource_id=3, resource_name='NVIDIA A100 (AI 80GB)', unit_price_inr=150.00),
            Resource(resource_id=6, resource_name='RTX 5090 (Elite 16GB)', unit_price_inr=250.00),
            
            # Storage Specific
            Resource(resource_id=7, resource_name='1TB NVMe Storage (Monthly)', unit_price_inr=500.00)
        ]
        db.session.add_all(resources)

        # Tamil User Base
        customers = [
            Customer(cust_id=101, name='Suthan', plan_id=3),
            Customer(cust_id=102, name='Akash', plan_id=1),
            Customer(cust_id=103, name='Kavin', plan_id=3),
            Customer(cust_id=104, name='Rahul', plan_id=2),
            Customer(cust_id=105, name='Sanjay', plan_id=1)
        ]
        db.session.add_all(customers)

        # Baseline Usage Logs
        logs = [
            UsageLog(cust_id=101, resource_id=6, units_used=10.0, usage_date=date(2026, 4, 1)), # Suthan -> 5090 Elite
            UsageLog(cust_id=102, resource_id=5, units_used=30.0, usage_date=date(2026, 4, 2)), # Akash -> 4060 Pro
            UsageLog(cust_id=103, resource_id=3, units_used=20.0, usage_date=date(2026, 4, 3)), # Kavin -> A100
            UsageLog(cust_id=104, resource_id=7, units_used=1.0, usage_date=date(2026, 4, 1))  # Rahul -> 1TB Dedicated
        ]
        db.session.add_all(logs)

        db.session.commit()
        print(f"Hypercloud Elite catalog and users initialized successfully!")

if __name__ == '__main__':
    init_db()
