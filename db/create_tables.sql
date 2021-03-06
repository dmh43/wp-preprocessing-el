CREATE TABLE IF NOT EXISTS pages (
`id` bigint(20) NOT NULL auto_increment,
`source_id` bigint(20),
`title` varchar(255) CHARACTER SET utf8mb4 NOT NULL,
`content` MEDIUMTEXT CHARACTER SET utf8mb4 NOT NULL,
`source` varchar(255) NOT NULL,
`is_seed_page` boolean NOT NULL,
`is_disambiguation_page` boolean NOT NULL,
PRIMARY KEY (`id`),
INDEX (`source_id`),
UNIQUE KEY (`source`, `source_id`)
);

CREATE TABLE IF NOT EXISTS categories (
`id` bigint(20) NOT NULL auto_increment,
`category` varchar(255) CHARACTER SET utf8mb4 NOT NULL UNIQUE,

PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS page_categories (
`id` bigint(20) NOT NULL auto_increment,
`category_id` bigint(20) NOT NULL,
`page_id` bigint(20) NOT NULL,

PRIMARY KEY (`id`),
INDEX (`page_id`),

FOREIGN KEY (`page_id`)
REFERENCES pages(`id`)
ON UPDATE CASCADE ON DELETE CASCADE,

FOREIGN KEY (`category_id`)
REFERENCES categories(`id`)
ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS entities (
`id` bigint(20) NOT NULL auto_increment,
`text` varchar(255) CHARACTER SET utf8mb4 NOT NULL UNIQUE,
PRIMARY KEY  (`id`),
INDEX (`text`)
);

CREATE TABLE IF NOT EXISTS mentions (
`id` bigint(20) NOT NULL auto_increment,
`text` varchar(255) CHARACTER SET utf8mb4 NOT NULL,
`offset` INT NOT NULL,
`page_id` bigint(20) NOT NULL,

PRIMARY KEY (`id`),
INDEX (`text`),

FOREIGN KEY (`page_id`)
REFERENCES pages(`id`)
ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS entity_mentions (
`id` bigint(20) NOT NULL auto_increment,
`entity_id` bigint(20) NOT NULL,
`mention_id` bigint(20) NOT NULL UNIQUE,

PRIMARY KEY  (`id`),
INDEX (`entity_id`),

FOREIGN KEY (`entity_id`)
REFERENCES entities(`id`)
ON UPDATE CASCADE ON DELETE CASCADE,

FOREIGN KEY (`mention_id`)
REFERENCES mentions(`id`)
ON UPDATE CASCADE ON DELETE CASCADE
);
