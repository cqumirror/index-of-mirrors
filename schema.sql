-- MySQL dump 10.13  Distrib 5.5.46, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: mirrors
-- ------------------------------------------------------
-- Server version	5.5.46-0ubuntu0.14.04.2

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
  `protocol` varchar(10) NOT NULL,
  `help` varchar(100) DEFAULT NULL,
  `comment` varchar(10) DEFAULT NULL,
  `status` int(11) NOT NULL,
  `created` datetime NOT NULL,
  `last_updated` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mirrors_info`
--

LOCK TABLES `mirrors_info` WRITE;
/*!40000 ALTER TABLE `mirrors_info` DISABLE KEYS */;
INSERT INTO `mirrors_info` VALUES (1,'arch-linux','Arch Linux','b.mirrors.lanunion.org','/archlinux','https','https://mirrors.cqu.edu.cn/wiki/index.php?title=ArchLinux',NULL,0,'2015-11-04 18:11:35','2015-11-04 18:11:35'),(2,'arch-linux-arm','Arch Linux ARM','b.mirrors.lanunion.org','/archlinux-arm','https','https://mirrors.cqu.edu.cn/wiki/index.php?title=ArchLinux-arm',NULL,0,'2015-11-04 18:11:35','2015-11-04 18:11:35'),(3,'arch-linux-cn','Arch Linux CN','b.mirrors.lanunion.org','/archlinux-cn','https','https://mirrors.cqu.edu.cn/wiki/index.php?title=ArchLinux-cn',NULL,0,'2015-11-04 18:11:35','2015-11-04 18:11:35'),(4,'centos','CentOS','b.mirrors.lanunion.org','/centos','https','https://mirrors.cqu.edu.cn/wiki/index.php?title=CentOS',NULL,0,'2015-11-04 18:11:35','2015-11-04 18:11:35'),(5,'cpan','CPAN','b.mirrors.lanunion.org','/cpan','https',NULL,NULL,0,'2015-11-04 18:11:35','2015-11-04 18:11:35'),(6,'debian','Debian','b.mirrors.lanunion.org','/debian','https',NULL,NULL,0,'2015-11-04 18:11:35','2015-11-04 18:11:35'),(7,'debian-backports','Debian backports','b.mirrors.lanunion.org','/debian-backports','https',NULL,NULL,0,'2015-11-04 18:11:35','2015-11-04 18:11:35'),(8,'debian-cd','Debian CD','b.mirrors.lanunion.org','/debian-cd','https',NULL,NULL,0,'2015-11-04 18:11:35','2015-11-04 18:11:35'),(9,'debian-multimedia','Debian multimedia','b.mirrors.lanunion.org','/debian-multimedia','https',NULL,NULL,0,'2015-11-04 18:11:35','2015-11-04 18:11:35'),(10,'debian-security','Debian security','b.mirrors.lanunion.org','/debian-security','https',NULL,NULL,0,'2015-11-04 18:11:35','2015-11-04 18:11:35'),(11,'deepin','Deepin','mirrors.cqu.edu.cn','/deepin','https','https://mirrors.cqu.edu.cn/wiki/index.php?title=Deepin',NULL,0,'2015-11-04 18:11:35','2015-11-04 18:11:35'),(12,'deepin-cd','Deepin CD','mirrors.cqu.edu.cn','/deepin-cd','https',NULL,NULL,0,'2015-11-04 18:11:35','2015-11-04 18:11:35'),(13,'epel','EPEL','b.mirrors.lanunion.org','/epel','https',NULL,NULL,0,'2015-11-04 18:11:35','2015-11-04 18:11:35'),(14,'ezgo','Ezgo','mirrors.cqu.edu.cn','/ezgo','https',NULL,NULL,0,'2015-11-04 18:11:35','2015-11-04 18:11:35'),(15,'kali','Kali','b.mirrors.lanunion.org','/kali','https',NULL,'new',0,'2015-11-04 18:11:35','2015-11-04 18:11:35'),(16,'kali-security','Kali security','b.mirrors.lanunion.org','/kali-security','https',NULL,'new',0,'2015-11-04 18:11:35','2015-11-04 18:11:35'),(17,'linux-mint','Linux Mint','b.mirrors.lanunion.org','/linuxmint','https','https://mirrors.cqu.edu.cn/wiki/index.php?title=Linuxmint',NULL,0,'2015-11-04 18:11:35','2015-11-04 18:11:35'),(18,'mariadb','Mariadb','c.mirrors.lanunion.org','/mariadb','https',NULL,NULL,0,'2015-11-04 18:11:35','2015-11-04 18:11:35'),(19,'opensuse','OpenSUSE','c.mirrors.lanunion.org','/opensuse','https',NULL,NULL,0,'2015-11-04 18:11:35','2015-11-04 18:11:35'),(20,'pypi','PyPI','pypi.mirrors.lanunion.org','/','https','https://mirrors.cqu.edu.cn/wiki/index.php?title=PyPI',NULL,0,'2015-11-04 18:11:35','2015-11-04 18:11:35'),(21,'raspbian','Raspbian','mirrors.cqu.edu.cn','/raspbian','https','https://mirrors.cqu.edu.cn/wiki/index.php?title=Raspbian',NULL,0,'2015-11-04 18:11:35','2015-11-04 18:11:35'),(22,'startos','StartOS','mirrors.cqu.edu.cn','/startos','https','https://mirrors.cqu.edu.cn/wiki/index.php?title=StartOS',NULL,0,'2015-11-04 18:11:35','2015-11-04 18:11:35'),(23,'ubuntu','Ubuntu','mirrors.cqu.edu.cn','/ubuntu','https','https://mirrors.cqu.edu.cn/wiki/index.php?title=Ubuntu',NULL,0,'2015-11-04 18:11:35','2015-11-04 18:11:35'),(24,'ubuntu-kylin-releases','Ubuntu Kylin releases','mirrors.cqu.edu.cn','/ubuntu-kylin-releases','https',NULL,NULL,0,'2015-11-04 18:11:35','2015-11-04 18:11:35'),(25,'ubuntu-releases','Ubuntu releases','mirrors.cqu.edu.cn','/ubuntu-releases','https',NULL,NULL,0,'2015-11-04 18:11:35','2015-11-04 18:11:35');
/*!40000 ALTER TABLE `mirrors_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mirrors_notices`
--

DROP TABLE IF EXISTS `mirrors_notices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mirrors_notices` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content` text NOT NULL,
  `level` varchar(20) NOT NULL,
  `status` int(11) NOT NULL,
  `created` datetime NOT NULL,
  `last_updated` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mirrors_notices`
--

LOCK TABLES `mirrors_notices` WRITE;
/*!40000 ALTER TABLE `mirrors_notices` DISABLE KEYS */;
INSERT INTO `mirrors_notices` VALUES (1,'There is a big progress.','normal',0,'2015-11-04 19:17:31','2015-11-04 19:17:35');
/*!40000 ALTER TABLE `mirrors_notices` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mirrors_resources`
--

DROP TABLE IF EXISTS `mirrors_resources`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mirrors_resources` (
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
  `status` int(11) NOT NULL,
  `created` datetime NOT NULL,
  `last_updated` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mirrors_resources`
--

LOCK TABLES `mirrors_resources` WRITE;
/*!40000 ALTER TABLE `mirrors_resources` DISABLE KEYS */;
INSERT INTO `mirrors_resources` VALUES (1,'ubuntu-desktop','Ubuntu Desktop','mirrors.cqu.edu.cn','/ubuntu-releases','/ubuntu-releases/14.04.3/ubuntu-14.04.3-desktop-amd64.iso','os','14.04.3-amd64',NULL,'https',0,'2015-11-04 18:11:35','2015-11-04 18:11:35'),(2,'ubuntu-desktop','Ubuntu Desktop','mirrors.cqu.edu.cn','/ubuntu-releases','/ubuntu-releases/14.04.3/ubuntu-14.04.3-desktop-i386.iso','os','14.04.3-i386',NULL,'https',0,'2015-11-04 18:11:35','2015-11-04 18:11:35'),(3,'ubuntu-server','Ubuntu Server','mirrors.cqu.edu.cn','/ubuntu-releases','/ubuntu-releases/14.04.3/ubuntu-14.04.3-server-amd64.iso','os','14.04.3-amd64',NULL,'https',0,'2015-11-04 18:11:35','2015-11-04 18:11:35'),(4,'ubuntu-server','Ubuntu Server','mirrors.cqu.edu.cn','/ubuntu-releases','/ubuntu-releases/14.04.3/ubuntu-14.04.3-server-i386.iso','os','14.04.3-i386',NULL,'https',0,'2015-11-04 18:11:35','2015-11-04 18:11:35'),(5,'ubuntu-desktop','Ubuntu Desktop','mirrors.cqu.edu.cn','/ubuntu-releases','/ubuntu-releases/14.10/ubuntu-14.10-desktop-amd64.iso','os','14.10-amd64',NULL,'https',0,'2015-11-04 18:11:35','2015-11-04 18:11:35'),(6,'ubuntu-desktop','Ubuntu Desktop','mirrors.cqu.edu.cn','/ubuntu-releases','/ubuntu-releases/14.10/ubuntu-14.10-desktop-i386.iso','os','14.10-i386',NULL,'https',0,'2015-11-04 18:11:35','2015-11-04 18:11:35'),(7,'ubuntu-desktop','Ubuntu Desktop','mirrors.cqu.edu.cn','/ubuntu-releases','/ubuntu-releases/15.04/ubuntu-15.04-desktop-amd64.iso','os','15.04-amd64',NULL,'https',0,'2015-11-04 18:11:35','2015-11-04 18:11:35'),(8,'ubuntu-desktop','Ubuntu Desktop','mirrors.cqu.edu.cn','/ubuntu-releases','/ubuntu-releases/15.04/ubuntu-15.04-desktop-i386.iso','os','15.04-i386',NULL,'https',0,'2015-11-04 18:11:35','2015-11-04 18:11:35'),(9,'centos','CentOS','b.mirrors.lanunion.org','/CentOS','/CentOS/7.1.1503/isos/x86_64/CentOS-7-x86_64-Minimal-1503-01.iso','os','7.1.1503-x86_64-Minimal',NULL,'https',0,'2015-11-04 18:11:35','2015-11-04 18:11:35');
/*!40000 ALTER TABLE `mirrors_resources` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-11-04  9:25:55
