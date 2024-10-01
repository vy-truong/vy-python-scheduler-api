CREATE DATABASE IF NOT EXISTS employee_info_db;

USE employee_info_db;

CREATE TABLE IF NOT EXISTS employee_role_tb (
    employee_role_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_role_name VARCHAR(100) NOT NULL UNIQUE, 
    employee_role_type VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS employee_info_tb (
    employee_id INT AUTO_INCREMENT PRIMARY KEY, 
    employee_name VARCHAR(250) NOT NULL, 
    employee_email VARCHAR(200) NOT NULL UNIQUE, 
    employee_phone VARCHAR(20),
    employment_type ENUM('Part-time', 'Full-time') NOT NULL,  
    employee_availability JSON,
    employee_role_id INT,
    FOREIGN KEY (employee_role_id) REFERENCES employee_role_tb(employee_role_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert Data
INSERT INTO employee_role_tb (employee_role_name, employee_role_type)
VALUES 
    ('busser', 'Dining Side'),
    ('cook', 'Kitchen Side'),
    ('host', 'Dining Side'),
    ('server', 'Dining Side');

INSERT INTO employee_info_tb (employee_name, employee_email, employee_phone, employment_type, employee_availability, employee_role_id)
VALUES 
    ('John Doe', 'john.doe@gmail.com', '123-456-7890', 'part-time', '["Closing"]', 1),
    ('Jane Smith', 'jane.smith@gmail.com', '987-654-3210', 'full-time', '["Opening","Evening","Closing"]', 4),
    ('Meo Meo', 'meo.meo@gmail.com', '987-654-3210', 'full-time', '["Opening","Evening","Closing"]', 2);
