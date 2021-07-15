delimiter //
CREATE  PROCEDURE Proc2_da()
 BEGIN

    SELECT DISTINCT ISP FROM User;

    SELECT DISTINCT method FROM Entry;

    SELECT DISTINCT content_type FROM Header;

 END//
delimiter ;
