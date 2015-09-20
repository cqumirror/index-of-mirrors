-- MySQL dump 10.13  Distrib 5.5.44, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: mirrors
-- ------------------------------------------------------
-- Server version	5.5.44-0ubuntu0.14.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `mirrors`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `mirrors` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `mirrors`;

--
-- Table structure for table `mirrors_downloads`
--

DROP TABLE IF EXISTS mirrors_resources;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mirrors_downloads` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(40) NOT NULL,
  `fullname` varchar(60) NOT NULL,
  `host` varchar(60) NOT NULL,
  `dir` varchar(40) DEFAULT NULL,
  `path` varchar(100) DEFAULT NULL,
  `type` varchar(10) NOT NULL,
  `version` varchar(40) NOT NULL,
  `comment` varchar(10) DEFAULT NULL,
  `protocol` varchar(10) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `name_index` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mirrors_downloads`
--

LOCK TABLES mirrors_resources WRITE;
/*!40000 ALTER TABLE mirrors_resources DISABLE KEYS */;
INSERT INTO mirrors_resources VALUES (1,'ubuntu-desktop','Ubuntu Desktop','mirrors.cqu.edu.cn','/ubuntu-releases','/ubuntu-releases/14.04.3/ubuntu-14.04.3-desktop-amd64.iso','os','14.04.3-amd64',NULL,'https'),(2,'ubuntu-desktop','Ubuntu Desktop','mirrors.cqu.edu.cn','/ubuntu-releases','/ubuntu-releases/14.04.3/ubuntu-14.04.3-desktop-i386.iso','os','14.04.3-i386',NULL,'https'),(3,'ubuntu-server','Ubuntu Server','mirrors.cqu.edu.cn','/ubuntu-releases','/ubuntu-releases/14.04.3/ubuntu-14.04.3-server-amd64.iso','os','14.04.3-amd64',NULL,'https'),(4,'ubuntu-server','Ubuntu Server','mirrors.cqu.edu.cn','/ubuntu-releases','/ubuntu-releases/14.04.3/ubuntu-14.04.3-server-i386.iso','os','14.04.3-i386',NULL,'https'),(5,'ubuntu-desktop','Ubuntu Desktop','mirrors.cqu.edu.cn','/ubuntu-releases','/ubuntu-releases/14.10/ubuntu-14.10-desktop-amd64.iso','os','14.10-amd64',NULL,'https'),(6,'ubuntu-desktop','Ubuntu Desktop','mirrors.cqu.edu.cn','/ubuntu-releases','/ubuntu-releases/14.10/ubuntu-14.10-desktop-i386.iso','os','14.10-i386',NULL,'https'),(7,'ubuntu-desktop','Ubuntu Desktop','mirrors.cqu.edu.cn','/ubuntu-releases','/ubuntu-releases/15.04/ubuntu-15.04-desktop-amd64.iso','os','15.04-amd64',NULL,'https'),(8,'ubuntu-desktop','Ubuntu Desktop','mirrors.cqu.edu.cn','/ubuntu-releases','/ubuntu-releases/15.04/ubuntu-15.04-desktop-i386.iso','os','15.04-i386',NULL,'https'),(9,'centos','CentOS','b.mirrors.lanunion.org','/CentOS','/CentOS/7.1.1503/isos/x86_64/CentOS-7-x86_64-Minimal-1503-01.iso','os','7.1.1503-x86_64-Minimal',NULL,'https');
/*!40000 ALTER TABLE mirrors_resources ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mirrors_info`
--

DROP TABLE IF EXISTS `mirrors_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mirrors_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(40) NOT NULL,
  `fullname` varchar(60) NOT NULL,
  `host` varchar(60) NOT NULL,
  `path` varchar(100) NOT NULL,
  `help` varchar(100) DEFAULT NULL,
  `comment` varchar(10) DEFAULT NULL,
  `protocol` varchar(10) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name_index` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mirrors_info`
--

LOCK TABLES `mirrors_info` WRITE;
/*!40000 ALTER TABLE `mirrors_info` DISABLE KEYS */;
INSERT INTO `mirrors_info` VALUES (1,'archlinux','Arch Linux','b.mirrors.lanunion.org','/archlinux','/wiki/index.php?title=ArchLinux',NULL,'https'),(2,'archlinux-cn','Arch Linux CN','b.mirrors.lanunion.org','/archlinux-cn','/wiki/index.php?title=ArchLinux-cn',NULL,'https'),(3,'archlinux-arm','Arch Linux ARM','b.mirrors.lanunion.org','/archlinux-arm','/wiki/index.php?title=ArchLinux-arm',NULL,'https'),(4,'centos','CentOS','b.mirrors.lanunion.org','/centos','/wiki/index.php?title=CentOS',NULL,'https'),(5,'debian','Debian','b.mirrors.lanunion.org','/debian',NULL,NULL,'https'),(6,'debian-backports','Debian backports','b.mirrors.lanunion.org','/debian-backports',NULL,NULL,'https'),(7,'debian-cd','Debian CD','b.mirrors.lanunion.org','/debian-cd',NULL,NULL,'https'),(8,'debian-multimedia','Debian multimedia','b.mirrors.lanunion.org','/debian-multimedia',NULL,NULL,'https'),(9,'debian-security','Debian security','b.mirrors.lanunion.org','/debian-security',NULL,NULL,'https'),(10,'deepin','Deepin','mirrors.cqu.edu.cn','/deepin','/wiki/index.php?title=Deepin',NULL,'https'),(11,'deepin-cd','Deepin CD','mirrors.cqu.edu.cn','/deepin-cd',NULL,NULL,'https'),(12,'epel','EPEL','b.mirrors.lanunion.org','/epel',NULL,'new','https'),(13,'ezgo','Ezgo','mirrors.cqu.edu.cn','/ezgo',NULL,NULL,'https'),(14,'linuxmint','Linux Mint','b.mirrors.cqu.edu.cn','/linuxmint','/wiki/index.php?title=Linuxmint',NULL,'https'),(15,'opensuse','OpenSUSE','c.mirrors.lanunion.org','/opensuse',NULL,NULL,'https'),(16,'pypi','PyPI','pypi.mirrors.lanunion.org','/pypi','/wiki/index.php?title=PyPI','new','https'),(17,'raspbian','Raspbian','mirrors.cqu.edu.cn','/raspbian','/wiki/index.php?title=Raspbian',NULL,'https'),(18,'startos','StartOS','mirrors.cqu.edu.cn','/startos','/wiki/index.php?title=StartOS',NULL,'https'),(19,'ubuntu','Ubuntu','mirrors.cqu.edu.cn','/ubuntu','/wiki/index.php?title=Ubuntu',NULL,'https'),(20,'ubuntu-releases','Ubuntu releases','mirrors.cqu.edu.cn','/ubuntu-releases',NULL,NULL,'https');
/*!40000 ALTER TABLE `mirrors_info` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-09-19  8:33:02
