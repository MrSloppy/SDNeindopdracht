create table customerInfo (
  Klantid  SERIAL primary key ,
  Companyname varchar(100),
  Username varchar(30) NOT NULL UNIQUE ,
  Password varchar(30) NOT NULL ,
  FSAccess boolean,
  PrntAcces boolean,
  LeMinutes int



)

