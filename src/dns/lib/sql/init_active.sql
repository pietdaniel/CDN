create table if not exists 'active' (
  `server` varchar(16) DEFAULT NULL,
  `latency` float(10) DEFAULT 10000.0000,
  `timestamp` long not null default 0,
  primary key (server)
);
