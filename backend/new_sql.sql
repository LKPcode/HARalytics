-- MySQL Workbench Synchronization
-- Generated: 2020-11-29 15:30
-- Model: New Model
-- Version: 1.0
-- Project: Name of the project
-- Author: Home

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

CREATE SCHEMA IF NOT EXISTS `mydtbs` DEFAULT CHARACTER SET utf8 ;

CREATE TABLE IF NOT EXISTS `mydtbs`.`User` (
  `email` VARCHAR(255) NOT NULL,
  `ip` VARCHAR(255) NOT NULL,
  `username` VARCHAR(255) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `ISP` VARCHAR(255) NULL DEFAULT NULL,
  `admin` TINYINT(4) NULL DEFAULT NULL,
  PRIMARY KEY (`email`),
  UNIQUE INDEX `e-mail_UNIQUE` (`email` ASC) VISIBLE,
  INDEX `fk_user_ip1_idx` (`ip` ASC) VISIBLE
  -- ,
 -- CONSTRAINT `fk_user_ip1`
  --  FOREIGN KEY (`ip`)
  --  REFERENCES `mydtbs`.`Ip` (`ip`)
  --  ON DELETE NO ACTION
  --  ON UPDATE NO ACTION
    )
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

CREATE TABLE IF NOT EXISTS `mydtbs`.`Header` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `content_type` VARCHAR(255) NULL DEFAULT NULL,
  `age` INT(11) NULL DEFAULT NULL,
  `cache_control` VARCHAR(1024) NULL DEFAULT NULL,
  `pragma` VARCHAR(255) NULL DEFAULT NULL,
  `expires` DATETIME NULL DEFAULT NULL,
  `last_modified` DATETIME NULL DEFAULT NULL,
  `host` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

CREATE TABLE IF NOT EXISTS `mydtbs`.`Ip` (
  `ip` VARCHAR(255) NOT NULL,
  `city` VARCHAR(255) NULL DEFAULT NULL,
  `country` VARCHAR(255) NULL DEFAULT NULL,
  `x` FLOAT(11) NULL DEFAULT NULL,
  `y` FLOAT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`ip`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

CREATE TABLE IF NOT EXISTS `mydtbs`.`Entry` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(255) NULL DEFAULT NULL,
  `serverIPAddress` VARCHAR(255) NULL DEFAULT NULL,
  `reqHeader` INT(11) NULL DEFAULT NULL,
  `resHeader` INT(11) NULL DEFAULT NULL,
  `method` VARCHAR(255) NULL DEFAULT NULL,
  `reqAddress` VARCHAR(255) NULL DEFAULT NULL,
  `startedDateTime` DATETIME NULL DEFAULT NULL,
  `wait` INT(11) NULL DEFAULT NULL,
  `url` VARCHAR(1024) NULL DEFAULT NULL,
  `domain` VARCHAR(255) NULL DEFAULT NULL,
  `is_page` ENUM('true' , 'false'),
  `status` INT(11) NULL DEFAULT NULL,
  `statusText` VARCHAR(255) NULL DEFAULT NULL,
  `day` ENUM('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday') NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_entry_user_idx` (`email` ASC) VISIBLE,
  INDEX `fk_entry_ip1_idx` (`serverIPAddress` ASC) VISIBLE,
  INDEX `fkhdr1_idx` (`reqHeader` ASC) VISIBLE,
  INDEX `fkhdr2_idx` (`resHeader` ASC) VISIBLE
 -- ,
 -- CONSTRAINT `fk_entry_user`
 --   FOREIGN KEY (`user_e-mail`)
 --  REFERENCES `mydb`.`user` (`e-mail`)
 --   ON DELETE SET NULL
 --   ON UPDATE CASCADE,
 --  CONSTRAINT `fk_entry_ip1`
 --   FOREIGN KEY (`serverIP`)
 --   REFERENCES `mydb`.`ip` (`id_ip`)
 --   ON DELETE SET NULL
 --   ON UPDATE CASCADE,
 --   CONSTRAINT `fkhdr1`
 --   FOREIGN KEY (`reqHeader`)
 --   REFERENCES `mydb`.`header` (`id_header`)
 --   ON DELETE SET NULL
 --   ON UPDATE CASCADE,
 --  CONSTRAINT `fkhdr2`
--   FOREIGN KEY (`resHeader`)
--   REFERENCES `mydb`.`header` (`id_header`)
 --    ON DELETE SET NULL
 --    ON UPDATE CASCADE
 )
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
