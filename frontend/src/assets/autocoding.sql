-- MySQL Workbench Synchronization
-- Generated: 2020-11-29 15:30
-- Model: New Model
-- Version: 1.0
-- Project: Name of the project
-- Author: Home

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;

CREATE TABLE IF NOT EXISTS `mydb`.`user` (
  `e-mail` VARCHAR(255) NOT NULL,
  `user_ip` VARCHAR(255) NOT NULL,
  `username` VARCHAR(255) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `ISP` VARCHAR(255) NULL DEFAULT NULL,
  `admin` TINYINT(4) NULL DEFAULT NULL,
  PRIMARY KEY (`e-mail`),
  UNIQUE INDEX `e-mail_UNIQUE` (`e-mail` ASC) VISIBLE,
  INDEX `fk_user_ip1_idx` (`user_ip` ASC) VISIBLE,
  CONSTRAINT `fk_user_ip1`
    FOREIGN KEY (`user_ip`)
    REFERENCES `mydb`.`ip` (`id_ip`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

CREATE TABLE IF NOT EXISTS `mydb`.`entry` (
  `id_entry` INT(11) NOT NULL AUTO_INCREMENT,
  `user_e-mail` VARCHAR(255) NULL DEFAULT NULL,
  `serverIP` VARCHAR(255) NULL DEFAULT NULL,
  `reqHeader` INT(11) NULL DEFAULT NULL,
  `resHeader` INT(11) NULL DEFAULT NULL,
  `method` VARCHAR(255) NULL DEFAULT NULL,
  `reqAddress` INT(11) NULL DEFAULT NULL,
  `startDateTime` DATETIME NULL DEFAULT NULL,
  `waitTime` INT(11) NULL DEFAULT NULL,
  `url` VARCHAR(255) NULL DEFAULT NULL,
  `status` INT(11) NULL DEFAULT NULL,
  `statusText` VARCHAR(255) NULL DEFAULT NULL,
  `day` ENUM('monday', 'tuesday', 'wednesday', 'thursday', ' friday', 'saturday', 'sunday') NULL DEFAULT NULL,
  PRIMARY KEY (`id_entry`),
  INDEX `fk_entry_user_idx` (`user_e-mail` ASC) VISIBLE,
  INDEX `fk_entry_ip1_idx` (`serverIP` ASC) VISIBLE,
  INDEX `fkhdr1_idx` (`reqHeader` ASC) VISIBLE,
  INDEX `fkhdr2_idx` (`resHeader` ASC) VISIBLE,
  CONSTRAINT `fk_entry_user`
    FOREIGN KEY (`user_e-mail`)
    REFERENCES `mydb`.`user` (`e-mail`)
    ON DELETE SET NULL
    ON UPDATE CASCADE,
  CONSTRAINT `fk_entry_ip1`
    FOREIGN KEY (`serverIP`)
    REFERENCES `mydb`.`ip` (`id_ip`)
    ON DELETE SET NULL
    ON UPDATE CASCADE,
  CONSTRAINT `fkhdr1`
    FOREIGN KEY (`reqHeader`)
    REFERENCES `mydb`.`header` (`id_header`)
    ON DELETE SET NULL
    ON UPDATE CASCADE,
  CONSTRAINT `fkhdr2`
    FOREIGN KEY (`resHeader`)
    REFERENCES `mydb`.`header` (`id_header`)
    ON DELETE SET NULL
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

CREATE TABLE IF NOT EXISTS `mydb`.`header` (
  `id_header` INT(11) NOT NULL AUTO_INCREMENT,
  `content-type` VARCHAR(255) NULL DEFAULT NULL,
  `age` INT(11) NULL DEFAULT NULL,
  `cache-control` VARCHAR(255) NULL DEFAULT NULL,
  `pragma` VARCHAR(255) NULL DEFAULT NULL,
  `expires` DATETIME NULL DEFAULT NULL,
  `last-modified` DATETIME NULL DEFAULT NULL,
  `host` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY (`id_header`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

CREATE TABLE IF NOT EXISTS `mydb`.`ip` (
  `id_ip` VARCHAR(255) NOT NULL,
  `city` VARCHAR(255) NULL DEFAULT NULL,
  `country` VARCHAR(255) NULL DEFAULT NULL,
  `x` FLOAT(11) NULL DEFAULT NULL,
  `y` FLOAT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id_ip`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
