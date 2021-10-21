-- phpMyAdmin SQL Dump
-- version 4.9.4
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Oct 03, 2020 at 11:44 AM
-- Server version: 5.6.41-84.1
-- PHP Version: 7.3.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `jrobles_agentebitcoin`
--

-- --------------------------------------------------------

--
-- Table structure for table `ab_paymethod`
--

CREATE TABLE `ab_paymethod` (
  `paymethod_id` int(11) NOT NULL,
  `paymethod_group_id` int(11) NOT NULL,
  `description` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `ab_paymethod`
--

INSERT INTO `ab_paymethod` (`paymethod_id`, `paymethod_group_id`, `description`, `status`) VALUES
(1, 1, 'BCP Banco de Crédito', 1),
(2, 1, 'BBVA Banco Continental', 1),
(3, 1, 'Interbank', 1),
(4, 1, 'Scotiabank', 1),
(5, 2, 'Tarjeta de Crédito', 1),
(6, 2, 'Saldo Mercado Libre', 1),
(7, 2, 'Saldo PayPal', 1);

-- --------------------------------------------------------

--
-- Table structure for table `ab_paymethod_group`
--

CREATE TABLE `ab_paymethod_group` (
  `paymethod_group_id` int(11) NOT NULL,
  `description` varchar(128) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `ab_paymethod_group`
--

INSERT INTO `ab_paymethod_group` (`paymethod_group_id`, `description`) VALUES
(1, 'Transferencia o Depósito Bancario'),
(2, 'Otros Medios de Pago (+5%)');

-- --------------------------------------------------------

--
-- Table structure for table `ab_trade`
--

CREATE TABLE `ab_trade` (
  `trade_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `btcToBuy` decimal(10,8) NOT NULL,
  `currencyCode` varchar(3) COLLATE utf8_unicode_ci NOT NULL,
  `walletAddress` varchar(64) COLLATE utf8_unicode_ci NOT NULL,
  `payMethod` int(11) NOT NULL,
  `basePrice` decimal(10,2) NOT NULL,
  `commissionPercentage` decimal(5,4) NOT NULL,
  `priceToPay` decimal(10,2) NOT NULL,
  `trade_creation` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `trade_completion` datetime DEFAULT NULL,
  `trade_status` int(11) NOT NULL DEFAULT '0',
  `trade_coin` varchar(3) COLLATE utf8_unicode_ci NOT NULL DEFAULT 'BTC',
  `trade_txid` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `ab_user`
--

CREATE TABLE `ab_user` (
  `user_id` int(11) NOT NULL,
  `creation_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `trust_level` int(11) NOT NULL DEFAULT '0',
  `given_name` varchar(250) COLLATE utf8_unicode_ci NOT NULL,
  `family_name` varchar(250) COLLATE utf8_unicode_ci NOT NULL,
  `email` varchar(250) COLLATE utf8_unicode_ci NOT NULL,
  `birth_date` date DEFAULT NULL,
  `address_line1` varchar(250) COLLATE utf8_unicode_ci DEFAULT NULL,
  `address_line2` varchar(250) COLLATE utf8_unicode_ci DEFAULT NULL,
  `address_country` varchar(2) COLLATE utf8_unicode_ci DEFAULT NULL,
  `telephone_number` varchar(16) COLLATE utf8_unicode_ci DEFAULT NULL,
  `document_country` varchar(2) COLLATE utf8_unicode_ci DEFAULT NULL,
  `document_type` varchar(3) COLLATE utf8_unicode_ci DEFAULT NULL,
  `document_number` varchar(16) COLLATE utf8_unicode_ci DEFAULT NULL,
  `document2_country` varchar(2) COLLATE utf8_unicode_ci DEFAULT NULL,
  `document2_type` varchar(3) COLLATE utf8_unicode_ci DEFAULT NULL,
  `document2_number` varchar(16) COLLATE utf8_unicode_ci DEFAULT NULL,
  `google_id` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `verified_telephone` int(11) NOT NULL DEFAULT '0',
  `verified_document` int(11) NOT NULL DEFAULT '0',
  `verified_document2` int(11) NOT NULL DEFAULT '0',
  `verified_address` int(11) NOT NULL DEFAULT '0',
  `status` int(11) NOT NULL DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `ab_paymethod`
--
ALTER TABLE `ab_paymethod`
  ADD PRIMARY KEY (`paymethod_id`);

--
-- Indexes for table `ab_paymethod_group`
--
ALTER TABLE `ab_paymethod_group`
  ADD PRIMARY KEY (`paymethod_group_id`);

--
-- Indexes for table `ab_trade`
--
ALTER TABLE `ab_trade`
  ADD PRIMARY KEY (`trade_id`);

--
-- Indexes for table `ab_user`
--
ALTER TABLE `ab_user`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `google_id` (`google_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `ab_paymethod`
--
ALTER TABLE `ab_paymethod`
  MODIFY `paymethod_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `ab_paymethod_group`
--
ALTER TABLE `ab_paymethod_group`
  MODIFY `paymethod_group_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `ab_trade`
--
ALTER TABLE `ab_trade`
  MODIFY `trade_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `ab_user`
--
ALTER TABLE `ab_user`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
