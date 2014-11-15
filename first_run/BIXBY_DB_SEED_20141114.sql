-- MySQL dump 10.13  Distrib 5.6.21, for osx10.8 (x86_64)
--
-- Host: 127.0.0.1    Database: BIXBY_DB
-- ------------------------------------------------------
-- Server version	5.6.21

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
-- Temporary view structure for view `active_users`
--

DROP TABLE IF EXISTS `active_users`;
/*!50001 DROP VIEW IF EXISTS `active_users`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `active_users` AS SELECT 
 1 AS `UID`,
 1 AS `EXTERNAL_UID`,
 1 AS `EXTERNAL_USERNUMBER`,
 1 AS `FIRST_NAME`,
 1 AS `LAST_NAME`,
 1 AS `MIDDLE_NAME`,
 1 AS `DEPARTMENT_ID`,
 1 AS `GOOGLE_USERNAME`,
 1 AS `DOMAIN_NAME`,
 1 AS `DOMAIN_ID`,
 1 AS `USER_TYPE`,
 1 AS `USER_TYPEID`,
 1 AS `FULL_EMAIL`,
 1 AS `EMAIL_OVERRIDE_ADDRESS`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `departments`
--

DROP TABLE IF EXISTS `departments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `departments` (
  `DEPARTMENTID` int(11) NOT NULL AUTO_INCREMENT,
  `SITEID` int(9) DEFAULT NULL COMMENT 'School Number',
  `DEPARTMENT` varchar(45) NOT NULL,
  `DESCRIPTION` varchar(255) DEFAULT NULL,
  `ABBREVIATION` varchar(45) DEFAULT NULL,
  `UNIQUE_IDENTIFIER` varchar(45) DEFAULT NULL,
  `UNIT` int(3) DEFAULT NULL,
  `UNUSED_USER_TYPEID` int(2) DEFAULT '1',
  `SITECODE` int(11) DEFAULT NULL,
  PRIMARY KEY (`DEPARTMENTID`)
) ENGINE=InnoDB AUTO_INCREMENT=84 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `domains`
--

DROP TABLE IF EXISTS `domains`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `domains` (
  `DOMAIN_ID` int(11) NOT NULL AUTO_INCREMENT,
  `DOMAIN_NAME` varchar(40) NOT NULL,
  `PRIMARY_DOMAIN` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`DOMAIN_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `google_users`
--

DROP TABLE IF EXISTS `google_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `google_users` (
  `UID` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Bixby Unique ID',
  `EXTERNAL_UID` int(11) NOT NULL COMMENT 'The Unique ID used by the external system feeding Bixby.',
  `EXTERNAL_USERNUMBER` varchar(20) NOT NULL COMMENT 'A user number if different from the EXTERNAL_UID',
  `FIRST_NAME` varchar(45) NOT NULL,
  `LAST_NAME` varchar(45) NOT NULL,
  `MIDDLE_NAME` varchar(45) DEFAULT NULL,
  `GENDER` varchar(1) DEFAULT NULL,
  `DEPARTMENT_ID` int(12) NOT NULL COMMENT 'Department or School ID',
  `DEPARTMENT` varchar(50) DEFAULT NULL,
  `GOOGLE_USERNAME` varchar(30) DEFAULT NULL,
  `GOOGLE_PASSWORD` varchar(25) DEFAULT NULL,
  `DOMAIN_ID` int(2) NOT NULL DEFAULT '1' COMMENT 'ID of the Domain to associate user with. Keys in Domains Table.',
  `USER_TYPEID` int(3) NOT NULL DEFAULT '1' COMMENT 'ID of the user type. Keys in USER_TYPES table.',
  `EXTERNAL_USERSTATUS` int(2) NOT NULL DEFAULT '1' COMMENT 'staff/student status',
  `SUSPEND_ACCOUNT` int(1) DEFAULT '0',
  `EMAIL_OVERRIDE_ADDRESS` varchar(30) DEFAULT NULL COMMENT 'text field to override the email address',
  `ACCOUNT_STATUS` int(1) DEFAULT NULL COMMENT 'active/inactive in external system and Bixby.',
  `CREATED_DATE` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `MODIFIED_DATE` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `USER_DEFINED_1` varchar(255) DEFAULT NULL,
  `USER_DEFINED_2` varchar(255) DEFAULT NULL,
  `USER_DEFINED_3` varchar(255) DEFAULT NULL,
  `UPDATE_STATE` int(2) NOT NULL DEFAULT '0' COMMENT 'Used by Bixby to track the state of the user account. May eventually be depreciated.',
  `USER_TYPE` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`UID`),
  UNIQUE KEY `FK_User_ID` (`EXTERNAL_UID`,`EXTERNAL_USERNUMBER`),
  UNIQUE KEY `FK_Username_Domain` (`GOOGLE_USERNAME`,`DOMAIN_ID`),
  KEY `Sort_UID` (`UID`),
  KEY `Sort_External_UID` (`EXTERNAL_UID`),
  KEY `Sort_User_Number` (`EXTERNAL_USERNUMBER`)
) ENGINE=InnoDB AUTO_INCREMENT=38214 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `google_users_bins` BEFORE INSERT ON `google_users` 
FOR EACH ROW SET NEW.CREATED_DATE = CURRENT_TIMESTAMP */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `group_members`
--

DROP TABLE IF EXISTS `group_members`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `group_members` (
  `ID` int(12) NOT NULL AUTO_INCREMENT,
  `UID` int(11) NOT NULL,
  `GROUPID` int(11) NOT NULL,
  `MEMBER_TYPEID` int(2) NOT NULL DEFAULT '1' COMMENT '1 Member',
  PRIMARY KEY (`ID`),
  KEY `INDEX_UID` (`UID`),
  KEY `INDEX_GROUPID` (`GROUPID`),
  CONSTRAINT `groupid_ibfk_1` FOREIGN KEY (`GROUPID`) REFERENCES `groups` (`GROUPID`) ON DELETE CASCADE ON UPDATE NO ACTION,
  CONSTRAINT `uid_ibfk_1` FOREIGN KEY (`UID`) REFERENCES `google_users` (`UID`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=64669 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `group_types`
--

DROP TABLE IF EXISTS `group_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `group_types` (
  `GROUP_TYPEID` int(11) NOT NULL AUTO_INCREMENT,
  `GROUP_TYPE` varchar(20) DEFAULT NULL,
  `COMMENTS` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`GROUP_TYPEID`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary view structure for view `group_view`
--

DROP TABLE IF EXISTS `group_view`;
/*!50001 DROP VIEW IF EXISTS `group_view`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `group_view` AS SELECT 
 1 AS `UNIQUE_ATTRIBUTE`,
 1 AS `GROUP_MEMBERID`,
 1 AS `UID`,
 1 AS `GROUPID`,
 1 AS `MEMBER_TYPEID`,
 1 AS `GROUP_TYPE`,
 1 AS `GROUP_TYPEID`,
 1 AS `DEPARTMENT_ID`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `groups`
--

DROP TABLE IF EXISTS `groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `groups` (
  `GROUPID` int(11) NOT NULL AUTO_INCREMENT,
  `DEPARTMENT_ID` int(11) DEFAULT NULL COMMENT 'SCHOOLID',
  `GROUP_EMAIL` varchar(50) NOT NULL,
  `GROUP_NAME` varchar(65) NOT NULL,
  `GROUP_DESCRIPTION` varchar(255) DEFAULT NULL,
  `GROUP_STATUS` int(2) NOT NULL DEFAULT '1',
  `DOMAIN_ID` int(2) NOT NULL DEFAULT '1',
  `GROUP_TYPEID` int(10) DEFAULT NULL,
  `GROUP_TYPE` varchar(45) DEFAULT NULL,
  `UNIQUE_ATTRIBUTE` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`GROUPID`),
  KEY `groupid` (`GROUPID`),
  KEY `schoolid` (`DEPARTMENT_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=6107939 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `groups_bins` BEFORE INSERT ON `groups` 
FOR EACH ROW SET NEW.GROUP_TYPEID = (SELECT GROUP_TYPEID FROM group_types WHERE GROUP_TYPE = NEW.GROUP_TYPE) */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `groups_bupd` BEFORE UPDATE ON `groups` 
FOR EACH ROW SET NEW.GROUP_TYPE = (SELECT GROUP_TYPE FROM group_types WHERE GROUP_TYPEID = NEW.GROUP_TYPEID) */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Temporary view structure for view `new_orgmembers`
--

DROP TABLE IF EXISTS `new_orgmembers`;
/*!50001 DROP VIEW IF EXISTS `new_orgmembers`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `new_orgmembers` AS SELECT 
 1 AS `uid`,
 1 AS `external_uid`,
 1 AS `department_id`,
 1 AS `EXTERNAL_USERNUMBER`,
 1 AS `USER_TYPEID`,
 1 AS `NEW_ORGID`,
 1 AS `NEW_ORGPATH`,
 1 AS `OLD_ORGID`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `org_members`
--

DROP TABLE IF EXISTS `org_members`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `org_members` (
  `UID` int(11) NOT NULL,
  `ORGID` int(11) NOT NULL DEFAULT '1',
  `MODIFIED_TS` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`UID`),
  CONSTRAINT `uid_ibfk_2` FOREIGN KEY (`UID`) REFERENCES `google_users` (`UID`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `org_units`
--

DROP TABLE IF EXISTS `org_units`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `org_units` (
  `ORGID` int(11) NOT NULL AUTO_INCREMENT,
  `ORG_UNIT` varchar(50) NOT NULL,
  `PARENT_ORG` varchar(50) DEFAULT NULL,
  `PARENT_PATH` varchar(255) DEFAULT NULL,
  `FULL_PATH` varchar(255) DEFAULT NULL,
  `DESCRIPTION` varchar(255) DEFAULT NULL,
  `FOREIGNKEY` int(11) DEFAULT NULL,
  `UPDATE_ORG` int(2) NOT NULL DEFAULT '1',
  `LEVEL` int(2) DEFAULT NULL,
  `PARENT_ORGID` int(11) NOT NULL DEFAULT '188',
  `DEPARTMENT_ID` int(11) DEFAULT NULL,
  `USER_TYPEID` int(10) DEFAULT NULL,
  `LOW_OU` int(2) DEFAULT NULL,
  `HIGH_OU` int(2) DEFAULT NULL,
  PRIMARY KEY (`ORGID`)
) ENGINE=InnoDB AUTO_INCREMENT=439 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ps_cc`
--

DROP TABLE IF EXISTS `ps_cc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ps_cc` (
  `PS_ID` int(11) NOT NULL,
  `studentid` int(11) NOT NULL,
  `sectionid` int(11) NOT NULL,
  `termid` int(4) NOT NULL,
  `schoolid` int(9) NOT NULL,
  `dateenrolled` datetime DEFAULT NULL,
  `dateleft` datetime DEFAULT NULL,
  PRIMARY KEY (`PS_ID`),
  UNIQUE KEY `PS_ID_UNIQUE` (`PS_ID`),
  KEY `sectionid` (`sectionid`),
  KEY `studentid` (`studentid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `run_history`
--

DROP TABLE IF EXISTS `run_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `run_history` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `STARTED_TS` timestamp NULL DEFAULT NULL,
  `FINISHED_TS` timestamp NULL DEFAULT NULL,
  `STATUS` varchar(45) DEFAULT 'Running',
  `OPTIONS` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `schools`
--

DROP TABLE IF EXISTS `schools`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `schools` (
  `ID` int(12) NOT NULL,
  `FULL_NAME` varchar(255) NOT NULL,
  `SCHOOL_NUMBER` int(15) NOT NULL,
  `ABBREVIATION` varchar(20) NOT NULL,
  `SHORT_NAME` varchar(30) DEFAULT NULL,
  `LOW_GRADE` int(2) NOT NULL,
  `HIGH_GRADE` int(2) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sections_py`
--

DROP TABLE IF EXISTS `sections_py`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sections_py` (
  `SECTIONID` int(10) NOT NULL AUTO_INCREMENT,
  `SCHOOLID` int(11) DEFAULT NULL,
  `GROUP_EMAIL` varchar(50) NOT NULL,
  `GROUP_NAME` varchar(65) NOT NULL,
  `GROUP_DESCRIPTION` varchar(255) DEFAULT NULL,
  `TERMID` int(4) DEFAULT NULL,
  `GROUP_OWNER` int(11) DEFAULT NULL,
  `COURSE_NUMBER` varchar(10) DEFAULT NULL,
  `SECTION_NUMBER` varchar(5) DEFAULT NULL,
  `COURSE_NAME` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`SECTIONID`)
) ENGINE=InnoDB AUTO_INCREMENT=43804 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sites`
--

DROP TABLE IF EXISTS `sites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sites` (
  `SITEID` int(11) NOT NULL AUTO_INCREMENT,
  `SITECODE` int(11) DEFAULT NULL,
  `SITE` varchar(45) DEFAULT NULL,
  `DESCRIPTION` varchar(45) DEFAULT NULL,
  `ABBREVIATION` varchar(12) DEFAULT NULL,
  `UNIQUE_IDENTIFIER` varchar(45) DEFAULT NULL,
  `LOWER_UNIT` int(3) DEFAULT NULL,
  `UPPER_UNIT` int(3) DEFAULT NULL,
  `USER_TYPEID` int(2) NOT NULL DEFAULT '1',
  `AUTO_EXCLUDE` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`SITEID`),
  UNIQUE KEY `SITECODE_UNIQUE` (`SITECODE`),
  KEY `SITECODE_INDX` (`SITECODE`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `staff_org`
--

DROP TABLE IF EXISTS `staff_org`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `staff_org` (
  `STAFFID` int(11) NOT NULL,
  `ORGID` int(11) NOT NULL DEFAULT '1',
  `ORG_PATH` varchar(255) DEFAULT NULL,
  `UPDATE_STAFF_ORG` varchar(45) NOT NULL DEFAULT '1',
  PRIMARY KEY (`STAFFID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `staff_py`
--

DROP TABLE IF EXISTS `staff_py`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `staff_py` (
  `STAFFID` int(11) NOT NULL,
  `SCHOOLID` int(11) NOT NULL DEFAULT '0',
  `TEACHERNUMBER` varchar(20) DEFAULT NULL,
  `CERTIFICATED` int(1) NOT NULL DEFAULT '0',
  `FIRST_NAME` varchar(30) NOT NULL,
  `LAST_NAME` varchar(30) NOT NULL,
  `MIDDLE_NAME` varchar(30) DEFAULT NULL,
  `GENDER` varchar(4) DEFAULT NULL,
  `HOMEROOM` varchar(255) DEFAULT NULL,
  `EXTERNAL_USERSTATUS` int(2) NOT NULL DEFAULT '1',
  `STAFF_TYPE` int(1) NOT NULL DEFAULT '1',
  `SUSPEND_ACCOUNT` int(1) NOT NULL DEFAULT '0',
  `BUSD_Email` int(1) NOT NULL DEFAULT '0',
  `BUSD_Email_Address` varchar(31) DEFAULT NULL,
  `STAFF_CONFERENCE` int(1) NOT NULL DEFAULT '2',
  PRIMARY KEY (`STAFFID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `student_org`
--

DROP TABLE IF EXISTS `student_org`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `student_org` (
  `STUDENTID` int(11) NOT NULL,
  `GOOGLE_USERNAME` varchar(20) NOT NULL,
  `ORGID` int(11) NOT NULL DEFAULT '1',
  `ORG_PATH` varchar(255) DEFAULT NULL,
  `UPDATE_STUDENT_ORG` int(2) NOT NULL DEFAULT '1',
  PRIMARY KEY (`STUDENTID`),
  UNIQUE KEY `google_username_UNIQUE` (`GOOGLE_USERNAME`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `students_py`
--

DROP TABLE IF EXISTS `students_py`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `students_py` (
  `STUDENTID` int(11) NOT NULL,
  `SCHOOLID` int(11) NOT NULL,
  `STUDENT_NUMBER` int(11) NOT NULL,
  `FIRST_NAME` varchar(30) NOT NULL,
  `LAST_NAME` varchar(30) NOT NULL,
  `MIDDLE_NAME` varchar(30) DEFAULT NULL,
  `DOB` date NOT NULL,
  `GENDER` varchar(1) DEFAULT NULL,
  `GRADE_LEVEL` int(2) NOT NULL,
  `HOME_ROOM` varchar(255) DEFAULT NULL,
  `AREA` varchar(255) DEFAULT NULL,
  `ENTRYDATE` date NOT NULL,
  `EXITDATE` date NOT NULL,
  `EXTERNAL_USERSTATUS` int(2) NOT NULL,
  `SUSPEND_ACCOUNT` int(1) NOT NULL DEFAULT '0',
  `EMAIL_OVERRIDE` varchar(45) DEFAULT NULL,
  `STUDENT_WEB_ID` varchar(45) DEFAULT NULL,
  `PARENT_WEB_ID` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`STUDENTID`),
  KEY `STUDENTID` (`STUDENTID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Students Table';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `studentschedule_py`
--

DROP TABLE IF EXISTS `studentschedule_py`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `studentschedule_py` (
  `PS_ID` int(11) NOT NULL,
  `studentid` int(11) NOT NULL,
  `sectionid` int(11) NOT NULL,
  `termid` int(4) NOT NULL,
  `schoolid` int(9) NOT NULL,
  `dateenrolled` datetime DEFAULT NULL,
  `dateleft` datetime DEFAULT NULL,
  `update_cc` int(2) NOT NULL DEFAULT '1',
  PRIMARY KEY (`PS_ID`),
  UNIQUE KEY `PS_ID_UNIQUE` (`PS_ID`),
  KEY `STUDENTID_INDEX` (`studentid`),
  KEY `SECTIONID` (`sectionid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user_types`
--

DROP TABLE IF EXISTS `user_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_types` (
  `USER_TYPEID` int(10) NOT NULL,
  `USER_TYPE` varchar(20) NOT NULL,
  `DEFAULT_DOMAIN_ID` tinyint(4) DEFAULT '1',
  `DEFAULT_TYPE` tinyint(4) DEFAULT '0',
  PRIMARY KEY (`USER_TYPEID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary view structure for view `users_py`
--

DROP TABLE IF EXISTS `users_py`;
/*!50001 DROP VIEW IF EXISTS `users_py`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `users_py` AS SELECT 
 1 AS `external_uid`,
 1 AS `department_id`,
 1 AS `EXTERNAL_USERNUMBER`,
 1 AS `FIRST_NAME`,
 1 AS `LAST_NAME`,
 1 AS `MIDDLE_NAME`,
 1 AS `GENDER`,
 1 AS `OU_KEY`,
 1 AS `ENTRYDATE`,
 1 AS `EXITDATE`,
 1 AS `EXTERNAL_USERSTATUS`,
 1 AS `SUSPEND_ACCOUNT`,
 1 AS `EMAIL_OVERRIDE`,
 1 AS `USER_TYPEID`*/;
SET character_set_client = @saved_cs_client;

--
-- Final view structure for view `active_users`
--

/*!50001 DROP VIEW IF EXISTS `active_users`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `active_users` AS select `gu`.`UID` AS `UID`,`gu`.`EXTERNAL_UID` AS `EXTERNAL_UID`,cast(`sp`.`TEACHERNUMBER` as char charset utf8) AS `EXTERNAL_USERNUMBER`,`sp`.`FIRST_NAME` AS `FIRST_NAME`,`sp`.`LAST_NAME` AS `LAST_NAME`,`sp`.`MIDDLE_NAME` AS `MIDDLE_NAME`,`sp`.`SCHOOLID` AS `DEPARTMENT_ID`,`gu`.`GOOGLE_USERNAME` AS `GOOGLE_USERNAME`,`d`.`DOMAIN_NAME` AS `DOMAIN_NAME`,`d`.`DOMAIN_ID` AS `DOMAIN_ID`,`ut`.`USER_TYPE` AS `USER_TYPE`,`ut`.`USER_TYPEID` AS `USER_TYPEID`,concat(`gu`.`GOOGLE_USERNAME`,'@',`d`.`DOMAIN_NAME`) AS `FULL_EMAIL`,lcase(substring_index(`sp`.`BUSD_Email_Address`,'@',1)) AS `EMAIL_OVERRIDE_ADDRESS` from (((`google_users` `gu` join `user_types` `ut` on((`gu`.`USER_TYPEID` = `ut`.`USER_TYPEID`))) join `domains` `d` on((`ut`.`DEFAULT_DOMAIN_ID` = `d`.`DOMAIN_ID`))) join `staff_py` `sp` on((`gu`.`EXTERNAL_UID` = `sp`.`STAFFID`))) where ((`ut`.`USER_TYPE` = 'Staff') and (`sp`.`EXTERNAL_USERSTATUS` = 0) and (`sp`.`SUSPEND_ACCOUNT` = 0) and (`gu`.`ACCOUNT_STATUS` < 3)) union all select `gu`.`UID` AS `uid`,`gu`.`EXTERNAL_UID` AS `EXTERNAL_UID`,cast(`sp`.`STUDENT_NUMBER` as char charset utf8) AS `EXTERNAL_USERNUMBER`,`sp`.`FIRST_NAME` AS `FIRST_NAME`,`sp`.`LAST_NAME` AS `LAST_NAME`,`sp`.`MIDDLE_NAME` AS `MIDDLE_NAME`,`sp`.`SCHOOLID` AS `DEPARTMENT_ID`,`gu`.`GOOGLE_USERNAME` AS `GOOGLE_USERNAME`,`d`.`DOMAIN_NAME` AS `DOMAIN_NAME`,`d`.`DOMAIN_ID` AS `DOMAIN_ID`,`ut`.`USER_TYPE` AS `USER_TYPE`,`ut`.`USER_TYPEID` AS `USER_TYPEID`,concat(`gu`.`GOOGLE_USERNAME`,'@',`d`.`DOMAIN_NAME`) AS `FULL_EMAIL`,NULL AS `EMAIL_OVERRIDE_ADDRESS` from (((`google_users` `gu` join `user_types` `ut` on((`gu`.`USER_TYPEID` = `ut`.`USER_TYPEID`))) join `domains` `d` on((`ut`.`DEFAULT_DOMAIN_ID` = `d`.`DOMAIN_ID`))) join `students_py` `sp` on((`gu`.`EXTERNAL_UID` = `sp`.`STUDENTID`))) where ((`ut`.`USER_TYPE` = 'Student') and (`sp`.`EXTERNAL_USERSTATUS` = 0) and (`sp`.`SUSPEND_ACCOUNT` = 0) and (`gu`.`ACCOUNT_STATUS` < 3)) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `group_view`
--

/*!50001 DROP VIEW IF EXISTS `group_view`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `group_view` AS select `g`.`UNIQUE_ATTRIBUTE` AS `UNIQUE_ATTRIBUTE`,`gm`.`ID` AS `GROUP_MEMBERID`,`gm`.`UID` AS `UID`,`gm`.`GROUPID` AS `GROUPID`,`gm`.`MEMBER_TYPEID` AS `MEMBER_TYPEID`,`gt`.`GROUP_TYPE` AS `GROUP_TYPE`,`gt`.`GROUP_TYPEID` AS `GROUP_TYPEID`,`g`.`DEPARTMENT_ID` AS `DEPARTMENT_ID` from ((`groups` `g` join `group_members` `gm` on((`g`.`GROUPID` = `gm`.`GROUPID`))) join `group_types` `gt` on((`g`.`GROUP_TYPEID` = `gt`.`GROUP_TYPEID`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `new_orgmembers`
--

/*!50001 DROP VIEW IF EXISTS `new_orgmembers`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `new_orgmembers` AS select `gu`.`UID` AS `uid`,`up`.`external_uid` AS `external_uid`,`up`.`department_id` AS `department_id`,`up`.`EXTERNAL_USERNUMBER` AS `EXTERNAL_USERNUMBER`,`up`.`USER_TYPEID` AS `USER_TYPEID`,`ou`.`ORGID` AS `NEW_ORGID`,`ou`.`FULL_PATH` AS `NEW_ORGPATH`,`om`.`ORGID` AS `OLD_ORGID` from (((`users_py` `up` join `org_units` `ou` on(((`up`.`OU_KEY` between `ou`.`LOW_OU` and `ou`.`HIGH_OU`) and ((case when (`up`.`USER_TYPEID` = 1) then 0 else `up`.`department_id` end) = `ou`.`DEPARTMENT_ID`) and ((case when (`up`.`USER_TYPEID` = 1) then 1 else 4 end) = `ou`.`LEVEL`)))) join `google_users` `gu` on(((`up`.`external_uid` = `gu`.`EXTERNAL_UID`) and (`up`.`USER_TYPEID` = `gu`.`USER_TYPEID`)))) left join `org_members` `om` on((`gu`.`UID` = `om`.`UID`))) where ((`gu`.`ACCOUNT_STATUS` <> 5) and ((`om`.`ORGID` <> `ou`.`ORGID`) or isnull(`om`.`ORGID`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `users_py`
--

/*!50001 DROP VIEW IF EXISTS `users_py`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `users_py` AS select `students_py`.`STUDENTID` AS `external_uid`,`students_py`.`SCHOOLID` AS `department_id`,cast(`students_py`.`STUDENT_NUMBER` as char charset utf8) AS `EXTERNAL_USERNUMBER`,`students_py`.`FIRST_NAME` AS `FIRST_NAME`,`students_py`.`LAST_NAME` AS `LAST_NAME`,`students_py`.`MIDDLE_NAME` AS `MIDDLE_NAME`,ucase(`students_py`.`GENDER`) AS `GENDER`,`students_py`.`GRADE_LEVEL` AS `OU_KEY`,`students_py`.`ENTRYDATE` AS `ENTRYDATE`,`students_py`.`EXITDATE` AS `EXITDATE`,`students_py`.`EXTERNAL_USERSTATUS` AS `EXTERNAL_USERSTATUS`,`students_py`.`SUSPEND_ACCOUNT` AS `SUSPEND_ACCOUNT`,`students_py`.`EMAIL_OVERRIDE` AS `EMAIL_OVERRIDE`,'2' AS `USER_TYPEID` from `students_py` union select `staff_py`.`STAFFID` AS `external_uid`,`staff_py`.`SCHOOLID` AS `department_id`,`staff_py`.`TEACHERNUMBER` AS `external_usernumber`,`staff_py`.`FIRST_NAME` AS `FIRST_NAME`,`staff_py`.`LAST_NAME` AS `LAST_NAME`,`staff_py`.`MIDDLE_NAME` AS `MIDDLE_NAME`,ucase(`staff_py`.`GENDER`) AS `GENDER`,30 AS `OU_KEY`,str_to_date('08/27/2014','%m/%d/%Y') AS `Entrydate`,str_to_date('06/12/2015','%m/%d/%Y') AS `exitdate`,`staff_py`.`EXTERNAL_USERSTATUS` AS `EXTERNAL_USERSTATUS`,`staff_py`.`SUSPEND_ACCOUNT` AS `SUSPEND_ACCOUNT`,`staff_py`.`BUSD_Email_Address` AS `EMAIL_OVERRIDE`,'1' AS `USER_TYPEID` from `staff_py` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-11-14 17:13:08
