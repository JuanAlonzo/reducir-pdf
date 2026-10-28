import os
import shutil
import subprocess
import sys

# Configurar salida UTF-8 si la consola de Windows lo requiere
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, OSError, ValueError):
        pass

if getattr(sys, "frozen", False):
    # Si corre como ejecutable compilado:
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # Si corre como script .py normal:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INPUT_DIR = os.path.join(BASE_DIR, "pdfs_originales")
OUTPUT_DIR = os.path.join(BASE_DIR, "pdfs_comprimidos")

# Prioridad 1: Versión portable en 'gs_portable/bin/gswin64c.exe'
PORTABLE_GS = os.path.join(BASE_DIR, "gs_portable", "bin", "gswin64c.exe")
# Prioridad 2: Ruta estándar de instalación en el sistema
SYSTEM_GS_DEFAULT = r"C:\Program Files\gs\gs10.06.0\bin\gswin64c.exe"
# Prioridad 3: Variable de entorno PATH
SYSTEM_GS_PATH = shutil.which("gswin64c") or shutil.which("gswin32c")

if os.path.isfile(PORTABLE_GS):
    GS_EXECUTABLE = PORTABLE_GS
    print("[*] Modo: Ghostscript Portable detectado.")
elif os.path.isfile(SYSTEM_GS_DEFAULT):
    GS_EXECUTABLE = SYSTEM_GS_DEFAULT
    print("[*] Modo: Ghostscript instalado en el sistema detectado.")
elif SYSTEM_GS_PATH:
    GS_EXECUTABLE = SYSTEM_GS_PATH
    print("[*] Modo: Ghostscript encontrado en el PATH del sistema.")
else:
    print("[-] No se encontró Ghostscript en 'gs_portable/' ni en el sistema.")
    print("    Por favor coloca la carpeta 'gs_portable' junto al script o instala Ghostscript.")
    input("\nPresiona [Enter] para salir...")
    sys.exit(1)

os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

pdf_files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(".pdf")]

if not pdf_files:
    print(f"No se encontraron archivos PDF en la carpeta '{INPUT_DIR}'.")
else:
    print(f"Procesando {len(pdf_files)} archivo(s) con Ghostscript...")

    for filename in pdf_files:
        input_pdf = os.path.join(INPUT_DIR, filename)
        output_pdf = os.path.join(OUTPUT_DIR, filename)

        print(f"\n[+] Comprimiendo: {filename}")
        try:
            subprocess.run(
                [
                    GS_EXECUTABLE,
                    "-sDEVICE=pdfwrite",
                    "-dCompatibilityLevel=1.4",
                    "-dPDFSETTINGS=/ebook",
                    "-dNOPAUSE",
                    "-dQUIET",
                    "-dBATCH",
                    f"-sOutputFile={output_pdf}",
                    input_pdf,
                ],
                check=True,
            )

            orig_mb = os.path.getsize(input_pdf) / (1024 * 1024)
            comp_mb = os.path.getsize(output_pdf) / (1024 * 1024)
            reduction = (1 - (comp_mb / orig_mb)) * 100 if orig_mb > 0 else 0

            print(f"    Original:   {orig_mb:.2f} MB")
            print(f"    Comprimido: {comp_mb:.2f} MB ({reduction:.1f}% menor)")

        except (subprocess.CalledProcessError, OSError) as err:
            print(f"[-] Error al procesar {filename} con Ghostscript: {err}")

    print("\n✅ Compresión terminada exitosamente.")

input("\nPresiona [Enter] para cerrar...")
