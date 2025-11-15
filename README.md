<div align="center">

# 🛠️ Windows Error Diagnostic with AI 

*Diagnóstico inteligente y reparación automática para Windows usando inteligencia artificial*

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Windows](https://img.shields.io/badge/Platform-Windows%2010%2B-success)](https://www.microsoft.com/windows)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3.5%2B-orange)](https://openai.com/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

</div>

## 🌟 Resumen del Proyecto

Este proyecto, Windows Error Diagnostic with AI (WED), es una herramienta de diagnóstico y reparación inteligente diseñada para sistemas operativos Windows (10/11).

El objetivo principal es aprovechar la Inteligencia Artificial (IA) para analizar de forma proactiva y automática los logs de eventos de Windows, diagnosticar la causa de los errores del sistema y aplicar soluciones automatizadas a problemas comunes. La herramienta ofrece una interfaz de usuario moderna (construida con CustomTkinter) y proporciona reportes detallados del análisis y la reparación.

## ✨ Características Principales

- **🔍 Análisis Inteligente**: Usa IA para analizar logs de eventos de Windows y diagnosticar problemas
- **🛠️ Reparación Automática**: Ejecuta soluciones automáticas para problemas comunes del sistema
- **📊 Interfaz Moderna**: UI intuitiva y fácil de usar construida con CustomTkinter
- **🔐 Configuración Sencilla**: Configura tu API key de OpenAI directamente desde la aplicación
- **📝 Reportes Detallados**: Genera análisis completos con soluciones paso a paso
- **⚡ Tiempo Real**: Progreso en tiempo real durante el análisis y reparación
- **🛡️ Seguro**: Solo lectura y reparaciones estándar de Windows

## 🛠️ Tecnologías Utilizadas

| Tecnología | Propósito |
| :--- | :--- |
| **Python** | Lenguaje de programación principal. |
| **CustomTkinter** | Creación de la Interfaz Gráfica de Usuario (GUI) moderna. |
| **`os` & `glob`** | Manejo del sistema de archivos, directorios y obtención de metadatos (fechas de modificación). |
| **json** | Gestión del archivo de configuración, incluyendo la clave API. |
| **Manejo de Logs** | Lectura, filtrado y análisis de los registros de eventos de Windows. |

## 💡 Información General y Propósito

| Detalle | Descripción |
| :--- | :--- |
| **Creador** | LSCF |
| **Propósito** | Mejorar y optimizar las instalaciones semi-automáticas. |
| **Origen** | Idea original de LSCF, con soporte en el desarrollo por Inteligencia Artificial (IA). |


## 🚀 Instalación y Uso

### Prerrequisitos
- Python 3.8 o superior
- Windows 10/11
- Conexión a internet (Esencial para la comunicación con la API de IA)
- Permisos de administrador (Recomendado, ya que el script accede a logs de sistema y ejecuta reparaciones)
- Clave API de OpenAI
  
---
## 1. Instalación de Dependencias

1.  **Clona el repositorio**
    ```bash
    git clone https://github.com/LSCF84/WED.git
    cd WED
    ```
2.  **Instala dependencias**
    ```bash
    pip install -r requirements.txt
    ```
    ### 2. Ejecución
Dado que solo utiliza librerías ya estan instaladas.

1.  Descarga o clona el archivo `main.py` en tu máquina.
2.  Ejecuta el *script* desde tu terminal:

    ```bash
    python main.py
    ```
    
## 👨‍💻 Autor

**LSCF**

## ⚙️ Instalación y Dependencias

Para ejecutar este proyecto, necesitas Python 3.x

## 🤝 ¿Quieres contribuir?

¡Claro! Abre un Issue o un Pull Request. Usa la plantilla al crear un Issue.

---

⭐️ Si te sirvió, ¡dale una estrella al repositorio!
