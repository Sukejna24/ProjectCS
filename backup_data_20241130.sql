-- MariaDB dump 10.19  Distrib 10.4.32-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: data
-- ------------------------------------------------------
-- Server version	10.4.32-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `data`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `data` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci */;

USE `data`;

--
-- Table structure for table `artst`
--

DROP TABLE IF EXISTS `artst`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `artst` (
  `artist_uri` varchar(64) NOT NULL,
  `name` varchar(255) NOT NULL,
  `popularity` tinyint(3) unsigned NOT NULL,
  `followers` bigint(20) unsigned NOT NULL,
  `artist_type` varchar(64) NOT NULL,
  PRIMARY KEY (`artist_uri`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci COMMENT='Artist info with foreign key link to genres in gnres';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `artst`
--

LOCK TABLES `artst` WRITE;
/*!40000 ALTER TABLE `artst` DISABLE KEYS */;
INSERT INTO `artst` VALUES ('spotify:artist:00FQb4jTyendYWaN8pK0wa','Lana Del Rey',92,42047490,'artist'),('spotify:artist:0FEJqmeLRzsXj8hgcZaAyB','Indila',72,2139399,'artist'),('spotify:artist:1P6U1dCeHxPui5pIrGmndZ','Air',65,1024158,'artist'),('spotify:artist:1QAJqy2dA3ihHBFIHRphZj','Cigarettes After Sex',87,13593524,'artist'),('spotify:artist:1r43wW70tnGUauQYvY5w48','BENNETT',71,236379,'artist'),('spotify:artist:22HVxZPA6UhBp8wahxDA6I','France Gall',60,435532,'artist'),('spotify:artist:2AcUPzkVWo81vumdzeLLRN','Rhye',62,674070,'artist'),('spotify:artist:2gTl60Ao3u7bljVnAqxPh8','Tanita Tikaram',51,161829,'artist'),('spotify:artist:3gZ4Lrq3hdTnUv43ZMj0Yi','Peter Noone',13,1588,'artist'),('spotify:artist:3KyDVCWIj6zxYT2QU3iRcy','Genderbüebu',41,10102,'artist'),('spotify:artist:3l0CmX0FuQjFxr8SK7Vqag','Clairo',82,5498319,'artist'),('spotify:artist:3oDbviiivRWhXwIE8hxkVV','The Beach Boys',74,4715437,'artist'),('spotify:artist:56ZTgzPBDge0OvCGgMO3OY','Beach House',74,2395670,'artist'),('spotify:artist:5BKsn7SCN2XmbF7apdCpRS','Goldfrapp',53,572816,'artist'),('spotify:artist:5skauLarl8sqqUFypECtP4','Michel Berger',55,427893,'artist'),('spotify:artist:64LCTpIu9Iji2EPaxxPpxF','Joe Dassin',61,619111,'artist'),('spotify:artist:6ZRBTMONSlddCATaF9Qlq5','The Gypsy Queens',42,19343,'artist'),('spotify:artist:7d64ZVOXg02y73HB5UMqkb','Okay Kaya',51,115427,'artist'),('spotify:artist:7Jotu5LupekFt00kZZZ7C6','Hayley Westenra',43,92149,'artist'),('spotify:artist:7nXyULtoL8k7wP9l6kg8Ef','Madeleine Peyroux',60,452962,'artist'),('spotify:artist:7tr9pbgNEKtG0GQTKe08Tz','Mk.gee',67,261445,'artist');
/*!40000 ALTER TABLE `artst` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gnrs`
--

DROP TABLE IF EXISTS `gnrs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gnrs` (
  `artist_uri` varchar(64) NOT NULL,
  `genres_name` varchar(255) NOT NULL,
  PRIMARY KEY (`artist_uri`,`genres_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci COMMENT='Foregin key to artst';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gnrs`
--

LOCK TABLES `gnrs` WRITE;
/*!40000 ALTER TABLE `gnrs` DISABLE KEYS */;
INSERT INTO `gnrs` VALUES ('spotify:artist:00FQb4jTyendYWaN8pK0wa','art pop'),('spotify:artist:00FQb4jTyendYWaN8pK0wa','pop'),('spotify:artist:0FEJqmeLRzsXj8hgcZaAyB','french pop'),('spotify:artist:1P6U1dCeHxPui5pIrGmndZ','ambient pop'),('spotify:artist:1P6U1dCeHxPui5pIrGmndZ','downtempo'),('spotify:artist:1P6U1dCeHxPui5pIrGmndZ','electronica'),('spotify:artist:1P6U1dCeHxPui5pIrGmndZ','indietronica'),('spotify:artist:1P6U1dCeHxPui5pIrGmndZ','trip hop'),('spotify:artist:1QAJqy2dA3ihHBFIHRphZj','ambient pop'),('spotify:artist:1QAJqy2dA3ihHBFIHRphZj','dream pop'),('spotify:artist:1QAJqy2dA3ihHBFIHRphZj','el paso indie'),('spotify:artist:1QAJqy2dA3ihHBFIHRphZj','shoegaze'),('spotify:artist:1r43wW70tnGUauQYvY5w48','hypertechno'),('spotify:artist:22HVxZPA6UhBp8wahxDA6I','chanson'),('spotify:artist:22HVxZPA6UhBp8wahxDA6I','ye ye'),('spotify:artist:2AcUPzkVWo81vumdzeLLRN','art pop'),('spotify:artist:2AcUPzkVWo81vumdzeLLRN','downtempo'),('spotify:artist:2AcUPzkVWo81vumdzeLLRN','electronica'),('spotify:artist:2AcUPzkVWo81vumdzeLLRN','indie soul'),('spotify:artist:2AcUPzkVWo81vumdzeLLRN','indietronica'),('spotify:artist:2AcUPzkVWo81vumdzeLLRN','shimmer pop'),('spotify:artist:2gTl60Ao3u7bljVnAqxPh8','new wave pop'),('spotify:artist:3KyDVCWIj6zxYT2QU3iRcy','schwyzerorgeli'),('spotify:artist:3l0CmX0FuQjFxr8SK7Vqag','bedroom pop'),('spotify:artist:3l0CmX0FuQjFxr8SK7Vqag','indie pop'),('spotify:artist:3l0CmX0FuQjFxr8SK7Vqag','pov: indie'),('spotify:artist:56ZTgzPBDge0OvCGgMO3OY','art pop'),('spotify:artist:56ZTgzPBDge0OvCGgMO3OY','baltimore indie'),('spotify:artist:56ZTgzPBDge0OvCGgMO3OY','dream pop'),('spotify:artist:56ZTgzPBDge0OvCGgMO3OY','dreamo'),('spotify:artist:56ZTgzPBDge0OvCGgMO3OY','indie rock'),('spotify:artist:56ZTgzPBDge0OvCGgMO3OY','indietronica'),('spotify:artist:56ZTgzPBDge0OvCGgMO3OY','modern dream pop'),('spotify:artist:56ZTgzPBDge0OvCGgMO3OY','pov: indie'),('spotify:artist:5BKsn7SCN2XmbF7apdCpRS','alternative dance'),('spotify:artist:5BKsn7SCN2XmbF7apdCpRS','art pop'),('spotify:artist:5BKsn7SCN2XmbF7apdCpRS','electronica'),('spotify:artist:5BKsn7SCN2XmbF7apdCpRS','indietronica'),('spotify:artist:5BKsn7SCN2XmbF7apdCpRS','neo-synthpop'),('spotify:artist:5BKsn7SCN2XmbF7apdCpRS','trip hop'),('spotify:artist:5skauLarl8sqqUFypECtP4','chanson'),('spotify:artist:64LCTpIu9Iji2EPaxxPpxF','chanson'),('spotify:artist:64LCTpIu9Iji2EPaxxPpxF','chanson paillarde'),('spotify:artist:6ZRBTMONSlddCATaF9Qlq5','nice indie'),('spotify:artist:7d64ZVOXg02y73HB5UMqkb','art pop'),('spotify:artist:7Jotu5LupekFt00kZZZ7C6','bow pop'),('spotify:artist:7Jotu5LupekFt00kZZZ7C6','operatic pop'),('spotify:artist:7nXyULtoL8k7wP9l6kg8Ef','contemporary vocal jazz'),('spotify:artist:7nXyULtoL8k7wP9l6kg8Ef','jazz pop'),('spotify:artist:7nXyULtoL8k7wP9l6kg8Ef','vocal jazz'),('spotify:artist:7tr9pbgNEKtG0GQTKe08Tz','experimental r&b');
/*!40000 ALTER TABLE `gnrs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `plylst`
--

DROP TABLE IF EXISTS `plylst`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `plylst` (
  `playlist_uri` varchar(64) NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` varchar(1024) NOT NULL,
  `owner_uri` varchar(64) NOT NULL,
  `owner_display_name` varchar(255) NOT NULL,
  `collaborative` bit(1) NOT NULL,
  `public` bit(1) NOT NULL,
  `tracks_total` smallint(5) unsigned NOT NULL,
  `type` varchar(64) NOT NULL,
  PRIMARY KEY (`playlist_uri`),
  KEY `owner_uri` (`owner_uri`),
  CONSTRAINT `FK_User` FOREIGN KEY (`owner_uri`) REFERENCES `usr` (`user_uri`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci COMMENT='Playlist';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `plylst`
--

LOCK TABLES `plylst` WRITE;
/*!40000 ALTER TABLE `plylst` DISABLE KEYS */;
INSERT INTO `plylst` VALUES ('spotify:playlist:1GUklNPURDhcQWq6Zsug5R','Meine Playlist Nr. 1','','spotify:user:8hfijwcmt6an0jxt97h8ofe0f','spotify-user','\0','',5,'playlist'),('spotify:playlist:3WJrzYtcBaWj1ufUoOJqeh','Playlist Nr. 2','','spotify:user:8hfijwcmt6an0jxt97h8ofe0f','spotify-user','\0','',2,'playlist');
/*!40000 ALTER TABLE `plylst` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `trck`
--

DROP TABLE IF EXISTS `trck`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `trck` (
  `track_uri` varchar(64) NOT NULL,
  `playlist_uri` varchar(64) NOT NULL,
  `track` bit(1) NOT NULL,
  `album_name` varchar(256) NOT NULL,
  `album_type` varchar(64) NOT NULL,
  `total_tracks` mediumint(8) unsigned NOT NULL,
  `disc_number` mediumint(8) unsigned NOT NULL,
  `track_number` mediumint(8) unsigned NOT NULL,
  `duration_ms` int(10) unsigned NOT NULL,
  `release_date` datetime NOT NULL,
  `release_date_prescision` varchar(32) NOT NULL,
  `popularity` tinyint(3) unsigned NOT NULL,
  `item_added_at` datetime NOT NULL,
  `item_added_by_uri` varchar(64) NOT NULL,
  `track_id` varchar(64) NOT NULL,
  `acousticness` float NOT NULL,
  `danceability` float NOT NULL,
  `energy` float NOT NULL,
  `instrumentalness` float NOT NULL,
  `pitchKey` tinyint(4) NOT NULL,
  `liveness` float NOT NULL,
  `loudness` float NOT NULL,
  `mode` bit(1) NOT NULL,
  `speechiness` float NOT NULL,
  `tempo` float NOT NULL,
  `valence` float NOT NULL,
  PRIMARY KEY (`track_uri`),
  KEY `playlist_uri` (`playlist_uri`),
  CONSTRAINT `FK_Playlist` FOREIGN KEY (`playlist_uri`) REFERENCES `plylst` (`playlist_uri`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci COMMENT='track and track audio features of a playlist uri';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `trck`
--

LOCK TABLES `trck` WRITE;
/*!40000 ALTER TABLE `trck` DISABLE KEYS */;
INSERT INTO `trck` VALUES ('spotify:track:0i3TaYmc4gLpM2AvxbyZEl','spotify:playlist:1GUklNPURDhcQWq6Zsug5R','','Freundschaft','album',20,1,3,237040,'2021-09-24 00:00:00','day',27,'2024-10-29 20:08:52','spotify:user:8hfijwcmt6an0jxt97h8ofe0f','0i3TaYmc4gLpM2AvxbyZEl',0.00242,0.585,0.842,0.00686,9,0.0866,-5.883,'\0',0.0556,118.211,0.428),('spotify:track:0wz1LjDb9ZNEYwOmDJ3Q4b','spotify:playlist:1GUklNPURDhcQWq6Zsug5R','','Surfin\' USA (Remastered)','album',12,1,1,237040,'1963-03-25 00:00:00','day',70,'2024-10-29 20:08:18','spotify:user:8hfijwcmt6an0jxt97h8ofe0f','0wz1LjDb9ZNEYwOmDJ3Q4b',0.00242,0.585,0.842,0.00686,9,0.0866,-5.883,'\0',0.0556,118.211,0.428),('spotify:track:1C0GsKpv7rqKEmQaUOMDIE','spotify:playlist:1GUklNPURDhcQWq6Zsug5R','','Freundschaft','album',20,1,6,237040,'2021-09-24 00:00:00','day',36,'2024-10-29 20:08:53','spotify:user:8hfijwcmt6an0jxt97h8ofe0f','1C0GsKpv7rqKEmQaUOMDIE',0.00242,0.585,0.842,0.00686,9,0.0866,-5.883,'\0',0.0556,118.211,0.428),('spotify:track:1fX0h6SaZBXwmr4haRvirQ','spotify:playlist:3WJrzYtcBaWj1ufUoOJqeh','','Night Owls','album',12,1,1,237040,'1990-04-10 00:00:00','day',56,'2024-11-30 21:15:10','spotify:user:8hfijwcmt6an0jxt97h8ofe0f','1fX0h6SaZBXwmr4haRvirQ',0.00242,0.585,0.842,0.00686,9,0.0866,-5.883,'\0',0.0556,118.211,0.428),('spotify:track:3gvUS6JaXzbXNihHQlRWBW','spotify:playlist:1GUklNPURDhcQWq6Zsug5R','','Les Champs-Elysées','compilation',12,1,4,237040,'1969-08-20 00:00:00','day',52,'2024-10-29 20:09:07','spotify:user:8hfijwcmt6an0jxt97h8ofe0f','3gvUS6JaXzbXNihHQlRWBW',0.00242,0.585,0.842,0.00686,9,0.0866,-5.883,'\0',0.0556,118.211,0.428),('spotify:track:5fIZ683j2xPeLAXfHeWKEG','spotify:playlist:1GUklNPURDhcQWq6Zsug5R','','Dernière danse (Techno Mix)','single',1,1,1,237040,'2024-01-26 00:00:00','day',72,'2024-10-29 20:09:32','spotify:user:8hfijwcmt6an0jxt97h8ofe0f','5fIZ683j2xPeLAXfHeWKEG',0.00242,0.585,0.842,0.00686,9,0.0866,-5.883,'\0',0.0556,118.211,0.428),('spotify:track:5yttPxcfowfL4TUYKDqdJe','spotify:playlist:3WJrzYtcBaWj1ufUoOJqeh','','Collected','album',13,1,2,237040,'1984-01-01 00:00:00','day',26,'2024-11-30 21:15:22','spotify:user:8hfijwcmt6an0jxt97h8ofe0f','5yttPxcfowfL4TUYKDqdJe',0.00242,0.585,0.842,0.00686,9,0.0866,-5.883,'\0',0.0556,118.211,0.428);
/*!40000 ALTER TABLE `trck` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usr`
--

DROP TABLE IF EXISTS `usr`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usr` (
  `user_uri` varchar(64) NOT NULL COMMENT 'Unique ID from Spotify',
  `email` varchar(255) NOT NULL,
  `display_name` varchar(255) NOT NULL,
  `followers` int(11) NOT NULL,
  `country` char(2) NOT NULL,
  PRIMARY KEY (`user_uri`),
  UNIQUE KEY `userUri` (`user_uri`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci COMMENT='Spotify User';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usr`
--

LOCK TABLES `usr` WRITE;
/*!40000 ALTER TABLE `usr` DISABLE KEYS */;
INSERT INTO `usr` VALUES ('spotify:user:8hfijwcmt6an0jxt97h8ofe0f','','spotify-user',0,'');
/*!40000 ALTER TABLE `usr` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-01  0:40:57
