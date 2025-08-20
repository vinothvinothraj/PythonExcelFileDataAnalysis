DROP TABLE IF EXISTS data;
DROP TABLE IF EXISTS events;
DROP TABLE IF EXISTS files;

CREATE TABLE files (
    id INT AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    file_id INT,
    time DATETIME,
    type VARCHAR(255),
    FOREIGN KEY (file_id) REFERENCES files(id)
);

CREATE TABLE data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    file_id INT,
    time DATETIME,
    conductivity FLOAT,
    temperature FLOAT,
    pressure FLOAT,
    sea_pressure FLOAT,
    dissolved_o2_saturation FLOAT,
    chlorophyll_a FLOAT,
    fdom FLOAT,
    turbidity FLOAT,
    depth FLOAT,
    salinity FLOAT,
    speed_of_sound FLOAT,
    specific_conductivity FLOAT,
    density_anomaly FLOAT,
    dissolved_o2_concentration FLOAT,
    FOREIGN KEY (file_id) REFERENCES files(id)
);
