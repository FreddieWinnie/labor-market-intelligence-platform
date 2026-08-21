USE labor_market_intelligence;

CREATE TABLE IF NOT EXISTS sources (
  source_id INT AUTO_INCREMENT PRIMARY KEY,
  source_name VARCHAR(100) NOT NULL UNIQUE,
  base_url VARCHAR(255),
  country VARCHAR(100),

  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
  
);

CREATE TABLE IF NOT EXISTS companies (
  company_id INT AUTO_INCREMENT PRIMARY KEY,
  company_name VARCHAR(100) NOT NULL UNIQUE,

  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
  
);


CREATE TABLE IF NOT EXISTS locations (
  location_id INT AUTO_INCREMENT PRIMARY KEY,
  country VARCHAR(100) NOT NULL UNIQUE,
  state VARCHAR(100),
  county VARCHAR(100),
  city VARCHAR(100),

  display_name VARCHAR(255),

  latitude DECIMAL(10,6),
  longitude DECIMAL(10,6),

  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
  
);


CREATE TABLE IF NOT EXISTS categories (
  category_id INT AUTO_INCREMENT PRIMARY KEY,
  category_tag VARCHAR(100) NOT NULL,
  category_name VARCHAR(255) NOT NULL UNIQUE,

  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
  
);

CREATE TABLE IF NOT EXISTS jobs (
  job_id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  salary_min DECIMAL(10,2),
  salary_max DECIMAL(10,2),
  salary_average DECIMAL(10,2),
  salary_predicted BOOLEAN,

  contract_type VARCHAR(50),
  contract_time VARCHAR(50),
  created_date  DATETIME,
  
  redirect_url TEXT,
  adref TEXT,
  extraction_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,

  company_id INT NOT NULL,
  location_id INT NOT NULL,
  category_id INT NOT NULL,
  source_id INT NOT NULL,

  CONSTRAINT fk_jobs_company
    FOREIGN KEY (company_id)
    REFERENCES companies(company_id),

  CONSTRAINT fk_jobs_location
    FOREIGN KEY (location_id)
    REFERENCES locations(location_id),

  CONSTRAINT fk_jobs_category
    FOREIGN KEY (category_id)
    REFERENCES categories(category_id),

  CONSTRAINT fk_jobs_source
    FOREIGN KEY (source_id)
    REFERENCES sources(source_id)
  
);