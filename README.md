# Reductor y Compresor de PDFs en Lote 📄⚡

Herramienta en Python para procesar y reducir el tamaño de archivos PDF de forma masiva (en lote). Ofrece dos alternativas de compresión según las necesidades del usuario: una solución nativa en Python y otra basada en Ghostscript.

---

## 📌 Resumen del Proyecto

Este repositorio contiene dos scripts diseñados para procesar todos los archivos PDF situados en una carpeta de entrada (`pdfs_originales/`) y generar versiones optimizadas y de menor peso en una carpeta de salida (`pdfs_comprimidos/`).

### 1. `main.py` (Solución en Python con `pypdf` y `Pillow`)
- **Cómo funciona**: Analiza cada página del documento, extrae las imágenes incrustadas y las recomprime ajustando su calidad (`IMAGE_QUALITY = 60` por defecto).
- **Ventaja**: No necesita instalar programas adicionales en el sistema operativo; basta con las librerías de Python.
- **Métricas**: Muestra en consola el tamaño original, el tamaño final y el porcentaje de reducción por cada archivo procesado.

### 2. `main_ghostscript.py` (Solución con Ghostscript)
- **Cómo funciona**: Invoca el motor de Ghostscript (`gswin64c.exe`) utilizando el perfil de compresión `/ebook` (balance ideal entre compresión y legibilidad a 150 DPI).
- **Ventaja**: Es un estándar de la industria muy potente para optimizar fuentes, imágenes y vectores en documentos complejos.

---

## 📋 Requerimientos

### 🐍 Entorno Python
- **Python 3.8 o superior**

### 📦 Librerías de Python (`requirements.txt`)
Para ejecutar `main.py`:
- **`pypdf`** ($\ge$ 5.0.0): Lectura, clonado y escritura de documentos PDF.
- **`Pillow`** ($\ge$ 10.0.0): Motor de procesamiento y compresión de imágenes incrustadas en el PDF.

### 🛠️ Software Externo (Opcional, solo para `main_ghostscript.py`)
- **[Ghostscript](https://www.ghostscript.com/download.html)** instalado en el sistema.
  - En Windows, la ruta por defecto en el script apunta a `C:\Program Files\gs\gs10.06.0\bin\gswin64c.exe` (ajusta la ruta según la versión que tengas instalada).

---

## 🚀 Instalación y Uso

### 1. Clonar el repositorio
```bash
git clone https://github.com/TU_USUARIO/TU_REPOSITORIO.git
cd TU_REPOSITORIO
```

### 2. (Opcional pero recomendado) Crear un entorno virtual
```bash
# En Windows:
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Preparar los archivos
Coloca los archivos `.pdf` que deseas comprimir dentro de la carpeta:
```
pdfs_originales/
```

### 5. Ejecutar la compresión

- **Opción A — Usando `main.py` (Recomendada y portable):**
  ```bash
  python main.py
  ```

- **Opción B — Usando `main_ghostscript.py`:**
  *(Asegúrate de que la ruta de Ghostscript en el script coincida con la de tu sistema)*
  ```bash
  python main_ghostscript.py
  ```

Los archivos resultantes se guardarán automáticamente en la carpeta:
```
pdfs_comprimidos/
```

---

## 📂 Estructura del Repositorio

```text
├── pdfs_originales/       # Carpeta donde colocas los PDFs a procesar
├── pdfs_comprimidos/      # Carpeta donde se guardan los PDFs comprimidos
├── main.py                # Script de compresión nativo en Python (pypdf + Pillow)
├── main_ghostscript.py    # Script de compresión mediante Ghostscript
├── requirements.txt       # Lista de dependencias de Python
└── README.md              # Documentación del proyecto
```

---

## ⚙️ Parámetros de Configuración

### En `main.py`:
- `IMAGE_QUALITY`: Nivel de compresión de imágenes de 1 a 100 (por defecto `60`).
  - Valores entre `50` y `70` suelen dar el mejor balance entre reducción de peso y nitidez de lectura.

### En `main_ghostscript.py`:
- `-dPDFSETTINGS`: Permite ajustar el preset de calidad:
  - `/screen`: Máxima compresión, menor calidad (72 DPI).
  - `/ebook`: Balance medio (150 DPI) — *valor por defecto*.
  - `/printer`: Alta calidad para impresión (300 DPI).
  - `/prepress`: Máxima calidad para preimpresión (300 DPI con preservación de color).

---

## 📄 Licencia

Este proyecto se distribuye bajo la licencia MIT. Eres libre de usarlo, modificarlo y distribuirlo.
