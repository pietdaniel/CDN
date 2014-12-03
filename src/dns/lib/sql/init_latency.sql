create table if not exists 'latency' (
  `authority` boolean NOT NULL DEFAULT False,
  `ip` varchar(16) DEFAULT NULL,
  `server` varchar(16) DEFAULT NULL,
  `latency` float(10) DEFAULT 10000.0000,
  `timestamp` long NOT NULL DEFAULT 0,
  primary key (ip,server)
);
