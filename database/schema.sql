-- database: staff.db

CREATE TABLE IF NOT EXISTS staffs(
    name TEXT,
    rfid TEXT,
    PRIMARY KEY (name)
);

CREATE TABLE IF NOT EXISTS records(
    staff_name TEXT,
    check_datetime TEXT,
    io TEXT,
    PRIMARY KEY (staff_name, check_datetime),
    FOREIGN KEY (staff_name) REFERENCES staff_new(name)
);