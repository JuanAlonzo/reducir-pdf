import os
import subprocess
import sys

# Configurar salida UTF-8 si la consola de Windows lo requiere
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, OSError, ValueError):
        pass

INPUT_DIR = "pdfs_originales"
OUTPUT_DIR = "pdfs_comprimidos"
GS_EXECUTABLE = r"C:\Program Files\gs\gs10.06.0\bin\gswin64c.exe"

os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

if not os.path.isfile(GS_EXECUTABLE):
    print(f"[-] No se encontró el ejecutable de Ghostscript en: {GS_EXECUTABLE}")
    print("    Por favor actualiza la variable 'GS_EXECUTABLE' con la ruta correcta de tu sistema.")
    sys.exit(1)

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
