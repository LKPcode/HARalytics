delimiter //
CREATE  PROCEDURE Proc3c(IN conArray VARCHAR(5000),IN ispArray VARCHAR(100),IN C BOOLEAN,IN I BOOLEAN)
 BEGIN
 		DECLARE sum INT;
		DECLARE mus INT;

	IF (C = 0 AND I = 0) THEN
        SELECT count(content_type)
		INTO sum
		FROM Header
        INNER JOIN Entry
		ON Entry.resHeader = Header.id
		INNER JOIN User
		ON Entry.email = User.email;

        SELECT count(content_type)
		INTO mus
		FROM mydtbs.Header
		INNER JOIN Entry
		ON Entry.resHeader = Header.id
		INNER JOIN User
		ON Entry.email = User.email
		WHERE (`no-cache`=true OR `no-store`=true
		OR private=true OR public=true);

		SELECT concat(round(( mus/sum * 100 ),2),'%') AS cashed;

    ELSEIF (C = 1 AND I = 0) THEN
		SELECT count(content_type)
		INTO sum
		FROM Header
        INNER JOIN Entry
		ON Entry.resHeader = Header.id
		INNER JOIN User
		ON Entry.email = User.email
		WHERE FIND_IN_SET(content_type, conArray);

		SELECT count(content_type)
		INTO mus
		FROM mydtbs.Header
		INNER JOIN Entry
		ON Entry.resHeader = Header.id
		INNER JOIN User
		ON Entry.email = User.email
		WHERE FIND_IN_SET(content_type, conArray)
		AND (`no-cache`=true OR `no-store`=true
		OR private=true OR public=true);

		SELECT concat(round(( mus/sum * 100 ),2),'%') AS cashed;

	ELSEIF (C = 0 AND I = 1) THEN
		SELECT count(content_type)
		INTO sum
		FROM Header
        INNER JOIN Entry
		ON Entry.resHeader = Header.id
		INNER JOIN User
		ON Entry.email = User.email
		WHERE FIND_IN_SET(isp,ispArray);

		SELECT count(content_type)
		INTO mus
		FROM mydtbs.Header
		INNER JOIN Entry
		ON Entry.resHeader = Header.id
		INNER JOIN User
		ON Entry.email = User.email
		WHERE FIND_IN_SET(isp,ispArray)
		AND (`no-cache`=true OR `no-store`=true
		OR private=true OR public=true);

		SELECT concat(round(( mus/sum * 100 ),2),'%') AS cashed;

    ELSEIF (C= 1 AND I = 1) THEN
		SELECT count(content_type)
		INTO sum
		FROM Header
        INNER JOIN Entry
		ON Entry.resHeader = Header.id
		INNER JOIN User
		ON Entry.email = User.email
		WHERE FIND_IN_SET(content_type, conArray)
        AND FIND_IN_SET(isp,ispArray);

		SELECT count(content_type)
		INTO mus
		FROM mydtbs.Header
		INNER JOIN Entry
		ON Entry.resHeader = Header.id
		INNER JOIN User
		ON Entry.email = User.email
		WHERE FIND_IN_SET(content_type, conArray)
		AND (`no-cache`=true OR `no-store`=true
		OR private=true OR public=true)
        AND FIND_IN_SET(isp,ispArray);

		SELECT concat(round(( mus/sum * 100 ),2),'%') AS cashed;

    ELSE
		SELECT 'FALSE STATEMENT' AS message;

	END IF;

 END//

delimiter ;
