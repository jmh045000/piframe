DROP TABLE IF EXISTS images;
DROP TABLE IF EXISTS displayed_images;

CREATE TABLE images (
    image_id INTEGER PRIMARY KEY AUTOINCREMENT,
    path TEXT UNIQUE,
    folder_id INT NOT NULL
);

CREATE TABLE displayed_images (
    image_id INT,
    FOREIGN KEY (image_id) REFERENCES images (image_id)
);

CREATE TEMP VIEW undisplayed_images AS SELECT t.* FROM images t
    LEFT JOIN displayed_images d ON t.image_id = d.image_id
    WHERE d.image_id IS NULL;

CREATE TEMP VIEW undisplayed_folders AS SELECT DISTINCT folder_id FROM undisplayed_images;
