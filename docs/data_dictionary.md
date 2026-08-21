|Dataset Source|
| Property        | Value                  |
| --------------- | ---------------------- |
| Data Source     | Adzuna Jobs API        |
| Response Format | JSON                   |
| Primary Entity  | Job Posting            |
| Sample File     | `sample_response.json` |

|Jobs Table|
| Field                | Data Type     | Nullable | Description                | Source                | Transformation                |
| -------------------- | ------------- | -------- | -------------------------- | --------------------- | ----------------------------- |
| job_id               | VARCHAR(20)   | No       | Unique Adzuna Job ID       | `id`                  | None                          |
| title                | VARCHAR(255)  | No       | Job title                  | `title`               | Trim whitespace               |
| description          | TEXT          | No       | Job description            | `description`         | Clean text                    |
| salary_min           | DECIMAL(10,2) | Yes      | Minimum salary             | `salary_min`          | None                          |
| salary_max           | DECIMAL(10,2) | Yes      | Maximum salary             | `salary_max`          | None                          |
| salary_average       | DECIMAL(10,2) | Yes      | Average salary             | Derived               | `(salary_min + salary_max)/2` |
| salary_predicted     | BOOLEAN       | Yes      | Salary estimated by Adzuna | `salary_is_predicted` | Convert 0/1 to Boolean        |
| contract_time        | VARCHAR(50)   | Yes      | Full-time / Part-time      | `contract_time`       | Standardize values            |
| contract_type        | VARCHAR(50)   | Yes      | Permanent / Contract       | `contract_type`       | Standardize values            |
| created_date         | DATETIME      | No       | Job posting date           | `created`             | Convert to DATETIME           |
| redirect_url         | TEXT          | No       | Original job posting URL   | `redirect_url`        | None                          |
| adref                | TEXT          | No       | Adzuna reference           | `adref`               | None                          |
| company_id           | INT           | No       | FK to Companies            | Derived               | Lookup                        |
| location_id          | INT           | No       | FK to Locations            | Derived               | Lookup                        |
| category_id          | INT           | No       | FK to Categories           | Derived               | Lookup                        |
| extraction_timestamp | DATETIME      | No       | ETL load timestamp         | System Generated      | Current timestamp             |

|Companies Table|
| Field        | Data Type    | Nullable | Description  | Source                 | Transformation     |
| ------------ | ------------ | -------- | ------------ | ---------------------- | ------------------ |
| company_id   | INT          | No       | Primary Key  | Generated              | Auto Increment     |
| company_name | VARCHAR(255) | No       | Company name | `company.display_name` | Trim & standardize |

|Locations Table|
| Field        | Data Type     | Nullable | Description    | Source         |
| ------------ | ------------- | -------- | -------------- | -------------- |
| location_id  | INT           | No       | Primary Key    | Generated      |
| country      | VARCHAR(100)  | No       | Country        | `area[0]`      |
| state        | VARCHAR(100)  | Yes      | State/Province | `area[1]`      |
| county       | VARCHAR(100)  | Yes      | County         | `area[2]`      |
| city         | VARCHAR(100)  | Yes      | City           | `area[3]`      |
| display_name | VARCHAR(255)  | No       | Full location  | `display_name` |
| latitude     | DECIMAL(10,6) | Yes      | Latitude       | `latitude`     |
| longitude    | DECIMAL(10,6) | Yes      | Longitude      | `longitude`    |

|Categories Table|
| Field         | Data Type    | Nullable | Description             | Source           |
| ------------- | ------------ | -------- | ----------------------- | ---------------- |
| category_id   | INT          | No       | Primary Key             | Generated        |
| category_tag  | VARCHAR(100) | No       | API category tag        | `category.tag`   |
| category_name | VARCHAR(255) | No       | Human-readable category | `category.label` |






