#!/usr/bin/env python3
import sys
import os
import argparse
import subprocess
from fpdf import FPDF
from pdf2docx import Converter
from pypdf import PdfMerger, PdfReader, PdfWriter
from PIL import Image

# Configurar consola Windows para UTF-8
if sys.platform == "win32":
    try:
        subprocess.run(["chcp", "65001"], shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        print("Advertencia: No se pudo configurar la consola para UTF-8 en Windows.")

DESCRIPTION = """
SysToolKit – file_tools
Unifica conversiones y manipulaciones de archivos:
  * TXT a PDF  
  * DOCX a PDF  
  * PDF a DOCX  
  * Combinar o dividir PDFs  
  * Convertir imágenes  
  * Extraer texto de PDFs
"""

def txt2pdf(src, dst):
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        with open(src, 'r', encoding='utf-8') as f:
            for line in f:
                pdf.cell(0, 10, line.rstrip(), ln=1)
        pdf.output(dst)
        print(f"[OK] Archivo guardado: {dst}")
    except Exception as e:
        print(f"[ERROR] txt2pdf: {e}")

def docx2pdf(src):
    try:
        cmd = ["soffice", "--headless", "--convert-to", "pdf", src]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        print(f"[OK] PDF generado desde: {src}")
    except Exception as e:
        print(f"[ERROR] docx2pdf: {e}")

def pdf2docx(src, dst):
    try:
        cv = Converter(src)
        cv.convert(dst)
        cv.close()
        print(f"[OK] Archivo guardado: {dst}")
    except Exception as e:
        print(f"[ERROR] pdf2docx: {e}")

def mergepdf(output, inputs):
    try:
        merger = PdfMerger()
        for pdf in inputs:
            merger.append(pdf)
        merger.write(output)
        merger.close()
        print(f"[OK] PDF combinado: {output}")
    except Exception as e:
        print(f"[ERROR] mergepdf: {e}")

def splitpdf(src, pages, prefix):
    try:
        reader = PdfReader(src)
        indices = []
        for part in pages.split(','):
            if '-' in part:
                a, b = map(int, part.split('-'))
                indices.extend(range(a - 1, b))
            else:
                indices.append(int(part) - 1)
        writer = PdfWriter()
        for i in indices:
            writer.add_page(reader.pages[i])
        out = f"{prefix or src[:-4]}_split.pdf"
        with open(out, 'wb') as f:
            writer.write(f)
        print(f"[OK] PDF dividido: {out}")
    except Exception as e:
        print(f"[ERROR] splitpdf: {e}")

def imgconvert(src, dst):
    try:
        img = Image.open(src)
        img.save(dst)
        print(f"[OK] Imagen convertida: {dst}")
    except Exception as e:
        print(f"[ERROR] imgconvert: {e}")

def extracttxt(src, dst):
    try:
        text = []
        reader = PdfReader(src)
        for page in reader.pages:
            t = page.extract_text()
            if t:
                text.append(t)
        with open(dst, 'w', encoding='utf-8') as f:
            f.write("\n".join(text))
        print(f"[OK] Texto extraído a: {dst}")
    except Exception as e:
        print(f"[ERROR] extracttxt: {e}")

def main():
    parser = argparse.ArgumentParser(
        prog="file_tools",
        description=DESCRIPTION,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = parser.add_subparsers(dest="cmd", required=True, metavar="comando")

    p = sub.add_parser("txt2pdf", help="Convertir .txt a .pdf")
    p.add_argument("src", help="Archivo .txt de origen")
    p.add_argument("dst", help="Archivo .pdf de salida")

    p = sub.add_parser("docx2pdf", help="Convertir .docx a .pdf (requiere LibreOffice)")
    p.add_argument("src", help="Archivo .docx de origen")

    p = sub.add_parser("pdf2docx", help="Convertir .pdf a .docx")
    p.add_argument("src", help="Archivo .pdf de origen")
    p.add_argument("dst", help="Archivo .docx de salida")

    p = sub.add_parser("mergepdf", help="Unir múltiples PDFs en uno")
    p.add_argument("output", help="Archivo PDF de salida")
    p.add_argument("inputs", nargs='+', help="Archivos PDF a combinar")

    p = sub.add_parser("splitpdf", help="Dividir un PDF por rangos de páginas")
    p.add_argument("src", help="PDF de origen")
    p.add_argument("pages", help="Rangos de páginas, ejemplo: 1-3,5")
    p.add_argument("--prefix", help="Prefijo del archivo generado", default=None)

    p = sub.add_parser("imgconvert", help="Convertir una imagen a otro formato")
    p.add_argument("src", help="Imagen de origen")
    p.add_argument("dst", help="Archivo de imagen convertido")

    p = sub.add_parser("extracttxt", help="Extraer texto de un PDF a .txt")
    p.add_argument("src", help="PDF de origen")
    p.add_argument("dst", help="Archivo .txt de salida")

    args = parser.parse_args()

    # Mapa de comandos
    commands = {
        "txt2pdf": lambda: txt2pdf(args.src, args.dst),
        "docx2pdf": lambda: docx2pdf(args.src),
        "pdf2docx": lambda: pdf2docx(args.src, args.dst),
        "mergepdf": lambda: mergepdf(args.output, args.inputs),
        "splitpdf": lambda: splitpdf(args.src, args.pages, args.prefix),
        "imgconvert": lambda: imgconvert(args.src, args.dst),
        "extracttxt": lambda: extracttxt(args.src, args.dst),
    }

    try:
        commands[args.cmd]()
    except KeyError:
        print(f"[ERROR] Comando no reconocido: {args.cmd}")
    except Exception as e:
        print(f"[ERROR] Fallo al ejecutar el comando '{args.cmd}': {e}")

if __name__ == "__main__":
    main()
    input("\nPresiona Enter para volver al menú...")
