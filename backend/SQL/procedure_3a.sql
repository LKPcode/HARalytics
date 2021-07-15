delimiter //
CREATE  PROCEDURE Proc3a(IN conArray VARCHAR(5000),IN ispArray VARCHAR(5000),IN C BOOLEAN,IN I BOOLEAN)
 BEGIN
	declare sum int;
    declare mus int;

	IF (C = 0 AND I = 0) THEN
        SELECT `max-age`, count(content_type) as plhthos
		FROM Header
		INNER JOIN Entry
		ON Entry.resHeader = Header.id
		INNER JOIN User
		ON Entry.email = User.email
		WHERE `max-age` is NOT NULL
		AND content_type is NOT NULL
		GROUP BY `max-age`;

		SELECT TIMESTAMPDIFF(SECOND,last_modified,expires) AS `dif-max-age`, count(content_type)  as plhthos
		FROM Header
		INNER JOIN Entry
		ON Entry.resHeader = Header.id
		INNER JOIN User
		ON Entry.email = User.email
		WHERE `max-age` is null
		AND expires is not null
		AND last_modified is not null
		AND Entry.email like "top21%"
		AND content_type is NOT NULL
		GROUP BY `dif-max-age`;


    ELSEIF (C = 1 AND I = 0) THEN
        SELECT `max-age`, count(content_type) as plhthos
		FROM Header
		INNER JOIN Entry
		ON Entry.resHeader = Header.id
		INNER JOIN User
		ON Entry.email = User.email
        WHERE FIND_IN_SET(content_type, conArray)
		AND `max-age` is NOT NULL
		AND content_type is NOT NULL
		GROUP BY `max-age`;

		SELECT TIMESTAMPDIFF(SECOND,last_modified,expires) AS `dif-max-age`, count(content_type)  as plhthos
		FROM Header
		INNER JOIN Entry
		ON Entry.resHeader = Header.id
		INNER JOIN User
		ON Entry.email = User.email
		WHERE `max-age` is null
		AND expires is not null
		AND last_modified is not null
		AND Entry.email like "top21%"
		AND content_type is NOT NULL
		GROUP BY `dif-max-age`;

	ELSEIF (C = 0 AND I = 1) THEN
        SELECT `max-age`, count(content_type) as plhthos
		FROM Header
		INNER JOIN Entry
		ON Entry.resHeader = Header.id
		INNER JOIN User
		ON Entry.email = User.email
        WHERE FIND_IN_SET(isp,ispArray)
		AND `max-age` is NOT NULL
		AND content_type is NOT NULL
		GROUP BY `max-age`;

		SELECT TIMESTAMPDIFF(SECOND,last_modified,expires) AS `dif-max-age`, count(content_type)  as plhthos
		FROM Header
		INNER JOIN Entry
		ON Entry.resHeader = Header.id
		INNER JOIN User
		ON Entry.email = User.email
		WHERE `max-age` is null
		AND expires is not null
		AND last_modified is not null
		AND Entry.email like "top21%"
		AND FIND_IN_SET(isp,ispArray)
		GROUP BY `dif-max-age`;

    ELSEIF (C= 1 AND I = 1) THEN
        SELECT `max-age`, count(content_type) as plhthos
		FROM Header
		INNER JOIN Entry
		ON Entry.resHeader = Header.id
		INNER JOIN User
		ON Entry.email = User.email
        WHERE FIND_IN_SET(content_type, conArray)
		AND FIND_IN_SET(isp,ispArray)
		AND `max-age` is NOT NULL
		AND content_type is NOT NULL
		GROUP BY `max-age`;

		SELECT TIMESTAMPDIFF(SECOND,last_modified,expires) AS `dif-max-age`, count(content_type)  as plhthos
		FROM Header
		INNER JOIN Entry
		ON Entry.resHeader = Header.id
		INNER JOIN User
		ON Entry.email = User.email
		WHERE `max-age` is null
		AND expires is not null
		AND last_modified is not null
		AND Entry.email like "top21%"
		AND FIND_IN_SET(content_type, conArray)
		AND FIND_IN_SET(isp,ispArray)
		GROUP BY `dif-max-age`;

    ELSE
		SELECT 'FALSE STATEMENT' AS message;

	END IF;

 END//
delimiter ;
