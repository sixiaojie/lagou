tee /var/log/installlog/Update_DB_install.log
use lagou;
create table `position` (
  `id` int not null auto_increment,
  `positionId` int not null,
  `positionName` char(30) not null,
  `companyId` int not null,
  `companyShortName` varchar(30) not null,
  `salary` varchar(10) not null,
  `company_type` varchar(20) not null,
  `benifit` varchar(100) not null,
  `district` varchar(20) not null,
  `createTime` varchar(30) ,
  `formatCreateTime` varchar(20),
  `positionAdvantage` varchar(100),
  `firstType` varchar(30),
  `secondType` varchar(30),
  `positionLables` varchar(50),
  `businessZones` varchar(50),
  PRIMARY KEY(id),
  constraint p_c_id unique (positionId,companyId)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
notee