CREATE DATABASE  IF NOT EXISTS `hcm` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `hcm`;
-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: hcm
-- ------------------------------------------------------
-- Server version	8.0.34

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
-- Table structure for table `administrativestaff`
--

DROP TABLE IF EXISTS `administrativestaff`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `administrativestaff` (
  `Admin_Id` varchar(10) NOT NULL,
  `First_Name` varchar(50) DEFAULT NULL,
  `Middle_Name` varchar(50) DEFAULT NULL,
  `Last_Name` varchar(50) DEFAULT NULL,
  `Date_Of_Birth` varchar(20) DEFAULT NULL,
  `Gender` varchar(10) DEFAULT NULL,
  `Address` varchar(100) DEFAULT NULL,
  `Position` varchar(50) DEFAULT NULL,
  `Phone_Number` varchar(15) DEFAULT NULL,
  `Email_Id` varchar(100) DEFAULT NULL,
  `IP_Address` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`Admin_Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `administrativestaff`
--

LOCK TABLES `administrativestaff` WRITE;
/*!40000 ALTER TABLE `administrativestaff` DISABLE KEYS */;
INSERT INTO `administrativestaff` VALUES ('A1','Sarah','M','Smith','1980-03-25','Female','789 Elm Street','Office Manager','555-123-4567','sarah@email.com','192.168.1.1'),('A2','James','C','Johnson','1975-09-12','Male','456 Oak Avenue','HR Coordinator','888-987-6543','james@email.com','192.168.1.2'),('A3','Linda','A','Brown','1988-11-02','Female','123 Maple Road','Receptionist','777-555-3210','linda@email.com','192.168.1.3');
/*!40000 ALTER TABLE `administrativestaff` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `appointments`
--

DROP TABLE IF EXISTS `appointments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appointments` (
  `Appointment_Id` int NOT NULL,
  `Date` varchar(10) DEFAULT NULL,
  `Time` varchar(10) DEFAULT NULL,
  `Patient_Name` varchar(50) DEFAULT NULL,
  `Scheduled` tinyint(1) DEFAULT NULL,
  `Cancellation` tinyint(1) DEFAULT NULL,
  `Completed` tinyint(1) DEFAULT NULL,
  `Specialization` varchar(50) DEFAULT NULL,
  `Department` varchar(50) DEFAULT NULL,
  `Patient_ID` varchar(10) DEFAULT NULL,
  `doctor_id` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`Appointment_Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appointments`
--

LOCK TABLES `appointments` WRITE;
/*!40000 ALTER TABLE `appointments` DISABLE KEYS */;
INSERT INTO `appointments` VALUES (1,'2023-10-18','10:00:00','Michael Williams',1,0,0,'Cardiology','Cardiology','1','D3'),(2,'2023-10-19','14:30:00','Emily Davis',1,0,0,'Dermatology','Dermatology','2','D1'),(3,'2023-10-20','11:15:00','Sophia Miller',1,0,0,'Orthopedics','Orthopedics','3','D2'),(4,'2023-12-18','10:00:18','Jasmine',1,0,0,'Cardiology','Cardiology','P4','D3');
/*!40000 ALTER TABLE `appointments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bill`
--

DROP TABLE IF EXISTS `bill`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bill` (
  `Bill_Id` varchar(10) NOT NULL,
  `Date` varchar(10) DEFAULT NULL,
  `total_amount` int DEFAULT NULL,
  `Payment_Status` varchar(20) DEFAULT NULL,
  `Time` varchar(10) DEFAULT NULL,
  `patient_id` varchar(10) DEFAULT NULL,
  `admin_id` varchar(10) DEFAULT NULL,
  `doctor_id` varchar(10) DEFAULT NULL,
  `Room_Type` varchar(10) DEFAULT NULL,
  `Tests_Done` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`Bill_Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bill`
--

LOCK TABLES `bill` WRITE;
/*!40000 ALTER TABLE `bill` DISABLE KEYS */;
INSERT INTO `bill` VALUES ('B1','2023-12-13',2525,'Paid','20:44:40','P1','A1','D1','Suite','X-Ray,MRI'),('B2','2023-12-13',2325,'Paid','20:46:32','P1','A1','D1','Suite','X-Ray'),('B3','2023-12-13',2325,'Paid','20:47:57','P1','A1','D1','Suite','X-Ray'),('B4','2023-12-13',2325,'Paid','20:49:15','P1','A1','D1','Suite','X-Ray');
/*!40000 ALTER TABLE `bill` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `credentials`
--

DROP TABLE IF EXISTS `credentials`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `credentials` (
  `User_Id` varchar(10) DEFAULT NULL,
  `Password` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `credentials`
--

LOCK TABLES `credentials` WRITE;
/*!40000 ALTER TABLE `credentials` DISABLE KEYS */;
INSERT INTO `credentials` VALUES ('A1','password123'),('A2','securepass'),('A3','adminpass'),('D1','Password@123'),('D2','Password@231'),('D3','Password@132');
/*!40000 ALTER TABLE `credentials` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `doctors`
--

DROP TABLE IF EXISTS `doctors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doctors` (
  `Doctor_Id` varchar(10) NOT NULL,
  `Doctor_Name` varchar(50) DEFAULT NULL,
  `Date_Of_Birth` varchar(20) DEFAULT NULL,
  `Gender` varchar(10) DEFAULT NULL,
  `Address` varchar(100) DEFAULT NULL,
  `Specialization` varchar(50) DEFAULT NULL,
  `License_Number` varchar(20) DEFAULT NULL,
  `Age` int DEFAULT NULL,
  `Experience` varchar(20) DEFAULT NULL,
  `Department` varchar(50) DEFAULT NULL,
  `Email_Id` varchar(100) DEFAULT NULL,
  `Mobile_Number` varchar(15) DEFAULT NULL,
  `Language` varchar(50) DEFAULT NULL,
  `Visitation_Charge` decimal(10,2) DEFAULT NULL,
  `IP_Address` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`Doctor_Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doctors`
--

LOCK TABLES `doctors` WRITE;
/*!40000 ALTER TABLE `doctors` DISABLE KEYS */;
INSERT INTO `doctors` VALUES ('D1','Utkarsh  Tiwary','25/03/2004','Male','Vadodara','Dermatology','D2503',19,'15','Dermatology','utkarshtiwary2004@gmail.com','98195331471','English, Hindi, Gujarati, Sanskrit',2000.00,'192.168.1.1'),('D2','Jayesh D Kankaria','18/12/2002','Male','Kolkata','Orthopedics','D1812',21,'7','Orthopedics','jayeshkanakaria@gmail.com','9876543210','Hindi, English, Bengali, Marwadi',1800.00,'192.168.1.2'),('D3','Pranika  Kumar','5/12/2003','Female','Noida','Cardiology','D0512',20,'10','Cardiology','pranikakumar@gmail.com','1234567890','English, Hindi',1500.00,'192.168.1.3');
/*!40000 ALTER TABLE `doctors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `doctorschedules`
--

DROP TABLE IF EXISTS `doctorschedules`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doctorschedules` (
  `Day` varchar(20) DEFAULT NULL,
  `Type_of_Work` varchar(20) DEFAULT NULL,
  `Time` varchar(20) DEFAULT NULL,
  `Doctor_ID` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doctorschedules`
--

LOCK TABLES `doctorschedules` WRITE;
/*!40000 ALTER TABLE `doctorschedules` DISABLE KEYS */;
INSERT INTO `doctorschedules` VALUES ('Monday','Consultation','10:00 AM - 2:00 PM','D1'),('Tuesday','Consultation','9:00 AM - 1:00 PM','D2'),('Wednesday','Consultation','1:00 PM - 5:00 PM','D3'),('Thursday','OT','12:00 PM - 5:00 PM','D1'),('Friday','OT','2:00 PM - 7:00 PM','D2'),('Saturday','OT','10:00 AM - 2:00 PM','D3');
/*!40000 ALTER TABLE `doctorschedules` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `equipmentrecords`
--

DROP TABLE IF EXISTS `equipmentrecords`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `equipmentrecords` (
  `Bill_Id` varchar(10) DEFAULT NULL,
  `Equipment_Name` varchar(50) DEFAULT NULL,
  `Equipment_Cost` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `equipmentrecords`
--

LOCK TABLES `equipmentrecords` WRITE;
/*!40000 ALTER TABLE `equipmentrecords` DISABLE KEYS */;
INSERT INTO `equipmentrecords` VALUES ('1','X-ray Machine',5000.00),('2','Ultrasound Scanner',3500.00),('3','ECG Machine',2500.00);
/*!40000 ALTER TABLE `equipmentrecords` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `insuranceinformation`
--

DROP TABLE IF EXISTS `insuranceinformation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `insuranceinformation` (
  `Insurance_Id` varchar(10) NOT NULL,
  `Company_Name` varchar(50) DEFAULT NULL,
  `Coverage_Amount` decimal(10,2) DEFAULT NULL,
  `Policy_Number` varchar(20) DEFAULT NULL,
  `Patient_ID` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`Insurance_Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `insuranceinformation`
--

LOCK TABLES `insuranceinformation` WRITE;
/*!40000 ALTER TABLE `insuranceinformation` DISABLE KEYS */;
INSERT INTO `insuranceinformation` VALUES ('I1','ABC Insurance',5000.00,'POL001','P1'),('I2','XYZ Insurance',7500.00,'POL002','P2'),('I3','LMN Insurance',6000.00,'POL003','P3');
/*!40000 ALTER TABLE `insuranceinformation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opdbill`
--

DROP TABLE IF EXISTS `opdbill`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `opdbill` (
  `Date` varchar(10) DEFAULT NULL,
  `Time` varchar(10) DEFAULT NULL,
  `Patient_ID` varchar(10) DEFAULT NULL,
  `Doctor_ID` varchar(10) DEFAULT NULL,
  `OPD_Bill_ID` varchar(10) NOT NULL,
  `Admin_ID` varchar(10) DEFAULT NULL,
  `total_amount` int DEFAULT NULL,
  PRIMARY KEY (`OPD_Bill_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opdbill`
--

LOCK TABLES `opdbill` WRITE;
/*!40000 ALTER TABLE `opdbill` DISABLE KEYS */;
INSERT INTO `opdbill` VALUES ('2023-12-12','23:15:24','P1','D1','O1','A1',2050),('2023-12-12','23:59:22','P2','D1','O2','A1',2325),('2023-12-13','00:00:21','P1','D1','O3','A1',2275),('2023-12-13','00:01:12','P1','D1','O4','A1',2075),('2023-12-13','13:20:35','P1','D1','O5','A1',2200);
/*!40000 ALTER TABLE `opdbill` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patients`
--

DROP TABLE IF EXISTS `patients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patients` (
  `Patient_ID` varchar(10) NOT NULL,
  `First_Name` varchar(50) DEFAULT NULL,
  `Middle_Name` varchar(50) DEFAULT NULL,
  `Last_Name` varchar(50) DEFAULT NULL,
  `date_of_birth` varchar(20) DEFAULT NULL,
  `Gender` varchar(10) DEFAULT NULL,
  `Address` varchar(100) DEFAULT NULL,
  `Medical_History` varchar(100) DEFAULT NULL,
  `Email_Id` varchar(100) DEFAULT NULL,
  `Blood_Group` varchar(5) DEFAULT NULL,
  `Phone_Number` varchar(15) DEFAULT NULL,
  `Insurance_Id` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`Patient_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patients`
--

LOCK TABLES `patients` WRITE;
/*!40000 ALTER TABLE `patients` DISABLE KEYS */;
INSERT INTO `patients` VALUES ('P1','Williams','A','Doe','1990-05-15','Male','123 St. Elm St','None','utkarsh.tiwary2021@vitstudent.ac.in','O+','123-456-7890','I1'),('P2','Emily','B','Davis','1985-12-03','Female','456 Oak Ave','Allergies','jane@email.com','A-','987-654-3210','I2'),('P3','Sophia','','Miller','1978-08-20','Female','789 Maple Rd','Hypertension','robert@email.com','B+','555-123-4567','I3'),('P4','Pari','','Kankaria','2006-11-17','Female','ChinarPark','','kankaria.pari@gmail.com','B+','9831223388','I1233');
/*!40000 ALTER TABLE `patients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `prescription`
--

DROP TABLE IF EXISTS `prescription`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `prescription` (
  `Prescription_ID` varchar(10) NOT NULL,
  `Date` varchar(10) DEFAULT NULL,
  `Medications` varchar(100) DEFAULT NULL,
  `Instructions` varchar(100) DEFAULT NULL,
  `Dosage` varchar(20) DEFAULT NULL,
  `Doctor_ID` varchar(10) DEFAULT NULL,
  `Patient_ID` varchar(10) DEFAULT NULL,
  `Appointment_ID` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`Prescription_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prescription`
--

LOCK TABLES `prescription` WRITE;
/*!40000 ALTER TABLE `prescription` DISABLE KEYS */;
INSERT INTO `prescription` VALUES ('PS1','2023-10-18','Med1, Med2','Take with food','2 tablets daily','D1','P1','A1'),('PS2','2023-10-19','Med3, Med4','Take on an empty stomach','1 capsule daily','D2','P2','A2'),('PS3','2023-10-20','Med5','Take as needed','1 tablet as needed','D3','P3','A3');
/*!40000 ALTER TABLE `prescription` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roomexpenses`
--

DROP TABLE IF EXISTS `roomexpenses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roomexpenses` (
  `Room_Type` varchar(10) NOT NULL,
  `Room_Cost` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`Room_Type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roomexpenses`
--

LOCK TABLES `roomexpenses` WRITE;
/*!40000 ALTER TABLE `roomexpenses` DISABLE KEYS */;
INSERT INTO `roomexpenses` VALUES ('Double',100.00),('Single',150.00),('Suite',250.00);
/*!40000 ALTER TABLE `roomexpenses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `testexpenses`
--

DROP TABLE IF EXISTS `testexpenses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `testexpenses` (
  `Test` varchar(50) DEFAULT NULL,
  `Test_Cost` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `testexpenses`
--

LOCK TABLES `testexpenses` WRITE;
/*!40000 ALTER TABLE `testexpenses` DISABLE KEYS */;
INSERT INTO `testexpenses` VALUES ('Blood Test',50.00),('MRI',200.00),('X-Ray',75.00);
/*!40000 ALTER TABLE `testexpenses` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-12-13 23:35:01
