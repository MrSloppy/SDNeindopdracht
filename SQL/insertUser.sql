insert into customerinfo (companyname, username, password, fsaccess, prntacces, leminutes)  values ('VD', 'Timo', 'Welkom01', false, false, 99);




insert into devicemap (deviceid, port1, port2, port3, port4) values ('of:000070b3d56cd938', 11,12,13,14)

select deviceid,port1outlet,port2outlet,port3outlet,port4outlet from devicemap where 11 IN (port1outlet,port2outlet,port3outlet,port4outlet)


