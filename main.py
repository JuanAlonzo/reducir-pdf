import os
import sys

import pypdf
from pypdf.errors import PyPdfError

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
IMAGE_QUALITY = 60  # Calidad de compresión de imágenes (1 a 100). 60 ofrece buen balance tamaño/legibilidad

os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

pdf_files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(".pdf")]

if not pdf_files:
    print(f"No se encontraron archivos PDF en la carpeta '{INPUT_DIR}'.")
else:
    print(f"Procesando {len(pdf_files)} archivo(s)...")

    for filename in pdf_files:
        input_pdf = os.path.join(INPUT_DIR, filename)
        output_pdf = os.path.join(OUTPUT_DIR, filename)

        print(f"\n[+] Comprimiendo: {filename}")
        try:
            reader = pypdf.PdfReader(input_pdf)
            writer = pypdf.PdfWriter(clone_from=reader)

            # Recomprimir imágenes internas
            for page in writer.pages:
                for img in page.images:
                    if img.image is not None:
                        try:
                            img.replace(img.image, quality=IMAGE_QUALITY)
                        except (OSError, ValueError, TypeError):
                            # Si una imagen en específico no permite compresión, se conserva la original
                            pass

            with open(output_pdf, "wb") as out_file:
                writer.write(out_file)

            orig_mb = os.path.getsize(input_pdf) / (1024 * 1024)
            comp_mb = os.path.getsize(output_pdf) / (1024 * 1024)
            reduction = (1 - (comp_mb / orig_mb)) * 100 if orig_mb > 0 else 0

            print(f"    Original:   {orig_mb:.2f} MB")
            print(f"    Comprimido: {comp_mb:.2f} MB ({reduction:.1f}% menor)")

        except (PyPdfError, OSError, ValueError) as err:
            print(f"[-] Error al procesar {filename}: {err}")

    print("\n[OK] Compresion terminada exitosamente.")

input("\nPresiona [Enter] para cerrar...")
