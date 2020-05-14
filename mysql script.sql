CREATE TABLE iot(
    id varchar(255) NOT NULL,
    pir varchar(255),
    ultrasonic_table varchar(255),
    time_col TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);	

SELECT @@global.time_zone;
SET GLOBAL time_zone = '+8:00';

CREATE TABLE occupancy(
    id varchar(255) NOT NULL,
    occ_status varchar(255),
    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP  ON UPDATE CURRENT_TIMESTAMP NOT NULL
);	

CREATE TABLE occ_data(
    id varchar(255) NOT NULL,
    occ_status varchar(255),
    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP  ON UPDATE CURRENT_TIMESTAMP NOT NULL
);	

INSERT INTO occ_data(id, occ_status) VALUES 
('ce5bbf82f163', 'EMPTY');

select * from iot;

select * from iot where id='ce5bbf82f163';
select * from occupancy;

UPDATE occupancy SET occ_status = 'EMPTY' WHERE id = 'ce5bbf82f163';
