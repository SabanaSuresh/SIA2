-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : sam. 10 mai 2025 à 16:26
-- Version du serveur : 9.1.0
-- Version de PHP : 8.3.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `airblio`
--

-- --------------------------------------------------------

--
-- Structure de la table `demandes`
--

DROP TABLE IF EXISTS `demandes`;
CREATE TABLE IF NOT EXISTS `demandes` (
  `numero_demande` varchar(20) NOT NULL,
  `numero_client` varchar(100) DEFAULT NULL,
  `intitule` varchar(255) DEFAULT NULL,
  `date_demande` date DEFAULT NULL,
  `importance` varchar(20) DEFAULT NULL,
  `description` text,
  `heure_demande` time DEFAULT NULL,
  `entreprise` varchar(100) DEFAULT NULL,
  `site` varchar(100) DEFAULT NULL,
  `contact` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`numero_demande`)
) ENGINE=MyISAM AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `demandes`
--

INSERT INTO `demandes` (`numero_demande`, `numero_client`, `intitule`, `date_demande`, `importance`, `description`, `heure_demande`, `entreprise`, `site`, `contact`) VALUES
('D682714', '52041', 'Panne électrique suite à une tempête', '2025-03-28', 'red', 'Bonjour,\r\n\r\nSuite à une tempête violente, notre site industriel subit une panne électrique totale, impactant nos opérations critiques. Cette panne met en danger la continuité de service et la sécurité des équipements sensibles.\r\n\r\nDétails techniques :\r\n\r\nPoste de transformation endommagé\r\n\r\nDisjoncteurs hors service\r\n\r\nBesoin urgent d’un générateur mobile et de câbles haute tension\r\n\r\nMerci\r\nCordialement', '08:37:00', 'ÉnergieMarineTech', 'Port de Lorient, Quai de la Perrière, 56100 Lorient', 'Sophie Leroux – +33 6 78 54 23 10'),
('D682713', '43707', 'Suivi de commande pour le nouvel équipement', '2025-03-20', 'green', 'Bonjour,\r\n\r\nNous n’avons toujours pas reçu le matériel sonar commandé le mois dernier. Cette livraison est essentielle pour équiper notre prochaine mission en mer prévue sous peu.\r\n\r\nDétails du matériel attendu :\r\n\r\nSonar latéral modèle STX-300\r\n\r\nAccessoires de montage et alimentation\r\n\r\nMerci de nous confirmer le statut d’expédition au plus vite.\r\nCordialement', '10:03:00', 'SubOcean Equipements', '5 rue du Port, 35400 Saint-Malo', 'Clara Vasseur – +33 7 88 12 46 83'),
('D682712', '34567', 'Maintenance du système de communication', '2025-03-15', 'orange', 'Bonjour,\r\n\r\nDepuis quelques jours, nous observons des interférences et des pertes de signal dans notre système de communication sous-marine.\r\n\r\nProblèmes détectés :\r\n\r\nCâbles coaxiaux probablement oxydés\r\n\r\nSignal radio intermittent entre les modules\r\n\r\nNécessité de tester et remplacer certaines unités\r\n\r\nMerci de planifier une intervention rapidement.\r\nCordialement', '15:10:00', 'ComNavTech', 'Base navale, Bâtiment B3, 29200 Brest', 'Ingrid Dumas – +33 7 61 45 98 22'),
('D682711', '23456', 'Installation de nouveaux capteurs', '2025-03-12', 'orange', 'Bonjour,\r\n\r\nComme convenu, nous souhaitons procéder à l’installation de capteurs environnementaux sur notre station côtière.\r\n\r\nIntervention prévue :\r\n\r\nFixation de 3 capteurs thermiques\r\n\r\nBranchement sur l’interface réseau locale\r\n\r\nCalibration initiale sur le logiciel de supervision\r\n\r\nMerci de nous envoyer une équipe disponible cette semaine.\r\nCordialement', '10:07:00', 'Nautilus', '12 rue Neptune, 13007 Marseille', 'Mathieu Girard – +33 6 45 89 33 77'),
('D682710', '67890', 'Mise à jour logicielle pour le ROV', '2025-03-05', 'green', 'Hi,\r\n\r\nWe need urgent assistance for a software update on our ROV control station. The current firmware causes stability issues and prevents full range maneuvering.\r\n\r\nTechnical requirements:\r\n\r\nDeploy version 3.4.2 of the ROV firmware\r\n\r\nValidate thruster calibration\r\n\r\nEnsure backup config is retained after upgrade\r\n\r\nPlease dispatch a certified technician ASAP.\r\nBest regards', '11:25:00', 'BelSea Engineering', 'Quai de la Digue, Anvers 2000, Belgique', 'Émile De Smet – +32 472 89 01 55'),
('D682709', '54321', 'Formation des techniciens sur le matériel', '2025-02-25', 'green', 'Hello,\r\n\r\nWe have received the new batch of diving equipment and would like to arrange a training session for our technicians.\r\n\r\nExpected training topics:\r\n\r\nSafe use of dry diving suits\r\n\r\nDeployment of underwater thrusters\r\n\r\nBasic maintenance and troubleshooting\r\n\r\nPlease let us know your available dates.\r\nBest regards;', '08:46:00', 'AquaForm Iberia', 'Calle del Puerto 22, 11006 Cádiz, Espagne', 'Julián Morel – +34 612 73 85 19');

-- --------------------------------------------------------

--
-- Structure de la table `equipements`
--

DROP TABLE IF EXISTS `equipements`;
CREATE TABLE IF NOT EXISTS `equipements` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(255) DEFAULT NULL,
  `quantite_disponible` int DEFAULT NULL,
  `quantite_totale` int DEFAULT NULL,
  `statut` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `equipements`
--

INSERT INTO `equipements` (`id`, `nom`, `quantite_disponible`, `quantite_totale`, `statut`) VALUES
(1, 'Caisson Hyperbare', 30, 50, 'Disponible'),
(2, 'Sonar de Plongée', 20, 40, 'Maintenance'),
(3, 'Combinaison de Plongée Étanche', 30, 40, 'Disponible'),
(4, 'Propulseur Sous–Marin', 7, 10, 'Maintenance'),
(5, 'Robot Sous–Marin (ROV)', 6, 10, 'Disponible'),
(6, 'Équipement de Soudure Sous–Marine', 11, 20, 'Défectueux');

-- --------------------------------------------------------

--
-- Structure de la table `interventions`
--

DROP TABLE IF EXISTS `interventions`;
CREATE TABLE IF NOT EXISTS `interventions` (
  `id` int NOT NULL,
  `reference_demande` varchar(100) DEFAULT NULL,
  `intitule` varchar(255) DEFAULT NULL,
  `date_intervention` date DEFAULT NULL,
  `lieu` varchar(255) DEFAULT NULL,
  `statut` varchar(50) DEFAULT NULL,
  `importance` varchar(50) DEFAULT NULL,
  `equipement` varchar(255) DEFAULT NULL,
  `membre` varchar(255) DEFAULT NULL,
  `description` text,
  `cout` varchar(50) DEFAULT NULL,
  `commentaire` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `interventions`
--

INSERT INTO `interventions` (`id`, `reference_demande`, `intitule`, `date_intervention`, `lieu`, `statut`, `importance`, `equipement`, `membre`, `description`, `cout`, `commentaire`) VALUES
(1783051, 'D682712', 'Remise à niveau du système de transmission sous-marin', '2024-03-18', '13 Rue de la Porte, 29200 Brest\r\n', 'A venir', 'Moyenne', 'Unité radio étanche, Module de transmission, Antenne marine renforcée', 'C. Durand (Ingénieur Systèmes), L. Bianchi (Technicien Réseau)', 'Mise à jour des composants critiques du système de transmission afin de garantir une communication stable. Les anciens modules ont été inspectés, certains remplacés, puis un calibrage complet a été effectué. L opération est planifiée pour coïncider avec une fenêtre météo favorable.', '27500', ''),
(1783052, 'D682713', 'Installation du nouvel équipement de plongée', '2024-03-22', '5 rue du Port, 35400 Saint-Malo', 'Terminée', 'Faible', 'Caisson Hyperbare, Sonar de Plongée, Combinaison de Plongée Étanche', 'M. Lefèvre (Chef de mission), C. Marin (Technicien Plongée), J. Dubois (Assistant technique)', 'Remplacement complet du système de communication défaillant. L équipe a procédé au démontage des anciens équipements, à l installation du nouveau matériel, puis à une série de tests de connectivité sous-marine. Les performances ont été validées sur site avec l accord du responsable client.\r\n', '38500', NULL),
(1783050, 'D682712', 'Vérification des câbles de communication sous-marins', '2024-03-18', '13 Rue de la Porte, 29200 Brest\r\n', 'En cours', 'Moyenne', 'Analyseur de câbles, Testeur de continuité, Module de pression sous-marine', 'A. Morel (Chef de projet), N. Roger (Plongeur technique)', 'Inspection visuelle et électronique des câbles principaux reliant les points de surveillance. Aucun dommage majeur n a été constaté. Des tests d étanchéité et de signal ont été réalisés pour garantir l intégrité du réseau. Intervention menée en coordination avec le service technique local.', '19800', 'Résultats conformes aux attentes. Quelques micro-f'),
(1783049, NULL, 'Maintenance préventive annuelle des équipements de plongée', '2024-03-16', 'Packhusplatsen 1, 411 13 Göteborg', 'Terminée', 'Faible', 'Station de recharge, Valves de secours, Kit d inspection optique', 'S. Bergström (Responsable site), K. Holm (Technicien maintenance)', 'Contrôle de sécurité de tous les équipements de plongée conformément aux normes en vigueur. Nettoyage, tests de pression, remplacement des pièces usées. Rapport transmis à la direction technique pour archivage. Aucune anomalie critique signalée.', '22400', NULL);

-- --------------------------------------------------------

--
-- Structure de la table `projets`
--

DROP TABLE IF EXISTS `projets`;
CREATE TABLE IF NOT EXISTS `projets` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nom_projet` varchar(255) DEFAULT NULL,
  `lieu` varchar(255) DEFAULT NULL,
  `latitude` float DEFAULT NULL,
  `longitude` float DEFAULT NULL,
  `date_projet` date DEFAULT NULL,
  `statut` enum('en cours','prévu') DEFAULT NULL,
  `membres` text,
  `equipements` text,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `projets`
--

INSERT INTO `projets` (`id`, `nom_projet`, `lieu`, `latitude`, `longitude`, `date_projet`, `statut`, `membres`, `equipements`) VALUES
(1, 'Inspection des câbles sous-marins', 'Paris', 48.8566, 2.3522, '2025-05-10', 'en cours', 'Paul, Carla', 'ROV, Sonar'),
(2, 'Maintenance de sonar', 'Londres', 51.5074, -0.1278, '2025-05-20', 'prévu', 'Laure, Antoine', 'Sonar'),
(3, 'Déploiement de ROV', 'New York', 40.7128, -74.006, '2025-06-15', 'en cours', 'Youssouf, Dicia', 'ROV'),
(4, 'Surveillance environnementale', 'Sydney', -33.8688, 151.209, '2025-07-01', 'prévu', 'Rony, Drexy', 'Capteurs, Logiciel de surveillance'),
(5, 'Installation capteurs océaniques', 'Tokyo', 35.6762, 139.65, '2025-08-01', 'en cours', 'Nargisse, Sofiane', 'Capteurs océaniques');

-- --------------------------------------------------------

--
-- Structure de la table `utilisateurs`
--

DROP TABLE IF EXISTS `utilisateurs`;
CREATE TABLE IF NOT EXISTS `utilisateurs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(191) NOT NULL,
  `mot_de_passe` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `utilisateurs`
--

INSERT INTO `utilisateurs` (`id`, `email`, `mot_de_passe`) VALUES
(1, 'responsable@airblio.com', 'mdp'),
(2, 'a@b.com', 'a');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
