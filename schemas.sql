CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    session_token TEXT,
    type VARCHAR(50) CHECK (type IN ('consumer', 'manufacturer', 'installer', 'manufacturer&installer')) DEFAULT 'consumer',
    register_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE consumers (
    id SERIAL PRIMARY KEY,
    user_id INT UNIQUE,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    address TEXT,
    account_id INT UNIQUE,
    register_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (account_id) REFERENCES accounts(id)
);

CREATE TABLE installers (
    id SERIAL PRIMARY KEY,
    user_id INT UNIQUE,
    comp_name VARCHAR(255) NOT NULL,
    address TEXT,
    zip_code VARCHAR(20),
    account_id INT UNIQUE,
    company_reg_number VARCHAR(255) UNIQUE,
    company_size VARCHAR(50),
    register_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (account_id) REFERENCES accounts(id)
);
CREATE TABLE manufacturers (
    id SERIAL PRIMARY KEY,
    user_id INT UNIQUE,
    comp_name VARCHAR(255) NOT NULL,
    address TEXT,
    zip_code VARCHAR(20),
    account_id INT UNIQUE,
    comp_register_number VARCHAR(255) UNIQUE,
    company_size VARCHAR(50),
    register_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (account_id) REFERENCES accounts(id)
);
CREATE TABLE accounts (
    id SERIAL PRIMARY KEY,
    user_id INT UNIQUE,
    name VARCHAR(255) NOT NULL,
    surname VARCHAR(255) NOT NULL,
    company_name VARCHAR(255),
    balance_nok DECIMAL(15, 2),
    register_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    bank_card_number VARCHAR(20) UNIQUE,
    bank VARCHAR(255),
    cvv VARCHAR(3),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
CREATE TABLE shares (
    id SERIAL PRIMARY KEY,
    amount_nok DECIMAL(15, 2) NOT NULL,
    account_id INT,
    project_id INT,
    percentage_share DECIMAL(5, 2),
    profit_margin DECIMAL(5, 2),
    register_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts(id),
    FOREIGN KEY (project_id) REFERENCES projects(id)
);
CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    share_id INT,
    installer_id INT,
    manufacturer_id INT,
    location TEXT,
    name VARCHAR(255) NOT NULL,
    type_of_facility VARCHAR(255),
    capacity DECIMAL(10, 2),
    realtime_electricity_generation DECIMAL(10, 2),
    number_of_shares INT,
    cost_nok DECIMAL(15, 2),
    money_required DECIMAL(15, 2),
    money_spent DECIMAL(15, 2),
    money_left DECIMAL(15, 2),
    electricity_generation_prediction TEXT,
    manufacturer_status VARCHAR(50),
    installer_status VARCHAR(50),
    funded_status VARCHAR(50),
    register_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (share_id) REFERENCES shares(id),
    FOREIGN KEY (installer_id) REFERENCES installers(id),
    FOREIGN KEY (manufacturer_id) REFERENCES manufacturers(id)
);
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    manufacturer_id INT,
    project_id INT,
    name VARCHAR(255) NOT NULL,
    category_id INT,
    register_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (manufacturer_id) REFERENCES manufacturers(id),
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (category_id) REFERENCES categories(id)
);
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    reg_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE images (
    id SERIAL PRIMARY KEY,
    category_id INT,
    register_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);
CREATE TABLE manufacturer_product (
    manufacturer_id INT,
    product_id INT,
    PRIMARY KEY (manufacturer_id, product_id),
    FOREIGN KEY (manufacturer_id) REFERENCES manufacturers(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);
