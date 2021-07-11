/* Heat Map */
select distinct Entry.domain , Ip.ip , Ip.country,  Ip.city, Ip.x, Ip.y  from Entry 
JOIN Ip ON Entry.serverIPAddress = Ip.ip 
where Entry.is_page="true";

/*Graph Map */
select SUM(X.count) as count, X.email, X.ip,  X.ip_city , X.ip_x , X.ip_y,   X.server_city, X.server_x, X.server_y  from (select  User.email, count(User.email) as count , User.ip , Ip.city as ip_city , Ip.x as ip_x , Ip.y as ip_y ,  Entry.serverIPAddress, entry_ip.city as server_city, entry_ip.x as server_x, entry_ip.y as server_y 
from User Join Entry on Entry.email=User.email 
left Join Ip on Ip.ip=User.ip  
left Join Ip as entry_ip on entry_ip.ip=Entry.serverIPAddress 
group by User.ip, Entry.serverIPAddress, Entry.email) as X
group by X.server_city, X.email, X.ip ,X.ip_x , X.ip_y, X.server_city, X.server_x, X.server_y;


select SUM(count) as count, serverIPAddress, server_city, server_x, server_y from (select count(User.email) as count, Entry.serverIPAddress, entry_ip.city as server_city, entry_ip.x as server_x, entry_ip.y as server_y \
from User Join Entry on Entry.email=User.email 
left Join Ip on Ip.ip=User.ip  
left Join Ip as entry_ip on entry_ip.ip=Entry.serverIPAddress 
where User.email='simpleanon@tutanota.com' group by User.ip, Entry.serverIPAddress, Entry.email) as ok
group by ok.server_x, ok.server_y;


select count(User.email) as count, Entry.serverIPAddress, entry_ip.city as server_city,   entry_ip.x as server_x, entry_ip.y as server_y \
from User Join Entry on Entry.email=User.email \
left Join Ip on Ip.ip=User.ip  \
left Join Ip as entry_ip on entry_ip.ip=Entry.serverIPAddress \
where User.email=%s group by User.ip, Entry.serverIPAddress, Entry.email 