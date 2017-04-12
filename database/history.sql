tee /var/log/installlog/Update_DB_install.log
drop database if EXISTS lagou;
create database lagou DEFAULT CHARACTER SET utf8;
use lagou;
create table `history` (
  `id` tinyint(4) NOT NULL AUTO_INCREMENT,
  `search_position` varchar(20) NOT NULL,
  `city` char(10) not null,
  `total_num` int,
  `search_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  primary key(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
notee
