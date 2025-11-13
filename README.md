 Sistema de Gestión para Consultorio Kinesiológico
Autor: Belmetiuk Joaquin

Descripción del Proyecto

Este proyecto es una aplicación de escritorio diseñada para gestionar un consultorio de kinesiología. Permite llevar un control detallado de los pacientes, su historial de atenciones y el registro de cobros. La aplicación incluye un sistema de recordatorios de citas y está preparada para una futura expansión, como la integración de un gimnasio.


├── data/                  # Capa de Conexión (Configuración de MySQL)
│   └── database.py        # Clase que maneja la conexión y consultas preparadas
│
├── database/              # Scripts SQL
│   └── script_creacion.sql # Script para crear la BD db_kinesiologia y tablas
│
├── models/                # Clases de Dominio (POO)
│   ├── persona.py         # Clase base con atributos comunes (Herencia)
│   ├── paciente.py        # Clase que hereda de Persona
│   └── turno.py           # Clase para las sesiones/turnos
│
├── services/              # Lógica de Negocio (Controlador)
│   └── gestion_kinesiologia.py # Contiene el CRUD completo y lógica de reportes
│
├── gui/                   # Interfaz de Usuario (Vista)
│   └── menu.py            # Menus y logica de interacción con el usuario (consola)
│
├── utils/                 # Funciones auxiliares
│   └── validador.py       # Validaciones de DNI, fecha y edad
│
├── docs/                  # Documentación Obligatoria
│   ├── manual_usuario.pdf # Manual de usuario
│   └── diagrama_uml.png   # Diagrama de Clases UML
│
├── main.py                # Punto de entrada principal
└── requirements.txt       # Dependencias de Python

 Configuración e Instalación. RequisitosPython 3.11+Servidor de Base de Datos MySQL (versión 8.0+)Git (para control de versiones)2. Instalación de Dependencias: Clona el repositorio e instala el conector de MySQL:Bashgit clone https://github.com/BelmeJoa/myproyectPOO.git ProyectoKinesiologia