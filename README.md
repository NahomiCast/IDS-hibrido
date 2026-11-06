## ENGLISH
# Hybrid-NIDS: Network Intrusion Detection System

A lightweight, hybrid Network Intrusion Detection System (NIDS) built with Python, Scapy, and Django. The system combines deterministic signature-based detection with traffic volume heuristic analysis to identify network reconnaissance and volumetric anomalies in real time, featuring an interactive management dashboard.

---

## Architecture Overview

The system implements a decoupled three-tier architecture:
                       
              | Packet Capture Tier (L3/4)|
              |       (Scapy Engine)      |
              +-------------+-------------+
                            |
                            v
              +---------------------------+
              |   Hybrid Detection Engine |
              |    (rules.py + heuristics)|
              +-------------+-------------+
                            |
         +------------------+------------------+
         |                                     |
         v                                     v
    +------------------------+           +------------------------+
    | Signature Engine       |           | Heuristic Engine       |
    | - Horizontal Port Scan |           | - Traffic Burst Rate   |
    | - Brute Force Correl.  |           | - Volume Anomaly (PPS) |
    +------------------------+           +------------------------+
                |                                     |
                +------------------+------------------+
                                   |
                                   v
                     +---------------------------+
                     | Persistence & Web Consoles|
                     | (PostgreSQL / Django ORM) |
                     +---------------------------+
### 1. Ingestion Tier (`capture.py`)
* Leverages raw socket capture via `Scapy` operating in promiscuous mode.
* Extracts core L3/L4 metadata (Source IP, Destination Port, Protocol, TCP flags).
* Persists telemetry events into the database entity `Evento`.

### 2. Hybrid Detection Engine (`engine.py`)
* **Signature-Based Inspection (`rules.py`):**
  * **Port Scanning:** Detects horizontal sweeps by tracking the cardinality of unique destination ports targeted by a single source IP across a configurable sliding time window ($T_{\text{window}}$).
  * **Brute Force:** Flags repeated authentication failures correlated by source address over sliding intervals.
* **Heuristic Anomaly Detection (`heuristics.py`):**
  * **Volumetric Bursts:** Identifies sudden traffic spikes by calculating the packet-per-second (PPS) rate, triggering warnings when baseline activity thresholds are exceeded.

### 3. Management & Telemetry Dashboard (`djIDS`)
* Real-time monitoring console displaying captured network events and categorized security alerts (`LOW`, `MEDIUM`, `HIGH`, `CRITICAL`).
* Dynamic parameter tuning: detection thresholds can be adjusted on the fly through the `RuleConfig` model without restarting the packet sniffing daemon.

---

## Prerequisites

* Python 3.10+
* Npcap (Windows) or `libpcap` (Linux / macOS)
* PostgreSQL database service running locally or remotely
* Root / Administrator privileges (required for raw socket binding)

---

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/NahomiCast/IDS-hibrido.git](https://github.com/NahomiCast/IDS-hibrido.git)
   cd IDS-hibrido

1- Create and activate a virtual environment:
  # Linux / macOS:
  python3 -m venv venv
  source venv/bin/activate

  # Windows (PowerShell):
  python -m venv venv
  .\venv\Scripts\Activate.ps1

2- Install dependencies:
  pip install -r requirements.txt

3- Configure environment variables:
Copy the example environment template and configure your local credentials:
  # Linux / macOS:
cp .env.example .env

# Windows (PowerShell):
Copy-Item .env.example .env

Edit .env to include your database credentials, Django secret key, and the network interface name (e.g., Wi-Fi, eth0).

4- Apply database migrations:
cd djIDS
python manage.py migrate

5- Create an administrative user:
python manage.py createsuperuser

Running the Application
1- Start the Django Dashboard:
# From inside the djIDS directory:
python manage.py runserver
Access the web console at http://127.0.0.1:8000/.

2- Launch the Packet Capture Daemon (requires elevated privileges):
# Windows (Run PowerShell as Administrator):
python IDShibrido/Sniffer/capture.py

# Linux:
sudo $(which python) IDShibrido/Sniffer/capture.py

Detection Threshold Configuration (RuleConfig)
Thresholds are stored in the database and can be modified at runtime via the web interface:

Port Scanning->PORT_SCAN_THRESHOLD: Maximum distinct destination ports targeted within a 60-second window.
Brute Force->BRUTE_FORCE_THRESHOLD: Consecutive failed login events permitted per source IP within 60s.
Traffic Anomaly->ANOMALY_THRESHOLD: Maximum packet volume tolerated from a single source address within 60s.
Security & Operational Notes
Credential Management: Secrets, database passwords, and environment configurations are decoupled from source control using environment variables (.env).

Packet Drop Mitigation: High-volume network scanning can strain database I/O. For high-throughput environments, consider deploying an event queue (e.g., Redis / Celery) or bulk-inserting packet batches.


## Español
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
