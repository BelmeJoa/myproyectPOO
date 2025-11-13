-- database/script_creacion.sql
-- ESTE SCRIPT DEBE EJECUTARSE UNA VEZ EN MYSQL

CREATE DATABASE IF NOT EXISTS db_kinesiologia;
USE db_kinesiologia;

-- Tabla base para Herencia
CREATE TABLE persona (
    id_persona INT AUTO_INCREMENT PRIMARY KEY,
    dni VARCHAR(10) UNIQUE NOT NULL,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    fecha_nacimiento DATE
);

-- Tabla Paciente (Hereda atributos de persona - Relación 1-1)
CREATE TABLE paciente (
    id_paciente INT PRIMARY KEY,
    historia_clinica VARCHAR(20) UNIQUE,
    obra_social VARCHAR(50),
    FOREIGN KEY (id_paciente) REFERENCES persona(id_persona)
);

-- Tabla Usuario (Kinesiologo)
CREATE TABLE usuario (
    id_usuario INT PRIMARY KEY,
    matricula VARCHAR(20) UNIQUE NOT NULL,
    rol VARCHAR(50),
    FOREIGN KEY (id_usuario) REFERENCES persona(id_persona)
);

-- Tabla Turno/Sesion
CREATE TABLE turno (
    id_turno INT AUTO_INCREMENT PRIMARY KEY,
    id_paciente INT NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    tratamiento TEXT,
    FOREIGN KEY (id_paciente) REFERENCES paciente(id_paciente) ON DELETE CASCADE
);