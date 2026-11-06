# IDS-hibrido
Sistema de Detección de Intrusos híbrido inspirado en Snort, con análisis por reglas y heurísticas, métricas de precisión y dashboard web.
# IDS-hibrido
Sistema de Detección de Intrusos híbrido inspirado en Snort, con análisis por reglas y heurísticas, métricas de precisión y dashboard web.
# Hybrid-IDS: Network Intrusion Detection System

Un Sistema de Detección de Intrusiones en Red (NIDS) híbrido desarrollado en Python y Django. Combina detección determinista basada en firmas con análisis heurístico de comportamiento de tráfico en tiempo real, integrando un panel de visualización y gestión de alertas.

---

## Arquitectura del Sistema

El sistema implementa una arquitectura desacoplada en tres capas principales:

|  Capa de Captura (L3/L4)  |
              |     (Scapy Engine)        |
              +-------------+-------------+
                            |
                            v
              +---------------------------+
              |   Motor de Detección      |
              |     (Hybrid Engine)       |
              +-------------+-------------+
                            |
         +------------------+------------------+
         |                                     |
         v                                     v
+------------------------+           +------------------------+
| Capa de Firmas (Rules) |           | Capa Heurística        |
| - Escaneo de Puertos   |           | - Anomalías de Volumen |
| - Intentos F. Bruta    |           | - Ráfagas de Tráfico   |
+------------------------+           +------------------------+
|                                     |
+------------------+------------------+
|
v
+---------------------------+
|  Persistencia y Consola   |
|  (Django ORM + Dashboard) |
+---------------------------+

### 1. Ingestión de Paquetes (`Sniffer`)
* Captura tráfico en vivo a nivel de sockets crudos mediante `Scapy`.
* Extrae metadatos esenciales de capas 3 y 4 (IP origen, IP destino, puertos, flags TCP).
* Almacena telemetría normalizada en la entidad `Evento`.

### 2. Motor Analítico Híbrido (`Engine`)
* **Análisis por Firmas (`rules.py`):**
  * **Port Scan:** Detección de escaneo horizontal evaluando cardinalidad de puertos de destino únicos alcanzados por una misma IP de origen en ventanas temporales parametrizables ($T_{\text{window}}$).
  * **Brute Force:** Detección de intentos repetidos de autenticación fallida correlacionados por IP de origen.
* **Análisis Heurístico (`heuristics.py`):**
  * **Burst / Volume Anomaly:** Identificación de anomalías volumétricas calculando la tasa de paquetes por segundo (PPS) y picos de tráfico que superan umbrales basales dinámicos.

### 3. Gestión y Telemetría (`Dashboard`)
* Visualización en tiempo real de eventos y clasificación de incidentes por severidad (`LOW`, `MEDIUM`, `HIGH`, `CRITICAL`).
* Modificación dinámica de umbrales analíticos en caliente mediante el modelo `RuleConfig` sin reiniciar el servicio de captura.

---

## Requisitos Previos

* Python 3.10+
* Npcap (en entornos Windows) o `libpcap` (en entornos Linux/Unix).
* Privilegios de superusuario (`sudo` o Administrador) para el binding de sockets en modo promiscuo.

---

## Instalación y Puesta en Marcha

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/NahomiCast/IDS-hibrido.git](https://github.com/NahomiCast/IDS-hibrido.git)
   cd IDS-hibrido
========================================================================
1- Crear y activar el entorno virtual:
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux:
source venv/bin/activate

2- Instalar dependencias:
pip install -r requirements.txt

3- Configurar variables de entorno:
Copia el archivo de plantilla y define tus parámetros:
cp .env.example .env

4- Aplicar migraciones:

cd djIDS
python manage.py migrate

5- Iniciar el panel de control:
python manage.py runserver

6- Iniciar el sniffer de captura (en terminal con privilegios elevados):
python IDShibrido/Sniffer/capture.py

------------Parámetros de Detección Configurables (RuleConfig)----------------------------
Port Scanning->PORT_SCAN_THRESHOLD: Cantidad máxima de puertos distintos consultados en 60s.
Brute Force->BRUTE_FORCE_THRESHOLD: Fallos de autenticación consecutivos tolerados en 60s.
Traffic Anomaly->ANOMALY_THRESHOLD: Volumen máximo de paquetes tolerados por IP en 60s.
