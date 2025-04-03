CREATE TABLE IF NOT EXISTS `crypto_currency_value` (
  `id_crypto_currency_value` int(10) UNSIGNED AUTO_INCREMENT,
  `id_crypto` varchar(10),
  `crypto_name` varchar(50),
  `crypto_symbol` varchar(50),
  `date` date,
  `price` float,
  `created_on` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_on` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_crypto_currency_value`),
  UNIQUE KEY `crypto_currency_value_unique_key`(`id_crypto`, `date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE = utf8_unicode_ci;
