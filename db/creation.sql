-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 25, 2023 at 05:06 PM
-- Server version: 10.4.20-MariaDB
-- PHP Version: 7.3.29

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";



CREATE TABLE `book` (
  `bookid` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `author` varchar(30) NOT NULL,
  `title` varchar(30) NOT NULL,
  `isbn` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  `category` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  `year` datetime NOT NULL DEFAULT current_timestamp(),
  `language` varchar(30) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE `periodical` (
  `bookid` int(11) NOT NULL,
    FOREIGN KEY (`bookid`) REFERENCES `book`(`bookid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE `audiobook` (
  `bookid` int(11) NOT NULL,
    `audioformat` varchar(30) NOT NULL,
    FOREIGN KEY (`bookid`) REFERENCES `book`(`bookid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;




CREATE TABLE `borrower` (
  `borrowerid` int(11) UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `firstname` varchar(255) DEFAULT NULL,
  `lastname` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `password` varchar(64) NOT NULL,
  `role` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `borrowed` (
  `borrowedid` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `bookid` int(11) NOT NULL,
  `borrowerid` int(11) UNSIGNED NOT NULL,
  `borrowdate` datetime NOT NULL DEFAULT current_timestamp(),
  `duedate` datetime NOT NULL,
  `returndate` datetime NOT NULL,
    FOREIGN KEY (`bookid`) REFERENCES `book`(`bookid`),
    FOREIGN KEY (`borrowerid`) REFERENCES `borrower`(`borrowerid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE `fine` (
  `fineid` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `borrowedid` int(11) NOT NULL,
  `status` varchar(30) NOT NULL,
  `amount` int NOT NULL,
   FOREIGN KEY (`borrowedid`) REFERENCES `borrowed`(`borrowedid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;






COMMIT;
