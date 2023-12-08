-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Dec 08, 2023 at 02:56 AM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `airticket`
--

-- --------------------------------------------------------

--
-- Table structure for table `Airline`
--

CREATE TABLE `Airline` (
  `name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `Airline`
--

INSERT INTO `Airline` (`name`) VALUES
('Jet Blue');

-- --------------------------------------------------------

--
-- Table structure for table `Airline_Staff`
--

CREATE TABLE `Airline_Staff` (
  `username` varchar(255) NOT NULL,
  `air_password` varchar(255) NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `date_of_birth` date NOT NULL,
  `Airline_name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `Airline_Staff`
--

INSERT INTO `Airline_Staff` (`username`, `air_password`, `first_name`, `last_name`, `date_of_birth`, `Airline_name`) VALUES
('111', '698d51a19d8a121ce581499d7b701668', '111', '111', '2023-12-20', 'Jet Blue'),
('112', '7f6ffaa6bb0b408017b62254211691b5', '1', '1', '2023-12-04', 'Jet Blue'),
('Andrew', '81dc9bdb52d04dc20036dbd8313ed055', 'Andrew', 'Zhang', '2023-12-14', 'Jet Blue'),
('Helen', '81dc9bdb52d04dc20036dbd8313ed055', 'Helen', 'Yuan', '2023-12-18', 'Jet Blue'),
('Sarah', '81dc9bdb52d04dc20036dbd8313ed055', 'Sarah', 'Lamond', '2023-12-05', 'Jet Blue'),
('staff', '81dc9bdb52d04dc20036dbd8313ed055', 'Sta', 'ff', '2023-12-03', 'Jet Blue');

-- --------------------------------------------------------

--
-- Table structure for table `AirPlane`
--

CREATE TABLE `AirPlane` (
  `name` varchar(255) NOT NULL,
  `id_num` varchar(255) NOT NULL,
  `num_of_seats` int(11) NOT NULL,
  `manu_company` varchar(255) NOT NULL,
  `model_num` int(11) NOT NULL,
  `manu_date` date NOT NULL,
  `age` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `AirPlane`
--

INSERT INTO `AirPlane` (`name`, `id_num`, `num_of_seats`, `manu_company`, `model_num`, `manu_date`, `age`) VALUES
('Jet Blue', '12345', 246, 'Boeing', 787, '2005-07-31', 18),
('Jet Blue', '13579', 80, 'Andrew', 939, '2023-12-01', 0),
('Jet Blue', '23456', 147, 'Airbus', 320, '2013-01-11', 10),
('Jet Blue', '24680', 90, 'sdfsdfsd', 123, '2023-12-21', 3),
('Jet Blue', '34567', 345, 'Boeing', 777, '2023-11-08', 0),
('Jet Blue', '98473', 890, 'ANdrew', 264, '2002-10-03', 21);

-- --------------------------------------------------------

--
-- Table structure for table `Airport`
--

CREATE TABLE `Airport` (
  `air_code` char(3) NOT NULL,
  `name` varchar(255) NOT NULL,
  `city` varchar(255) NOT NULL,
  `country` varchar(255) NOT NULL,
  `num_of_terminal` int(11) DEFAULT NULL,
  `type` enum('domestic','international','both') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `Airport`
--

INSERT INTO `Airport` (`air_code`, `name`, `city`, `country`, `num_of_terminal`, `type`) VALUES
('JFK', 'John F. Kennedy Airport', 'New York', 'USA', 5, 'both'),
('NRE', 'OIE', 'sdfds', 'sdfds', 3, 'both'),
('PVG', 'Shanghai Pudong International Airport', 'Shanghai', 'CNH', 2, 'both'),
('SZA', 'Shenzhen Airport', 'Shenzhen', 'CHN', 3, 'both'),
('SZC', 'Shenzhen Airport', 'Shenzhen', 'CHN', 3, 'both');

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

CREATE TABLE `customer` (
  `email` varchar(255) NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `customer_password` varchar(255) NOT NULL,
  `building_num` varchar(255) NOT NULL,
  `street` varchar(255) NOT NULL,
  `apt_num` varchar(255) NOT NULL,
  `city` varchar(255) NOT NULL,
  `state` varchar(255) NOT NULL,
  `zip_code` int(11) NOT NULL,
  `passport_num` varchar(255) NOT NULL,
  `passport_exp` date NOT NULL,
  `passport_country` varchar(255) NOT NULL,
  `date_of_birth` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`email`, `first_name`, `last_name`, `customer_password`, `building_num`, `street`, `apt_num`, `city`, `state`, `zip_code`, `passport_num`, `passport_exp`, `passport_country`, `date_of_birth`) VALUES
('cus@email.com', 'cus', 'tomer', '81dc9bdb52d04dc20036dbd8313ed055', '370', 'jay', '121', 'nyc', 'NY', 11201, 'E505005', '2023-12-19', 'CHN', '2023-12-03'),
('jianheng_zhang@163.com', 'Andrew', 'Zhang', '81dc9bdb52d04dc20036dbd8313ed055', '1', 'sdfsdf', '1', 'sdfsdf', 'sdfsd', 11201, 'sdfsdf', '2023-12-12', 'sdfsdf', '2023-12-12');

-- --------------------------------------------------------

--
-- Table structure for table `customer_phone_number`
--

CREATE TABLE `customer_phone_number` (
  `email` varchar(255) NOT NULL,
  `phone_num` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `customer_phone_number`
--

INSERT INTO `customer_phone_number` (`email`, `phone_num`) VALUES
('cus@email.com', '1234567890');

-- --------------------------------------------------------

--
-- Table structure for table `cus_comment`
--

CREATE TABLE `cus_comment` (
  `id_num_ticket` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `comments` varchar(255) DEFAULT NULL,
  `rate` int(5) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `cus_comment`
--

INSERT INTO `cus_comment` (`id_num_ticket`, `email`, `comments`, `rate`) VALUES
('2402', 'jianheng_zhang@163.com', 'sdfsadf', 4);

-- --------------------------------------------------------

--
-- Table structure for table `Flight`
--

CREATE TABLE `Flight` (
  `name` varchar(255) NOT NULL,
  `id_num` varchar(255) NOT NULL,
  `dept_date` date NOT NULL,
  `dept_time` time NOT NULL,
  `flight_num` int(11) NOT NULL,
  `dept_airport` char(3) NOT NULL,
  `arri_date` date NOT NULL,
  `arri_time` time NOT NULL,
  `base_price` decimal(18,2) NOT NULL,
  `flight_status` enum('delayed','on-time','canceled') NOT NULL,
  `arri_airport` char(3) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `Flight`
--

INSERT INTO `Flight` (`name`, `id_num`, `dept_date`, `dept_time`, `flight_num`, `dept_airport`, `arri_date`, `arri_time`, `base_price`, `flight_status`, `arri_airport`) VALUES
('Jet Blue', '12345', '2023-12-01', '12:30:00', 3243, 'JFK', '2023-12-02', '12:01:00', 12345.00, 'on-time', 'PVG'),
('Jet Blue', '12345', '2023-12-13', '12:00:00', 32423, 'JFK', '2023-12-20', '00:20:00', 8000.00, 'on-time', 'PVG'),
('Jet Blue', '12345', '2023-12-24', '14:36:00', 2375, 'PVG', '2023-12-25', '09:28:00', 5000.00, 'delayed', 'JFK'),
('Jet Blue', '12345', '2023-12-25', '12:30:00', 12345, 'JFK', '2023-12-28', '12:30:00', 1000.00, 'on-time', 'PVG'),
('Jet Blue', '12345', '2023-12-28', '12:30:00', 567, 'JFK', '2023-12-29', '12:30:00', 3000.00, 'on-time', 'PVG'),
('Jet Blue', '23456', '2023-12-25', '07:24:00', 8989, 'JFK', '2023-12-25', '02:58:00', 6000.00, 'delayed', 'PVG');

-- --------------------------------------------------------

--
-- Table structure for table `Inside`
--

CREATE TABLE `Inside` (
  `air_code` char(3) NOT NULL,
  `name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `Inside`
--

INSERT INTO `Inside` (`air_code`, `name`) VALUES
('JFK', 'Jet Blue'),
('NRE', 'Jet Blue'),
('PVG', 'Jet Blue'),
('SZC', 'Jet Blue');

-- --------------------------------------------------------

--
-- Table structure for table `maintainance`
--

CREATE TABLE `maintainance` (
  `name` varchar(255) NOT NULL,
  `id_num` varchar(255) NOT NULL,
  `start_date` date NOT NULL,
  `start_time` time NOT NULL,
  `end_date` date NOT NULL,
  `end_time` time NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `maintainance`
--

INSERT INTO `maintainance` (`name`, `id_num`, `start_date`, `start_time`, `end_date`, `end_time`) VALUES
('Jet Blue', '12345', '2023-12-27', '12:00:00', '2023-12-31', '12:00:00');

-- --------------------------------------------------------

--
-- Table structure for table `of`
--

CREATE TABLE `of` (
  `name` varchar(255) NOT NULL,
  `id_num_ap` varchar(255) NOT NULL,
  `dept_date` date NOT NULL,
  `dept_time` time NOT NULL,
  `flight_num` int(11) NOT NULL,
  `id_num_ticket` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `of`
--

INSERT INTO `of` (`name`, `id_num_ap`, `dept_date`, `dept_time`, `flight_num`, `id_num_ticket`) VALUES
('Jet Blue', '12345', '2023-12-01', '12:30:00', 3243, '2402'),
('Jet Blue', '12345', '2023-12-28', '12:30:00', 567, '3543');

-- --------------------------------------------------------

--
-- Table structure for table `purchase`
--

CREATE TABLE `purchase` (
  `id_num` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `card_type` varchar(255) NOT NULL,
  `card_num` varchar(255) NOT NULL,
  `name_on_card` varchar(255) NOT NULL,
  `exp_date` date NOT NULL,
  `date_purchase` date NOT NULL,
  `time_purchase` time NOT NULL,
  `passenger_name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `purchase`
--

INSERT INTO `purchase` (`id_num`, `email`, `card_type`, `card_num`, `name_on_card`, `exp_date`, `date_purchase`, `time_purchase`, `passenger_name`) VALUES
('2402', 'jianheng_zhang@163.com', '111', '1111', '1111', '2023-12-04', '2023-12-07', '20:38:16', '1111'),
('3543', 'jianheng_zhang@163.com', 'kk', 'kk', 'kk', '2023-12-26', '2023-12-07', '19:35:24', 'kk');

-- --------------------------------------------------------

--
-- Table structure for table `staff_email`
--

CREATE TABLE `staff_email` (
  `username` varchar(255) NOT NULL,
  `email_address` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `staff_email`
--

INSERT INTO `staff_email` (`username`, `email_address`) VALUES
('111', '111'),
('112', '111'),
('staff', 'email1@nyu.edu'),
('staff', 'email2@nyu.edu');

-- --------------------------------------------------------

--
-- Table structure for table `staff_phone_num`
--

CREATE TABLE `staff_phone_num` (
  `username` varchar(255) NOT NULL,
  `phone_num` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `staff_phone_num`
--

INSERT INTO `staff_phone_num` (`username`, `phone_num`) VALUES
('111', ''),
('112', ''),
('staff', '1234567890');

-- --------------------------------------------------------

--
-- Table structure for table `ticket`
--

CREATE TABLE `ticket` (
  `id_num` varchar(255) NOT NULL,
  `ticket_price` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `ticket`
--

INSERT INTO `ticket` (`id_num`, `ticket_price`) VALUES
('2402', 12345),
('3543', 3000);

-- --------------------------------------------------------

--
-- Table structure for table `Working`
--

CREATE TABLE `Working` (
  `name` varchar(255) NOT NULL,
  `username` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `Working`
--

INSERT INTO `Working` (`name`, `username`) VALUES
('Jet Blue', '111'),
('Jet Blue', '112'),
('Jet Blue', 'Andrew'),
('Jet Blue', 'Helen'),
('Jet Blue', 'Sarah'),
('Jet Blue', 'staff');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Airline`
--
ALTER TABLE `Airline`
  ADD PRIMARY KEY (`name`);

--
-- Indexes for table `Airline_Staff`
--
ALTER TABLE `Airline_Staff`
  ADD PRIMARY KEY (`username`),
  ADD KEY `Airline` (`Airline_name`);

--
-- Indexes for table `AirPlane`
--
ALTER TABLE `AirPlane`
  ADD PRIMARY KEY (`name`,`id_num`);

--
-- Indexes for table `Airport`
--
ALTER TABLE `Airport`
  ADD PRIMARY KEY (`air_code`);

--
-- Indexes for table `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`email`);

--
-- Indexes for table `customer_phone_number`
--
ALTER TABLE `customer_phone_number`
  ADD PRIMARY KEY (`email`,`phone_num`);

--
-- Indexes for table `cus_comment`
--
ALTER TABLE `cus_comment`
  ADD PRIMARY KEY (`id_num_ticket`,`email`),
  ADD KEY `email` (`email`);

--
-- Indexes for table `Flight`
--
ALTER TABLE `Flight`
  ADD PRIMARY KEY (`name`,`id_num`,`dept_date`,`dept_time`,`flight_num`),
  ADD KEY `arri_airport` (`arri_airport`),
  ADD KEY `dept_airport` (`dept_airport`);

--
-- Indexes for table `Inside`
--
ALTER TABLE `Inside`
  ADD PRIMARY KEY (`air_code`,`name`),
  ADD KEY `name` (`name`);

--
-- Indexes for table `maintainance`
--
ALTER TABLE `maintainance`
  ADD PRIMARY KEY (`name`,`id_num`,`start_date`,`start_time`,`end_date`,`end_time`);

--
-- Indexes for table `of`
--
ALTER TABLE `of`
  ADD PRIMARY KEY (`name`,`id_num_ap`,`dept_date`,`dept_time`,`flight_num`,`id_num_ticket`),
  ADD KEY `id_num_ticket` (`id_num_ticket`);

--
-- Indexes for table `purchase`
--
ALTER TABLE `purchase`
  ADD PRIMARY KEY (`id_num`,`email`),
  ADD KEY `email` (`email`);

--
-- Indexes for table `staff_email`
--
ALTER TABLE `staff_email`
  ADD PRIMARY KEY (`username`,`email_address`);

--
-- Indexes for table `staff_phone_num`
--
ALTER TABLE `staff_phone_num`
  ADD PRIMARY KEY (`username`,`phone_num`);

--
-- Indexes for table `ticket`
--
ALTER TABLE `ticket`
  ADD PRIMARY KEY (`id_num`);

--
-- Indexes for table `Working`
--
ALTER TABLE `Working`
  ADD PRIMARY KEY (`name`,`username`),
  ADD KEY `username` (`username`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `Airline_Staff`
--
ALTER TABLE `Airline_Staff`
  ADD CONSTRAINT `airline_staff_ibfk_1` FOREIGN KEY (`Airline_name`) REFERENCES `Airline` (`name`);

--
-- Constraints for table `AirPlane`
--
ALTER TABLE `AirPlane`
  ADD CONSTRAINT `airplane_ibfk_1` FOREIGN KEY (`name`) REFERENCES `Airline` (`name`);

--
-- Constraints for table `customer_phone_number`
--
ALTER TABLE `customer_phone_number`
  ADD CONSTRAINT `customer_phone_number_ibfk_1` FOREIGN KEY (`email`) REFERENCES `customer` (`email`);

--
-- Constraints for table `cus_comment`
--
ALTER TABLE `cus_comment`
  ADD CONSTRAINT `cus_comment_ibfk_1` FOREIGN KEY (`email`) REFERENCES `customer` (`email`),
  ADD CONSTRAINT `cus_comment_ibfk_2` FOREIGN KEY (`id_num_ticket`) REFERENCES `ticket` (`id_num`);

--
-- Constraints for table `Flight`
--
ALTER TABLE `Flight`
  ADD CONSTRAINT `flight_ibfk_1` FOREIGN KEY (`name`,`id_num`) REFERENCES `AirPlane` (`name`, `id_num`),
  ADD CONSTRAINT `flight_ibfk_2` FOREIGN KEY (`arri_airport`) REFERENCES `Airport` (`air_code`),
  ADD CONSTRAINT `flight_ibfk_3` FOREIGN KEY (`dept_airport`) REFERENCES `Airport` (`air_code`);

--
-- Constraints for table `Inside`
--
ALTER TABLE `Inside`
  ADD CONSTRAINT `inside_ibfk_1` FOREIGN KEY (`air_code`) REFERENCES `Airport` (`air_code`),
  ADD CONSTRAINT `inside_ibfk_2` FOREIGN KEY (`name`) REFERENCES `Airline` (`name`);

--
-- Constraints for table `maintainance`
--
ALTER TABLE `maintainance`
  ADD CONSTRAINT `maintainance_ibfk_1` FOREIGN KEY (`name`,`id_num`) REFERENCES `AirPlane` (`name`, `id_num`);

--
-- Constraints for table `of`
--
ALTER TABLE `of`
  ADD CONSTRAINT `of_ibfk_1` FOREIGN KEY (`name`,`id_num_ap`,`dept_date`,`dept_time`,`flight_num`) REFERENCES `Flight` (`name`, `id_num`, `dept_date`, `dept_time`, `flight_num`),
  ADD CONSTRAINT `of_ibfk_2` FOREIGN KEY (`id_num_ticket`) REFERENCES `ticket` (`id_num`);

--
-- Constraints for table `purchase`
--
ALTER TABLE `purchase`
  ADD CONSTRAINT `purchase_ibfk_1` FOREIGN KEY (`id_num`) REFERENCES `ticket` (`id_num`),
  ADD CONSTRAINT `purchase_ibfk_2` FOREIGN KEY (`email`) REFERENCES `customer` (`email`);

--
-- Constraints for table `staff_email`
--
ALTER TABLE `staff_email`
  ADD CONSTRAINT `staff_email_ibfk_1` FOREIGN KEY (`username`) REFERENCES `Airline_Staff` (`username`);

--
-- Constraints for table `staff_phone_num`
--
ALTER TABLE `staff_phone_num`
  ADD CONSTRAINT `staff_phone_num_ibfk_1` FOREIGN KEY (`username`) REFERENCES `Airline_Staff` (`username`);

--
-- Constraints for table `Working`
--
ALTER TABLE `Working`
  ADD CONSTRAINT `working_ibfk_1` FOREIGN KEY (`name`) REFERENCES `Airline` (`name`),
  ADD CONSTRAINT `working_ibfk_2` FOREIGN KEY (`username`) REFERENCES `Airline_Staff` (`username`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
