===============================================================================
                    TEATREO - RECOMENDADOR DE OBRAS DE TEATRO
===============================================================================

Una aplicación web inteligente que recopila información de obras de teatro de
múltiples fuentes, usa IA para analizar descripciones y aprende de las
valoraciones de los usuarios para ofrecer recomendaciones personalizadas.

===============================================================================
                        TABLA DE CONTENIDOS
===============================================================================
1. CARACTERISTICAS
2. COMO FUNCIONA
3. TECNOLOGIAS UTILIZADAS
4. REQUISITOS PREVIOS
5. INSTALACION
6. CONFIGURACION
7. BASE DE DATOS
8. EJECUTAR LA APLICACION
9. ESTRUCTURA DEL PROYECTO
10. GUIA DE USO
11. MOTOR DE RECOMENDACION
12. PERSONALIZACION
13. SOLUCION DE PROBLEMAS
14. CONTRIBUIR
15. LICENCIA

===============================================================================
1. CARACTERISTICAS
===============================================================================

- Descubrimiento Automatico de Obras: Extrae informacion de multiples paginas
  de teatros diariamente.
- Analisis con IA: Usa Gemini AI de Google para extraer generos, estados de
  animo y palabras clave de las descripciones.
- Recomendaciones Personalizadas: Aprende de tus valoraciones para sugerir
  obras que te encantaran.
- Filtrado por Estado de Animo: Encuentra obras segun tu estado de animo
  (Comedia, Drama, Alegre, etc.).
- Sistema de Valoracion Interactivo: Valora las obras con estrellas y
  "me gusta".
- Perfiles de Usuario: Crea una cuenta para guardar tus preferencias.
- Filtrado Colaborativo: Descubre obras que gustaron a personas con gustos
  similares.
- Diseno Adaptable: Funciona en ordenadores y dispositivos moviles.

===============================================================================
2. COMO FUNCIONA
===============================================================================

1. RECOLECCION DE DATOS
   El sistema extrae informacion de paginas de teatros diariamente.

2. ANALISIS CON IA
   Cada descripcion se envia a Gemini AI para extraer:
   - Genero (Comedia, Drama, Musical, etc.)
   - Estado de animo (Alegre, Serio, Profundo, etc.)
   - Palabras clave (temas como "amor", "guerra", "familia")

3. INTERACCION DEL USUARIO
   Los usuarios exploran obras, las valoran y las marcan como vistas.

4. APRENDIZAJE
   El sistema construye un perfil de cada usuario basado en sus valoraciones.

5. RECOMENDACIONES
   Los usuarios reciben sugerencias personalizadas segun sus gustos.

===============================================================================
3. TECNOLOGIAS UTILIZADAS
===============================================================================

PRINCIPAL
---------
- Python 3.8+          : Lenguaje de programacion principal
- Flask                : Framework web
- SQLite3              : Base de datos
- HTML5/CSS3/JavaScript: Frontend

WEB SCRAPING
------------
- Requests             : Obtener paginas web
- BeautifulSoup4       : Analizar HTML y extraer datos

IA Y MACHINE LEARNING
---------------------
- Google Gemini API    : Analisis de obras
- Motor de Recomendacion Personalizado : Aprendizaje de preferencias

HERRAMIENTAS DE DESARROLLO
--------------------------
- pip                  : Gestion de paquetes
- virtualenv/venv      : Aislamiento de entorno
- Git                  : Control de versiones

===============================================================================
4. REQUISITOS PREVIOS
===============================================================================

- Python 3.8 o superior (https://www.python.org/downloads/)
- Git (https://git-scm.com/downloads)
- Un editor de codigo (VS Code, PyCharm)
- Clave de API de Google Gemini (https://aistudio.google.com/)

===============================================================================
5. INSTALACION
===============================================================================

PASO 1: Clonar el Repositorio
------------------------------
$ git clone https://github.com/tuusuario/teatreo.git
$ cd teatreo

PASO 2: Crear un Entorno Virtual
---------------------------------
# En Windows
$ python -m venv venv
$ venv\Scripts\activate

# En macOS/Linux
$ python3 -m venv venv
$ source venv/bin/activate

PASO 3: Instalar Dependencias
------------------------------
$ pip install flask requests beautifulsoup4 google-generativeai python-dotenv

O crea un archivo requirements.txt con:
-------------------------------------------------------------------------------
Flask==2.3.3
requests==2.31.0
beautifulsoup4==4.12.2
google-generativeai==0.3.0
python-dotenv==1.0.0
-------------------------------------------------------------------------------

Y ejecuta:
$ pip install -r requirements.txt

===============================================================================
6. CONFIGURACION
===============================================================================

PASO 1: Variables de Entorno
-----------------------------
Crea un archivo .env en la raiz del proyecto:

-------------------------------------------------------------------------------
# .env
SECRET_KEY=tu-clave-secreta-cambia-esto-en-produccion
GEMINI_API_KEY=tu-clave-de-gemini-aqui
DATABASE_PATH=database.db
-------------------------------------------------------------------------------

PASO 2: Configurar Fuentes de Teatros
--------------------------------------
Crea config.py:

-------------------------------------------------------------------------------
# config.py
FUENTES_TEATROS = [
    {
        'nombre': 'Teatro A',
        'url': 'https://www.teatro-a.com/obras',
        'scraper': 'scraper_teatro_a'
    },
    {
        'nombre': 'Teatro B',
        'url': 'https://www.teatro-b.com/cartelera',
        'scraper': 'scraper_teatro_b'
    }
]

FUENTES_CRITICAS = [
    {
        'nombre': 'Criticas Locales',
        'url': 'https://www.criticasteatro.com/resenas',
        'scraper': 'scraper_criticas'
    }
]
-------------------------------------------------------------------------------

===============================================================================
7. BASE DE DATOS
===============================================================================

Crea init_db.py:

-------------------------------------------------------------------------------
import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Tabla de obras
cursor.execute('''
    CREATE TABLE IF NOT EXISTS obras (
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
    )
''')

# Tabla de usuarios
cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_usuario TEXT UNIQUE NOT NULL,
        contrasena TEXT NOT NULL,
        fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

# Tabla de valoraciones
cursor.execute('''
    CREATE TABLE IF NOT EXISTS valoraciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER,
        obra_id INTEGER,
        puntuacion INTEGER CHECK(puntuacion >= 1 AND puntuacion <= 5),
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
        FOREIGN KEY (obra_id) REFERENCES obras (id),
        UNIQUE(usuario_id, obra_id)
    )
''')

# Tabla de obras vistas
cursor.execute('''
    CREATE TABLE IF NOT EXISTS obras_vistas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER,
        obra_id INTEGER,
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
        FOREIGN KEY (obra_id) REFERENCES obras (id),
        UNIQUE(usuario_id, obra_id)
    )
''')

# Tabla de aprendizaje
cursor.execute('''
    CREATE TABLE IF NOT EXISTS palabras_clave_usuario (
        usuario_id INTEGER,
        palabra_clave TEXT,
        puntuacion INTEGER DEFAULT 0,
        ultima_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
        PRIMARY KEY (usuario_id, palabra_clave)
    )
''')

conn.commit()
conn.close()
print("Base de datos creada exitosamente!")
-------------------------------------------------------------------------------

Ejecutar:
$ python init_db.py

===============================================================================
8. EJECUTAR LA APLICACION
===============================================================================

PASO 1: Iniciar el Servidor
----------------------------
Crea app.py basico:

-------------------------------------------------------------------------------
from flask import Flask, render_template
import sqlite3

app = Flask(__name__)
app.secret_key = 'tu-clave-secreta'

def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db()
    obras = conn.execute('SELECT * FROM obras').fetchall()
    conn.close()
    return render_template('index.html', obras=obras)

if __name__ == '__main__':
    app.run(debug=True)
-------------------------------------------------------------------------------

PASO 2: Iniciar
----------------
$ python app.py

Veras: * Running on http://127.0.0.1:5000

PASO 3: Abrir Navegador
------------------------
Ve a: http://localhost:5000

PASO 4: Scraping Manual
------------------------
Crea ejecutar_scraper.py y ejecuta:
$ python ejecutar_scraper.py

PASO 5: Scraping Automatico (Opcional)
---------------------------------------
# Linux/Mac (crontab)
0 2 * * * cd /ruta/teatreo && venv/bin/python ejecutar_scraper.py

# Windows: Usar Programador de Tareas

===============================================================================
9. ESTRUCTURA DEL PROYECTO
===============================================================================

teatreo/
|
├── app.py                      # Aplicacion principal Flask
├── config.py                   # Configuracion
├── init_db.py                  # Inicializar base de datos
├── ejecutar_scraper.py         # Ejecutar scraping manual
├── motor_recomendacion.py      # Logica de recomendacion (ML)
├── requirements.txt            # Dependencias
├── .env                        # Variables de entorno
├── .gitignore                  # Archivos ignorados por Git
|
├── scrapers/                    # Modulos de scraping
│   ├── __init__.py
│   ├── scraper_base.py         # Clase base para scrapers
│   ├── scraper_teatro_a.py     # Scraper Teatro A
│   ├── scraper_teatro_b.py     # Scraper Teatro B
│   └── scraper_criticas.py     # Scraper de criticas
|
├── modelos/                     # Modelos de base de datos
│   ├── __init__.py
│   ├── obra.py
│   ├── usuario.py
│   └── valoracion.py
|
├── utils/                       # Funciones utilitarias
│   ├── __init__.py
│   ├── analizador_llm.py       # Integracion con Gemini
│   └── ayudantes.py            # Funciones auxiliares
|
├── templates/                   # Plantillas HTML
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   └── recomendaciones.html
|
├── static/                      # Archivos estaticos
│   ├── estilo.css
│   └── script.js
|
└── database.db                  # Base de datos SQLite

===============================================================================
10. GUIA DE USO
===============================================================================

PARA USUARIOS REGULARES
-----------------------

1. Crear una Cuenta
   - Haz clic en "Iniciar Sesion" y luego en "Registrarse"
   - Elige nombre de usuario y contrasena

2. Explorar Obras
   - La pagina principal muestra todas las obras actuales
   - Usa filtros de estado de animo (Comedia, Drama, etc.)

3. Valorar Obras
   - Haz clic en estrellas para puntuar (1-5)
   - Marca "Me gusto" para obras que disfrutaste
   - Marca "Vista" cuando hayas asistido

4. Obtener Recomendaciones
   - Visita "Mis Recomendaciones"
   - Ve sugerencias personalizadas segun tus gustos
   - Descubre que disfrutaron usuarios similares

PARA ADMINISTRADORES
--------------------

1. Anadir Nuevos Teatros
   - Crea nuevo scraper en scrapers/
   - Anade fuente en config.py

2. Ejecutar Scraping Manual
   $ python ejecutar_scraper.py --teatro TeatroA --forzar

3. Ver Base de Datos
   $ sqlite3 database.db
   sqlite> .tables
   sqlite> SELECT * FROM obras;

===============================================================================
11. MOTOR DE RECOMENDACION
===============================================================================

FASE 1: Analisis de Contenido (LLM)
------------------------------------
Crea utils/analizador_llm.py:

-------------------------------------------------------------------------------
import google.generativeai as genai
import json
import os

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-pro')

def analizar_obra(titulo, descripcion, criticas):
    prompt = f"""
    Analiza esta obra de teatro y devuelve un JSON con:
    - genero: (Comedia, Drama, Musical, Tragedia, Experimental, Familiar, Suspenso)
    - estado_animo: (Alegre, Serio, Profundo, Oscuro, Romantico, Divertido)
    - palabras_clave: lista de 3-5 temas (amor, guerra, identidad, etc.)
    
    Titulo: {titulo}
    Descripcion: {descripcion}
    Criticas: {criticas}
    
    Devuelve SOLO el JSON valido.
    """
    
    response = model.generate_content(prompt)
    try:
        return json.loads(response.text)
    except:
        return {"genero": "Desconocido", "estado_animo": "Desconocido", "palabras_clave": []}
-------------------------------------------------------------------------------

FASE 2: Motor de Recomendacion
-------------------------------
Crea motor_recomendacion.py:

-------------------------------------------------------------------------------
import sqlite3

class MotorRecomendacion:
    def __init__(self, db_path='database.db'):
        self.db_path = db_path
    
    def actualizar_perfil(self, usuario_id, obra_id, puntuacion):
        """APRENDIZAJE: Actualiza perfil del usuario segun valoracion"""
        conn = sqlite3.connect(self.db_path)
        
        obra = conn.execute('SELECT palabras_clave FROM obras WHERE id = ?', 
                           (obra_id,)).fetchone()
        
        if obra and obra[0]:
            palabras = [p.strip() for p in obra[0].split(',')]
            
            # Si puntuacion es buena (4-5), suma puntos
            # Si es mala (1-2), resta puntos
            cambio = 0
            if puntuacion >= 4:
                cambio = 1
            elif puntuacion <= 2:
                cambio = -1
            
            if cambio != 0:
                for palabra in palabras:
                    existe = conn.execute('''
                        SELECT puntuacion FROM palabras_clave_usuario 
                        WHERE usuario_id = ? AND palabra_clave = ?
                    ''', (usuario_id, palabra)).fetchone()
                    
                    if existe:
                        conn.execute('''
                            UPDATE palabras_clave_usuario 
                            SET puntuacion = puntuacion + ?, 
                                ultima_actualizacion = CURRENT_TIMESTAMP
                            WHERE usuario_id = ? AND palabra_clave = ?
                        ''', (cambio, usuario_id, palabra))
                    else:
                        conn.execute('''
                            INSERT INTO palabras_clave_usuario (usuario_id, palabra_clave, puntuacion)
                            VALUES (?, ?, ?)
                        ''', (usuario_id, palabra, cambio))
                    
                    conn.commit()
        conn.close()
    
    def obtener_recomendaciones(self, usuario_id, limite=5):
        """Genera recomendaciones personalizadas"""
        conn = sqlite3.connect(self.db_path)
        
        # Obtener preferencias del usuario
        preferencias = conn.execute('''
            SELECT palabra_clave, puntuacion FROM palabras_clave_usuario 
            WHERE usuario_id = ? AND puntuacion > 0
            ORDER BY puntuacion DESC
        ''', (usuario_id,)).fetchall()
        
        # Si no hay preferencias, recomendar obras al azar
        if not preferencias:
            recomendaciones = conn.execute('''
                SELECT * FROM obras 
                WHERE id NOT IN (
                    SELECT obra_id FROM obras_vistas WHERE usuario_id = ?
                )
                ORDER BY RANDOM()
                LIMIT ?
            ''', (usuario_id, limite)).fetchall()
            conn.close()
            return recomendaciones
        
        # Obtener obras no vistas
        obras_no_vistas = conn.execute('''
            SELECT * FROM obras 
            WHERE id NOT IN (
                SELECT obra_id FROM obras_vistas WHERE usuario_id = ?
            )
        ''', (usuario_id,)).fetchall()
        
        # Puntuar cada obra
        obras_puntuadas = []
        for obra in obras_no_vistas:
            if obra[6]:  # palabras_clave
                palabras_obra = [p.strip() for p in obra[6].split(',')]
                puntuacion = 0
                
                for p in preferencias:
                    if p[0] in palabras_obra:
                        puntuacion += p[1]
                
                obras_puntuadas.append((puntuacion, obra))
        
        # Ordenar y devolver mejores
        obras_puntuadas.sort(reverse=True, key=lambda x: x[0])
        conn.close()
        return [obra for puntuacion, obra in obras_puntuadas[:limite]]
-------------------------------------------------------------------------------

EJEMPLO DE APRENDIZAJE
----------------------

ESCENARIO: Usuario "Ana"

1. Ana ve "Hamlet" y da 5 estrellas
   - Palabras clave: venganza, realeza, locura, familia
   - Perfil: {venganza:1, realeza:1, locura:1, familia:1}

2. Ana ve "Rey Leon" y da 4 estrellas
   - Palabras clave: familia, aventura, musica, animales
   - Perfil: {familia:2, venganza:1, realeza:1, locura:1, aventura:1, musica:1}

3. Nueva obra "Macbeth"
   - Palabras: ambicion, poder, realeza, locura
   - Puntuacion: realeza(1) + locura(1) = 2

4. Nueva obra "Sonrisas y Lagrimas"
   - Palabras: familia, musica, amor, guerra
   - Puntuacion: familia(2) + musica(1) = 3
   - RESULTADO: Se recomienda "Sonrisas y Lagrimas" primero

===============================================================================
12. PERSONALIZACION
===============================================================================

ANADIR NUEVO TEATRO
-------------------

1. Crear scraper: scrapers/scraper_teatro_c.py
-------------------------------------------------------------------------------
from .scraper_base import ScraperBase

class ScraperTeatroC(ScraperBase):
    def __init__(self):
        super().__init__("Teatro C", "https://www.teatro-c.com")
    
    def obtener_obras(self):
        import requests
        from bs4 import BeautifulSoup
        
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        obras = []
        for obra in soup.find_all('div', class_='obra'):
            titulo = obra.find('h2').text
            descripcion = obra.find('p', class_='desc').text
            fechas = obra.find('span', class_='fechas').text
            
            obras.append({
                'titulo': titulo,
                'descripcion': descripcion,
                'teatro': self.nombre,
                'fechas': fechas
            })
        
        return obras
-------------------------------------------------------------------------------

2. Registrar en config.py
-------------------------------------------------------------------------------
FUENTES_TEATROS.append({
    'nombre': 'Teatro C',
    'url': 'https://www.teatro-c.com',
    'scraper': ScraperTeatroC
})
-------------------------------------------------------------------------------

MODIFICAR ANALISIS IA
---------------------

Editar utils/analizador_llm.py:

-------------------------------------------------------------------------------
def analizar_obra(descripcion):
    prompt = f"""
    Analiza esta descripcion y devuelve JSON con:
    - genero: (Comedia, Drama, Musical, etc.)
    - estado_animo: (Alegre, Oscuro, Romantico, etc.)
    - palabras_clave: (3-5 temas)
    - publico_objetivo: (Familiar, Adultos, Jovenes)
    - impacto_emocional: (Edificante, Triste, Inspirador)
    - epoca: (Clasica, Contemporanea, Futurista)
    
    Descripcion: {descripcion}
    """
    # ... resto del codigo
-------------------------------------------------------------------------------

===============================================================================
13. SOLUCION DE PROBLEMAS
===============================================================================

PROBLEMA: El scraper no encuentra obras
SOLUCION:
- Verifica si cambio la estructura del sitio web
- Inspecciona la pagina para encontrar nuevas clases CSS
- Ejecuta con modo debug: python ejecutar_scraper.py --debug
- Prueba con: print(soup.prettify()) para ver el HTML

PROBLEMA: Error de Gemini API
SOLUCION:
- Verifica tu API key en .env
- Comprueba limites de uso (60 requests/minuto gratis)
- Asegura conexion a internet
- Prueba: curl -H "Content-Type: application/json" ...

PROBLEMA: Error de base de datos
SOLUCION:
- Elimina database.db y ejecuta python init_db.py
- Verifica permisos de escritura
- sqlite3 database.db "PRAGMA integrity_check;"

PROBLEMA: No aparecen recomendaciones
SOLUCION:
- Valora al menos 3 obras para crear perfil
- Verifica que las obras tienen palabras clave
- Asegura que el usuario ha iniciado sesion
- Revisa tabla palabras_clave_usuario

PROBLEMA: CSS/JavaScript no carga
SOLUCION:
- Limpia cache del navegador (Ctrl+F5)
- Verifica archivos en static/
- Revisa consola del navegador (F12)
- Asegura que Flask corre en modo debug

PROBLEMA: Error "Internal Server Error"
SOLUCION:
- Revisa terminal para ver el error exacto
- Verifica que todas las tablas existen
- Comprueba que las rutas Flask estan bien definidas

===============================================================================
14. CONTRIBUIR
===============================================================================

1. Haz fork del repositorio
2. Crea rama: git checkout -b feature/NuevaCaracteristica
3. Haz commit: git commit -m 'Anadir nueva caracteristica'
4. Sube cambios: git push origin feature/NuevaCaracteristica
5. Abre Pull Request

ESTANDARES DE CODIGO
--------------------
- Sigue PEP 8 para Python
- Usa nombres de variables descriptivos en espanol
- Comenta logica compleja
- Escribe docstrings para funciones
- Prueba antes de hacer pull request

EJEMPLO DE CODIGO LIMPIO
------------------------
-------------------------------------------------------------------------------
def obtener_obras_por_estado_animo(estado_animo, limite=10):
    """
    Obtiene obras filtradas por estado de animo.
    
    Args:
        estado_animo (str): Estado de animo deseado
        limite (int): Numero maximo de obras a retornar
    
    Returns:
        list: Lista de obras que coinciden
    """
    conn = sqlite3.connect('database.db')
    obras = conn.execute('''
        SELECT * FROM obras 
        WHERE estado_animo = ? 
        LIMIT ?
    ''', (estado_animo, limite)).fetchall()
    conn.close()
    return obras
-------------------------------------------------------------------------------

===============================================================================
15. LICENCIA
===============================================================================

MIT License

Copyright (c) 2024 Teatreo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

===============================================================================
                    CONTACTO Y SOPORTE
===============================================================================

- GitHub: https://github.com/tuusuario/teatreo
- Issues: https://github.com/tuusuario/teatreo/issues
- Email: tu@email.com

===============================================================================
              ¡CADA VALORACION MEJORA TUS RECOMENDACIONES!
===============================================================================
