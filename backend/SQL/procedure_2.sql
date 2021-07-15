delimiter //
CREATE  PROCEDURE Proc2(IN ispArray VARCHAR(5000),		-- array with ISPs
						IN conArray VARCHAR(5000),		-- array with CONTENT-TYPES
                        IN dayArray VARCHAR(5000),		-- array with days of the week
						IN methodArray VARCHAR(5000),	-- array with HTTP methods
                        IN I BOOLEAN,IN C BOOLEAN,IN D BOOLEAN,IN M BOOLEAN)
						-- if I==0 select all ISPs
						-- if C==0 select all CONTENT_TYPES
						-- if D==0 select all days
						-- if M==0 select all HTTP methods
 BEGIN

		SELECT HOUR(startedDateTime)AS hours,cast(AVG(wait) as FLOAT) AS time
		FROM Entry
		INNER JOIN User
		ON Entry.email = User.email
        INNER JOIN Header
		ON Entry.resHeader = Header.id OR Entry.reqHeader = Header.id
        WHERE IF ( I=1, FIND_IN_SET(isp,ispArray), isp LIKE '%')
        AND IF( C= 1, FIND_IN_SET(content_type,conArray), 1=1)
        AND IF( D= 1, FIND_IN_SET(day,dayArray), 1=1)
        AND IF( M= 1, FIND_IN_SET(method,methodArray), 1=1)
		GROUP BY HOUR(startedDateTime);

 END//
delimiter ;
