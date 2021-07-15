delimiter //
CREATE  PROCEDURE Proc3b(IN conArray VARCHAR(5000),IN ispArray VARCHAR(100),IN C BOOLEAN,IN I BOOLEAN)
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
		WHERE (`min-fresh` IS NOT NULL OR `max-stale` IS NOT NULL);

		SELECT concat(round(( mus/sum * 100 ),2),'%') AS max_stale_or_min_fresh;

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
		AND (`min-fresh` IS NOT NULL OR `max-stale` IS NOT NULL);

		SELECT concat(round(( mus/sum * 100 ),2),'%') AS max_stale_or_min_fresh;

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
		AND (`min-fresh` IS NOT NULL OR `max-stale` IS NOT NULL);

		SELECT concat(round(( mus/sum * 100 ),2),'%') AS max_stale_or_min_fresh;

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
		AND (`min-fresh` IS NOT NULL OR `max-stale` IS NOT NULL)
        AND FIND_IN_SET(isp,ispArray);

		SELECT concat(round(( mus/sum * 100 ),2),'%') AS max_stale_or_min_fresh;

    ELSE
		SELECT 'FALSE STATEMENT' AS message;

	END IF;

 END//

delimiter ;
