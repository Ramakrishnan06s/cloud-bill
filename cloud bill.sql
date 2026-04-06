USE CloudResourceDB;

-- 1. Table for Hardware/Resource Rates
CREATE TABLE resource_types (
    resource_id INT PRIMARY KEY,
    resource_name VARCHAR(50), -- e.g., 'RTX 3050', 'NVIDIA A100', 'Standard Storage'
    unit_price_inr DECIMAL(10,2) -- Price per hour or per GB
);

-- 2. Table for Base Plans
CREATE TABLE service_plans (
    plan_id INT PRIMARY KEY,
    plan_name VARCHAR(20), -- 'Basic', 'Developer', 'Enterprise'
    monthly_base_fee DECIMAL(10,2)
);

-- 3. Enhanced Customers Table (linked to a plan)
CREATE TABLE customers_v2 (
    cust_id INT PRIMARY KEY,
    name VARCHAR(100),
    plan_id INT,
    FOREIGN KEY (plan_id) REFERENCES service_plans(plan_id)
);

-- 4. Raw Usage Logs (Tracks specific sessions)
CREATE TABLE usage_logs (
    log_id INT PRIMARY KEY AUTO_INCREMENT,
    cust_id INT,
    resource_id INT,
    units_used DECIMAL(10,2), -- hours or GB
    usage_date DATE,
    FOREIGN KEY (cust_id) REFERENCES customers_v2(cust_id),
    FOREIGN KEY (resource_id) REFERENCES resource_types(resource_id)
);

-- 5. Final Invoices Table
CREATE TABLE invoices (
    invoice_id INT PRIMARY KEY AUTO_INCREMENT,
    cust_id INT,
    billing_month VARCHAR(20),
    total_amount_inr DECIMAL(10,2),
    payment_status VARCHAR(20) DEFAULT 'Unpaid',
    FOREIGN KEY (cust_id) REFERENCES customers_v2(cust_id)
);













USE CloudResourceDB;

-- TABLE 3: GPU Inventory (Defining the "Next Values" for Hardware)
CREATE TABLE gpu_tiers (
    gpu_id INT PRIMARY KEY,
    model_name VARCHAR(50),
    hourly_rate_inr DECIMAL(10,2)
);

INSERT INTO gpu_tiers VALUES 
(1, 'RTX 3050 (Basic)', 40.00),
(2, 'RTX 4090 (Gaming)', 80.00),
(3, 'NVIDIA A100 (AI Pro)', 150.00);

-- TABLE 4: Subscription Plans
CREATE TABLE sub_plans (
    plan_id INT PRIMARY KEY,
    plan_name VARCHAR(20),
    base_monthly_fee DECIMAL(10,2)
);

INSERT INTO sub_plans VALUES 
(1, 'Student', 200.00),
(2, 'Developer', 1000.00);

-- TABLE 5: Payment Status Tracking
CREATE TABLE payment_log (
    pay_id INT PRIMARY KEY AUTO_INCREMENT,
    cust_id INT,
    amount_paid DECIMAL(10,2),
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cust_id) REFERENCES customers(cust_id)
);

-- ADDING NEXT VALUES TO YOUR BILLING LOGIC
-- Let's simulate a Pro user using an A100 GPU
INSERT INTO billing (cust_id, billing_month, gpu_hours, storage_gb) 
VALUES (101, 'April-2026', 15.0, 250);

-- Query to see everything combined (The "Professional" Output)
SELECT 
    c.name AS 'User',
    g.model_name AS 'Hardware',
    s.plan_name AS 'Plan',
    b.total_inr AS 'Final Bill'
FROM customers c
JOIN billing b ON c.cust_id = b.cust_id
JOIN gpu_tiers g ON g.gpu_id = 1 -- Simulating assigning a GPU tier
JOIN sub_plans s ON s.plan_id = 1;