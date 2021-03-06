
-- Fixes uppercase TRIGGER names.

DROP TRIGGER IF EXISTS `bixby_db`.`GROUPS_BINS`;
CREATE DEFINER=`root`@`localhost` TRIGGER `groups_bins` BEFORE INSERT ON `groups` 
FOR EACH ROW SET NEW.GROUP_TYPEID = (SELECT GROUP_TYPEID FROM group_types WHERE GROUP_TYPE = NEW.GROUP_TYPE);

DROP TRIGGER IF EXISTS `bixby_db`.`GROUPS_BUPD`;
CREATE DEFINER=`root`@`localhost` TRIGGER `groups_bupd` BEFORE UPDATE ON `groups` 
FOR EACH ROW SET NEW.GROUP_TYPE = (SELECT GROUP_TYPE FROM group_types WHERE GROUP_TYPEID = NEW.GROUP_TYPEID);

DROP TRIGGER IF EXISTS `bixby_db`.`GOOGLE_USERS_BINS`;
CREATE DEFINER=`root`@`localhost` TRIGGER `google_users_bins` BEFORE INSERT ON `google_users` 
FOR EACH ROW SET NEW.CREATED_DATE = CURRENT_TIMESTAMP;

SHOW TRIGGERS;