CREATE DATABASE  IF NOT EXISTS `historico_archivos` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `historico_archivos`;
-- MySQL dump 10.13  Distrib 8.0.29, for Win64 (x86_64)
--
-- Host: localhost    Database: historico_archivos
-- ------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `archivos`
--

DROP TABLE IF EXISTS `archivos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `archivos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `fecha_publicacion` datetime(6) DEFAULT NULL,
  `nombre` varchar(255) DEFAULT NULL,
  `nombre_periodico` varchar(255) DEFAULT NULL,
  `ruta` varchar(255) DEFAULT NULL,
  `tiempo_procesamiento_ia` float DEFAULT NULL,
  `fecha_procesamiento_ia` datetime DEFAULT NULL,
  `tiempo_procesamiento_ocr` float DEFAULT NULL,
  `fecha_procesamiento_ocr` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=122122 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `archivos`
--

LOCK TABLES `archivos` WRITE;
/*!40000 ALTER TABLE `archivos` DISABLE KEYS */;
/*!40000 ALTER TABLE `archivos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `divisiones_politicas`
--

DROP TABLE IF EXISTS `divisiones_politicas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `divisiones_politicas` (
  `archivo_id` int DEFAULT NULL,
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK8q1cjnv7jsf08e0ovonhxajiy` (`archivo_id`),
  CONSTRAINT `FK8q1cjnv7jsf08e0ovonhxajiy` FOREIGN KEY (`archivo_id`) REFERENCES `archivos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1291 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `divisiones_politicas`
--

LOCK TABLES `divisiones_politicas` WRITE;
/*!40000 ALTER TABLE `divisiones_politicas` DISABLE KEYS */;
/*!40000 ALTER TABLE `divisiones_politicas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `unidades_militares`
--

DROP TABLE IF EXISTS `unidades_militares`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `unidades_militares` (
  `archivo_id` int DEFAULT NULL,
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK4uwidj8wdlqrv2bdqg5fflll6` (`archivo_id`),
  CONSTRAINT `FK4uwidj8wdlqrv2bdqg5fflll6` FOREIGN KEY (`archivo_id`) REFERENCES `archivos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=644 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `unidades_militares`
--

LOCK TABLES `unidades_militares` WRITE;
/*!40000 ALTER TABLE `unidades_militares` DISABLE KEYS */;
/*!40000 ALTER TABLE `unidades_militares` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-09-01 10:32:47
