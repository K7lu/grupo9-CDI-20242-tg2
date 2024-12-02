/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19-11.4.4-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: sger_db
-- ------------------------------------------------------
-- Server version	11.4.4-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;

--
-- Table structure for table `alocacao`
--

DROP TABLE IF EXISTS `alocacao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alocacao` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Funcionario_ID` int(11) NOT NULL,
  `Projeto_ID` int(11) NOT NULL,
  `Data_Inicio` date NOT NULL,
  `Data_Termino` date DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `Funcionario_ID` (`Funcionario_ID`),
  KEY `Projeto_ID` (`Projeto_ID`),
  CONSTRAINT `alocacao_ibfk_1` FOREIGN KEY (`Funcionario_ID`) REFERENCES `funcionario` (`ID`),
  CONSTRAINT `alocacao_ibfk_2` FOREIGN KEY (`Projeto_ID`) REFERENCES `projeto` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alocacao`
--

LOCK TABLES `alocacao` WRITE;
/*!40000 ALTER TABLE `alocacao` DISABLE KEYS */;
/*!40000 ALTER TABLE `alocacao` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `alocacao_recursos`
--

DROP TABLE IF EXISTS `alocacao_recursos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alocacao_recursos` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Recurso_ID` int(11) NOT NULL,
  `Projeto_ID` int(11) NOT NULL,
  `Quantidade` int(11) NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `Recurso_ID` (`Recurso_ID`),
  KEY `Projeto_ID` (`Projeto_ID`),
  CONSTRAINT `alocacao_recursos_ibfk_1` FOREIGN KEY (`Recurso_ID`) REFERENCES `recurso` (`ID`),
  CONSTRAINT `alocacao_recursos_ibfk_2` FOREIGN KEY (`Projeto_ID`) REFERENCES `projeto` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alocacao_recursos`
--

LOCK TABLES `alocacao_recursos` WRITE;
/*!40000 ALTER TABLE `alocacao_recursos` DISABLE KEYS */;
/*!40000 ALTER TABLE `alocacao_recursos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cliente`
--

DROP TABLE IF EXISTS `cliente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cliente` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Nome` varchar(100) NOT NULL,
  `CNPJ` char(14) NOT NULL,
  `Endereco` varchar(255) DEFAULT NULL,
  `Telefone` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `CNPJ` (`CNPJ`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cliente`
--

LOCK TABLES `cliente` WRITE;
/*!40000 ALTER TABLE `cliente` DISABLE KEYS */;
/*!40000 ALTER TABLE `cliente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cliente_contato`
--

DROP TABLE IF EXISTS `cliente_contato`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cliente_contato` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Nome` varchar(100) NOT NULL,
  `Cargo` varchar(50) DEFAULT NULL,
  `Email` varchar(150) DEFAULT NULL,
  `Telefone` varchar(20) DEFAULT NULL,
  `Cliente_ID` int(11) NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `Cliente_ID` (`Cliente_ID`),
  CONSTRAINT `cliente_contato_ibfk_1` FOREIGN KEY (`Cliente_ID`) REFERENCES `cliente` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cliente_contato`
--

LOCK TABLES `cliente_contato` WRITE;
/*!40000 ALTER TABLE `cliente_contato` DISABLE KEYS */;
/*!40000 ALTER TABLE `cliente_contato` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `departamento`
--

DROP TABLE IF EXISTS `departamento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `departamento` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Nome` varchar(100) NOT NULL,
  `Responsavel_ID` int(11) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `Responsavel_ID` (`Responsavel_ID`),
  CONSTRAINT `departamento_ibfk_1` FOREIGN KEY (`Responsavel_ID`) REFERENCES `funcionario` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `departamento`
--

LOCK TABLES `departamento` WRITE;
/*!40000 ALTER TABLE `departamento` DISABLE KEYS */;
/*!40000 ALTER TABLE `departamento` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `efetivo`
--

DROP TABLE IF EXISTS `efetivo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `efetivo` (
  `ID` int(11) NOT NULL,
  `Salario` decimal(10,2) NOT NULL,
  `Beneficios` text DEFAULT NULL,
  PRIMARY KEY (`ID`),
  CONSTRAINT `efetivo_ibfk_1` FOREIGN KEY (`ID`) REFERENCES `funcionario` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `efetivo`
--

LOCK TABLES `efetivo` WRITE;
/*!40000 ALTER TABLE `efetivo` DISABLE KEYS */;
/*!40000 ALTER TABLE `efetivo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `funcionario`
--

DROP TABLE IF EXISTS `funcionario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `funcionario` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Nome` varchar(100) NOT NULL,
  `CPF` char(11) NOT NULL,
  `Data_Contratacao` date DEFAULT NULL,
  `Telefone` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `CPF` (`CPF`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `funcionario`
--

LOCK TABLES `funcionario` WRITE;
/*!40000 ALTER TABLE `funcionario` DISABLE KEYS */;
/*!40000 ALTER TABLE `funcionario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `projeto`
--

DROP TABLE IF EXISTS `projeto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `projeto` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Nome` varchar(100) NOT NULL,
  `Descricao` text DEFAULT NULL,
  `Data_Inicio` date DEFAULT NULL,
  `Data_Termino` date DEFAULT NULL,
  `Cliente_ID` int(11) NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `Cliente_ID` (`Cliente_ID`),
  CONSTRAINT `projeto_ibfk_1` FOREIGN KEY (`Cliente_ID`) REFERENCES `cliente` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `projeto`
--

LOCK TABLES `projeto` WRITE;
/*!40000 ALTER TABLE `projeto` DISABLE KEYS */;
/*!40000 ALTER TABLE `projeto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recurso`
--

DROP TABLE IF EXISTS `recurso`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `recurso` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Nome` varchar(100) NOT NULL,
  `Tipo` varchar(50) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recurso`
--

LOCK TABLES `recurso` WRITE;
/*!40000 ALTER TABLE `recurso` DISABLE KEYS */;
/*!40000 ALTER TABLE `recurso` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tarefa`
--

DROP TABLE IF EXISTS `tarefa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tarefa` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Descricao` text NOT NULL,
  `Data_Inicio` date DEFAULT NULL,
  `Data_Termino` date DEFAULT NULL,
  `Status` varchar(20) DEFAULT NULL,
  `Projeto_ID` int(11) NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `Projeto_ID` (`Projeto_ID`),
  CONSTRAINT `tarefa_ibfk_1` FOREIGN KEY (`Projeto_ID`) REFERENCES `projeto` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tarefa`
--

LOCK TABLES `tarefa` WRITE;
/*!40000 ALTER TABLE `tarefa` DISABLE KEYS */;
/*!40000 ALTER TABLE `tarefa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `terceirizado`
--

DROP TABLE IF EXISTS `terceirizado`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `terceirizado` (
  `ID` int(11) NOT NULL,
  `Empresa` varchar(100) NOT NULL,
  `Valor_Hora` decimal(10,2) NOT NULL,
  PRIMARY KEY (`ID`),
  CONSTRAINT `terceirizado_ibfk_1` FOREIGN KEY (`ID`) REFERENCES `funcionario` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `terceirizado`
--

LOCK TABLES `terceirizado` WRITE;
/*!40000 ALTER TABLE `terceirizado` DISABLE KEYS */;
/*!40000 ALTER TABLE `terceirizado` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2024-12-02 17:11:29
