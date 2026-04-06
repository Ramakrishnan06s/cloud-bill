import os
import sys
from flask import Flask, render_template, jsonify, request, redirect, url_for
from models import db, Customer, ServicePlan, Resource, UsageLog, Invoice
from sqlalchemy import func
from sqlalchemy.orm import joinedload
from datetime import date

# Add local bin to path for any sub-processes if needed
os.environ['PATH'] = os.environ.get('PATH', '') + ':/home/user/.local/bin'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cloud_bill.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def dashboard():
    with app.app_context():
        total_revenue = db.session.query(func.sum(Invoice.total_amount_inr)).scalar() or 0
        customer_count = Customer.query.count()
        resource_count = Resource.query.count()
        pending_invoices = Invoice.query.filter_by(payment_status='Unpaid').count()
        
        recent_usage = UsageLog.query.options(joinedload(UsageLog.customer), joinedload(UsageLog.resource)).order_by(UsageLog.usage_date.desc()).limit(5).all()
        
    return render_template('index.html', 
                           total_revenue=round(total_revenue, 2),
                           customer_count=customer_count,
                           resource_count=resource_count,
                           pending_invoices=pending_invoices,
                           recent_usage=recent_usage)

@app.route('/customers')
def customers():
    all_customers = Customer.query.options(joinedload(Customer.plan)).all()
    all_plans = ServicePlan.query.all()
    return render_template('customers.html', customers=all_customers, plans=all_plans)

@app.route('/usage')
def usage():
    all_usage = UsageLog.query.options(joinedload(UsageLog.customer), joinedload(UsageLog.resource)).order_by(UsageLog.usage_date.desc()).all()
    all_customers = Customer.query.all()
    all_resources = Resource.query.all()
    return render_template('usage.html', usage_logs=all_usage, customers=all_customers, resources=all_resources)

@app.route('/invoices')
def invoices():
    all_invoices = Invoice.query.options(joinedload(Invoice.customer)).all()
    return render_template('invoices.html', invoices=all_invoices)

@app.route('/services')
def services():
    all_resources = Resource.query.all()
    all_plans = ServicePlan.query.all()
    return render_template('services.html', resources=all_resources, plans=all_plans)

@app.route('/api/chart-data')
def chart_data():
    # Read: Dashboard query using JOIN
    revenue_data = db.session.query(
        Invoice.billing_month, 
        func.sum(Invoice.total_amount_inr)
    ).group_by(Invoice.billing_month).all()
    
    usage_data = db.session.query(
        Resource.resource_name, 
        func.sum(UsageLog.units_used)
    ).join(UsageLog).group_by(Resource.resource_name).all()
    
    return jsonify({
        'revenue': {
            'labels': [r[0] for r in revenue_data],
            'values': [float(r[1]) for r in revenue_data]
        },
        'usage': {
            'labels': [u[0] for u in usage_data],
            'values': [float(u[1]) for u in usage_data]
        }
    })

# CREATE: Launch Instance
@app.route('/usage/launch', methods=['POST'])
def launch_instance():
    cust_id = request.form.get('cust_id')
    resource_id = request.form.get('resource_id')
    units = request.form.get('units', type=float)
    
    new_log = UsageLog(cust_id=cust_id, resource_id=resource_id, units_used=units, usage_date=date.today())
    db.session.add(new_log)
    db.session.commit()
    return redirect(url_for('usage'))

# UPDATE: Modify Plan
@app.route('/customers/update-plan', methods=['POST'])
def update_plan():
    cust_id = request.form.get('cust_id')
    plan_id = request.form.get('plan_id')
    
    customer = Customer.query.get(cust_id)
    if customer:
        customer.plan_id = plan_id
        db.session.commit()
    return redirect(url_for('customers'))

# DELETE: Terminate Session
@app.route('/usage/terminate/<int:log_id>', methods=['POST'])
def terminate_session(log_id):
    log = UsageLog.query.get(log_id)
    if log:
        db.session.delete(log)
        db.session.commit()
    return redirect(url_for('usage'))

# ADD: New Customer
@app.route('/customers/add', methods=['POST'])
def add_customer():
    name = request.form.get('name')
    plan_id = request.form.get('plan_id')
    
    new_customer = Customer(name=name, plan_id=plan_id)
    db.session.add(new_customer)
    db.session.commit()
    return redirect(url_for('customers'))

# REMOVE: Delete Customer
@app.route('/customers/remove/<int:cust_id>', methods=['POST'])
def remove_customer(cust_id):
    customer = Customer.query.get(cust_id)
    if customer:
        # Cascade manually: Cleanup usage logs and invoices first
        UsageLog.query.filter_by(cust_id=cust_id).delete()
        Invoice.query.filter_by(cust_id=cust_id).delete()
        db.session.delete(customer)
        db.session.commit()
    return redirect(url_for('customers'))

# Phase 4: Billing Calculation
@app.route('/billing/calculate', methods=['POST'])
def calculate_billing():
    current_month = "April-2026"
    customers = Customer.query.options(joinedload(Customer.plan), joinedload(Customer.usage_logs)).all()
    
    for customer in customers:
        # Base Fee from Plan
        base_fee = customer.plan.monthly_base_fee if customer.plan else 0
        
        # Usage Calculation: Sum(units * rate)
        usage_total = 0
        for log in customer.usage_logs:
            usage_total += (log.units_used * log.resource.unit_price_inr)
        
        final_bill = base_fee + usage_total
        
        # Update existing invoice or create new one
        invoice = Invoice.query.filter_by(cust_id=customer.cust_id, billing_month=current_month).first()
        if invoice:
            invoice.total_amount_inr = round(final_bill, 2)
        else:
            new_invoice = Invoice(
                cust_id=customer.cust_id, 
                billing_month=current_month, 
                total_amount_inr=round(final_bill, 2),
                payment_status='Unpaid'
            )
            db.session.add(new_invoice)
            
    db.session.commit()
    return redirect(url_for('invoices'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
