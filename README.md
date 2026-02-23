that the name of the project should be Teatreo
🎭 Teatreo - Recomendador de Obras de Teatro
Una aplicación web inteligente que recopila información de obras de teatro de múltiples fuentes, usa IA para analizar descripciones y aprende de las valoraciones de los usuarios para ofrecer recomendaciones personalizadas. ¡Perfecta para amantes del teatro que quieren descubrir su próxima obra favorita!

📋 Tabla de Contenidos
Características

Cómo Funciona

Tecnologías Utilizadas

Requisitos Previos

Instalación

Configuración

Configuración de la Base de Datos

Ejecutar la Aplicación

Estructura del Proyecto

Guía de Uso

Cómo Funciona el Motor de Recomendación

Personalización

Solución de Problemas

Contribuir

Licencia

✨ Características
Descubrimiento Automático de Obras: Extrae información de múltiples páginas de teatros

Análisis con IA: Usa Gemini AI de Google para extraer géneros, estados de ánimo y palabras clave de las descripciones

Recomendaciones Personalizadas: Aprende de tus valoraciones para sugerir obras que te encantarán

Filtrado por Estado de Ánimo: Encuentra obras según tu estado de ánimo (Comedia, Drama, Alegre, etc.)

Sistema de Valoración Interactivo: Valora las obras que has visto con estrellas y "me gusta"

Perfiles de Usuario: Crea una cuenta para guardar tus preferencias y obtener mejores recomendaciones

Filtrado Colaborativo: Descubre obras que gustaron a personas con gustos similares

Diseño Adaptable: Funciona en ordenadores y dispositivos móviles

🎯 Cómo Funciona
Recolección de Datos: El sistema extrae información de páginas de teatros diariamente

Análisis con IA: Cada descripción se envía a Gemini AI para extraer:

Género (Comedia, Drama, Musical, etc.)

Estado de ánimo (Alegre, Serio, Que invita a la reflexión, etc.)

Palabras clave (temas como "amor", "guerra", "familia")

Interacción del Usuario: Los usuarios exploran obras, las valoran y las marcan como vistas

Aprendizaje: El sistema construye un perfil de cada usuario basado en sus valoraciones

Recomendaciones: Los usuarios reciben sugerencias personalizadas según sus gustos

🛠 Tecnologías Utilizadas
Principal
Python 3.8+ - Lenguaje de programación principal

Flask - Framework web

SQLite3 - Base de datos

HTML5/CSS3/JavaScript - Frontend

Web Scraping
Requests - Obtener páginas web

BeautifulSoup4 - Analizar HTML y extraer datos

IA y Machine Learning
Google Gemini API - Análisis de obras

Motor de Recomendación Personalizado - Aprendizaje de preferencias

Herramientas de Desarrollo
pip - Gestión de paquetes

virtualenv/venv - Aislamiento de entorno

Git - Control de versiones

📦 Requisitos Previos
Antes de comenzar, asegúrate de tener instalado:

Python 3.8 o superior (Descargar)

Git (Descargar)

Un editor de código (VS Code, PyCharm o similar)

Clave de API de Google Gemini (Obtener aquí)

🚀 Instalación
Paso 1: Clonar el Repositorio
bash
git clone https://github.com/tuusuario/teatreo.git
cd teatreo
Paso 2: Crear un Entorno Virtual
bash
# En Windows
python -m venv venv
venv\Scripts\activate

# En macOS/Linux
python3 -m venv venv
source venv/bin/activate
Paso 3: Instalar Dependencias
bash
pip install -r requirements.txt
Crea un archivo requirements.txt con:

txt
Flask==2.3.3
requests==2.31.0
beautifulsoup4==4.12.2
google-generativeai==0.3.0
python-dotenv==1.0.0
⚙ Configuración
1. Variables de Entorno
Crea un archivo .env en la raíz del proyecto:

bash
# .env
SECRET_KEY=tu-clave-secreta-cambia-esto-en-produccion
GEMINI_API_KEY=tu-clave-de-gemini-aqui
DATABASE_PATH=database.db
2. Configurar Fuentes de Teatros
Edita config.py para añadir los teatros que quieres analizar:

python
# config.py
FUENTES_TEATROS = [
    {
        'nombre': 'Teatro A',
        'url': 'https://www.teatro-a.com/obras',
        'scraper': 'scraper_teatro_a'  # Tú crearás esta función
    },
    {
        'nombre': 'Teatro B',
        'url': 'https://www.teatro-b.com/cartelera',
        'scraper': 'scraper_teatro_b'
    }
]

FUENTES_CRITICAS = [
    {
        'nombre': 'Críticas Locales',
        'url': 'https://www.criticasteatro.com/resenas',
        'scraper': 'scraper_criticas'
    }
]
🗄 Configuración de la Base de Datos
Inicializar la Base de Datos
Ejecuta el script de configuración:

bash
python init_db.py
Esto crea database.db con las siguientes tablas:

sql
-- Tabla de obras: Almacena toda la información de las obras
CREATE TABLE obras (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    descripcion TEXT,
    teatro TEXT,
    fechas TEXT,
    genero TEXT,
    estado_animo TEXT,
    palabras_clave TEXT,
    url_fuente TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de usuarios: Gestiona las cuentas de usuario
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_usuario TEXT UNIQUE NOT NULL,
    contrasena TEXT NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de valoraciones: Almacena las valoraciones de los usuarios
CREATE TABLE valoraciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER,
    obra_id INTEGER,
    puntuacion INTEGER CHECK(puntuacion >= 1 AND puntuacion <= 5),
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
    FOREIGN KEY (obra_id) REFERENCES obras (id),
    UNIQUE(usuario_id, obra_id)
);

-- Tabla de obras vistas: Registra lo que han visto los usuarios
CREATE TABLE obras_vistas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER,
    obra_id INTEGER,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
    FOREIGN KEY (obra_id) REFERENCES obras (id),
    UNIQUE(usuario_id, obra_id)
);

-- Tabla de palabras clave de usuario: Almacena preferencias aprendidas
CREATE TABLE palabras_clave_usuario (
    usuario_id INTEGER,
    palabra_clave TEXT,
    puntuacion INTEGER DEFAULT 0,
    ultima_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
    PRIMARY KEY (usuario_id, palabra_clave)
);
🏃 Ejecutar la Aplicación
1. Iniciar el Servidor Flask
bash
python app.py
Verás:

text
 * Running on http://127.0.0.1:5000 (Presiona CTRL+C para salir)
2. Abrir el Navegador
Ve a: http://localhost:5000

3. Ejecutar el Scraper (Manual)
Para obtener nuevas obras:

bash
python ejecutar_scraper.py
4. Programar Scraping Automático (Opcional)
Añade al crontab (Linux/macOS) para scraping diario:

bash
# Ejecutar scraper cada día a las 2 AM
0 2 * * * cd /ruta/al/proyecto && /ruta/al/venv/bin/python ejecutar_scraper.py
Para Windows, usa el Programador de Tareas para ejecutar ejecutar_scraper.py diariamente.

📁 Estructura del Proyecto
text
teatreo/
├── app.py                      # Aplicación principal Flask
├── config.py                   # Configuración
├── init_db.py                  # Inicialización de base de datos
├── ejecutar_scraper.py         # Ejecutor manual de scraping
├── requirements.txt            # Dependencias de Python
├── .env                        # Variables de entorno (crear este)
├── .gitignore                  # Archivos ignorados por Git
│
├── scrapers/                   # Módulos de scraping
│   ├── __init__.py
│   ├── scraper_base.py         # Clase base para scrapers
│   ├── scraper_teatro_a.py     # Scraper específico para Teatro A
│   ├── scraper_teatro_b.py     # Scraper específico para Teatro B
│   └── scraper_criticas.py     # Scraper de críticas
│
├── modelos/                    # Modelos de base de datos
│   ├── __init__.py
│   ├── obra.py                 # Modelo de obra
│   ├── usuario.py              # Modelo de usuario
│   └── valoracion.py           # Modelo de valoración
│
├── motor_recomendacion.py      # Lógica de recomendación (ML)
│
├── utils/                      # Funciones utilitarias
│   ├── __init__.py
│   ├── analizador_llm.py       # Integración con Gemini API
│   └── ayudantes.py            # Funciones auxiliares
│
├── templates/                  # Plantillas HTML
│   ├── base.html               # Plantilla base
│   ├── index.html              # Página principal
│   ├── login.html              # Página de inicio de sesión
│   └── recomendaciones.html    # Página de recomendaciones
│
├── static/                      # Archivos estáticos
│   ├── estilo.css               # Estilos CSS
│   └── script.js                 # JavaScript
│
└── database.db                   # Base de datos SQLite (se crea al iniciar)
📖 Guía de Uso
Para Usuarios Regulares
Crear una Cuenta

Haz clic en "Iniciar Sesión" y luego en "Registrarse"

Elige un nombre de usuario y contraseña

Explorar Obras

La página principal muestra todas las obras actuales

Usa los filtros de estado de ánimo para encontrar lo que te interesa

Valorar Obras

Haz clic en las estrellas para puntuar (1-5)

Marca "Me gustó" para obras que disfrutaste

Marca como "Vista" cuando hayas asistido

Obtener Recomendaciones

Visita la página "Mis Recomendaciones"

Verás sugerencias personalizadas según tus gustos

Descubre lo que disfrutaron usuarios con gustos similares

Para Administradores
Añadir Nuevas Fuentes de Teatro

Crea un nuevo scraper en scrapers/

Añade la fuente en config.py

Ejecutar Scraping Manual

bash
python ejecutar_scraper.py --teatro TeatroA --forzar
Ver Base de Datos

bash
sqlite3 database.db
.tables
SELECT * FROM obras;
🧠 Cómo Funciona el Motor de Recomendación
Fase 1: Análisis de Contenido (LLM)
Cada obra es analizada por Gemini AI:

python
# Ejemplo de análisis
{
    "genero": "Drama",
    "estado_animo": "Profundo",
    "palabras_clave": ["familia", "identidad", "pérdida", "redención"]
}
Fase 2: Perfil de Usuario
Cuando un usuario valora positivamente una obra (4-5 estrellas), su perfil gana puntos:

text
Usuario: Ana
Perfil inicial: {}
Tras valorar "Hamlet" 5 estrellas → +1 para [venganza, realeza, locura, familia]
Tras valorar "Rey León" 4 estrellas → +1 para [familia, aventura, música, animales]
Perfil final: {familia:2, venganza:1, realeza:1, locura:1, aventura:1, música:1, animales:1}
Fase 3: Puntuación de Recomendaciones
Las nuevas obras se puntúan según coincidencias de palabras clave:

text
Nueva Obra "Macbeth": palabras [ambición, poder, realeza, locura]
Puntuación = realeza:1 + locura:1 = 2

Nueva Obra "Sonrisas y Lágrimas": palabras [familia, música, amor, guerra]
Puntuación = familia:2 + música:1 = 3
Fase 4: Filtrado Colaborativo
Encuentra usuarios con gustos similares y recomienda lo que les gustó:

sql
-- Encontrar usuarios a los que gustó lo que me gustó
SELECT obras.* FROM obras
JOIN valoraciones ON obras.id = valoraciones.obra_id
WHERE valoraciones.usuario_id IN (
    SELECT usuario_id FROM valoraciones 
    WHERE obra_id IN (mis_obras_gustadas) AND puntuacion >= 4
)
AND obras.id NOT IN (mis_obras_vistas)
GROUP BY obras.id
ORDER BY COUNT(*) DESC;
🎨 Personalización
Añadir Nuevos Teatros
Crea un nuevo archivo scraper:

python
# scrapers/scraper_teatro_c.py
from .scraper_base import ScraperBase

class ScraperTeatroC(ScraperBase):
    def __init__(self):
        super().__init__("Teatro C", "https://www.teatro-c.com")
    
    def obtener_obras(self):
        # Tu lógica de scraping aquí
        obras = []
        # ... extraer datos de obras
        return obras
Regístralo en config.py:

python
FUENTES_TEATROS.append({
    'nombre': 'Teatro C',
    'url': 'https://www.teatro-c.com',
    'scraper': ScraperTeatroC
})
Modificar el Análisis con IA
Edita utils/analizador_llm.py para cambiar lo que extrae la IA:

python
def analizar_obra(descripcion):
    prompt = f"""
    Analiza esta descripción de obra y devuelve un JSON con:
    - género (Comedia, Drama, Musical, etc.)
    - estado_ánimo (Alegre, Oscuro, Romántico, etc.)
    - palabras_clave (3-5 temas)
    - público_objetivo (Familiar, Adultos, Jóvenes)
    - impacto_emocional (Edificante, Triste, Inspirador)
    
    Descripción: {descripcion}
    """
    # ... resto del código
🔍 Solución de Problemas
Problemas Comunes y Soluciones
P: El scraper no encuentra obras

Verifica si la estructura del sitio web del teatro ha cambiado

Inspecciona la página web para encontrar nuevas clases CSS

Prueba con modo debug: python ejecutar_scraper.py --debug

P: La API de Gemini devuelve errores

Verifica tu clave de API en .env

Comprueba los límites de uso de la API

Asegúrate de tener conexión a internet

P: Errores de base de datos al iniciar

Elimina database.db y ejecuta python init_db.py de nuevo

Verifica los permisos de archivo en el directorio del proyecto

P: El CSS/JavaScript no carga

Limpia la caché del navegador

Comprueba que los archivos estáticos están en el directorio correcto

Verifica que Flask está en modo debug para desarrollo

P: No aparecen recomendaciones

Valora al menos 3 obras para construir un perfil

Comprueba que las obras tienen palabras clave (ejecuta el analizador si faltan)

Verifica que el usuario ha iniciado sesión

🤝 Contribuir
Haz un fork del repositorio

Crea una rama para tu función (git checkout -b feature/NuevaCaracteristica)

Haz commit de tus cambios (git commit -m 'Añadir nueva característica')

Sube los cambios (git push origin feature/NuevaCaracteristica)

Abre un Pull Request

Estándares de Código
Sigue PEP 8 para código Python

Usa nombres de variables descriptivos

Comenta la lógica compleja

Escribe pruebas para nuevas funcionalidades
