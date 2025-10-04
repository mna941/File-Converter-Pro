from flask import Flask, request, redirect, url_for, render_template, flash, send_from_directory
from werkzeug.utils import secure_filename
import os
import uuid

# Conversion libraries
from pdf2docx import Converter
import fitz  # PyMuPDF
from docx import Document
from fpdf import FPDF
from lxml import etree

# -------------------------------
# Conversion Functions
# -------------------------------

import os, subprocess

def pdf_to_docx(pdf_path, out_folder, uid):
    docx_path = os.path.join(out_folder, f"{uid}.docx")
    # Use LibreOffice (soffice) for conversion to preserve formatting
    subprocess.run([
        "soffice", "--headless", "--convert-to", "docx", "--outdir", out_folder, pdf_path
    ], check=True)
    return docx_path


# Word to PDF
def word_to_pdf(docx_path, out_folder, uid):
    from docx2pdf import convert as docx2pdf_convert
    pdf_path = os.path.join(out_folder, f'{uid}.pdf')
    docx2pdf_convert(docx_path, pdf_path)
    return pdf_path

# PDF to Text
def pdf_to_text(pdf_path, out_folder, uid):
    text_path = os.path.join(out_folder, f'{uid}.txt')
    doc = fitz.open(pdf_path)
    text = ''
    for page in doc:
        text += page.get_text()
    with open(text_path, 'w', encoding='utf-8') as f:
        f.write(text)
    return text_path

# Text to PDF
def text_to_pdf(txt_path, out_folder, uid):
    pdf_path = os.path.join(out_folder, f'{uid}.pdf')
    with open(txt_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', size=12)
    for line in lines:
        pdf.cell(200, 10, txt=line.strip(), ln=1)
    pdf.output(pdf_path)
    return pdf_path

# PDF to HTML
def pdf_to_html(pdf_path, out_folder, uid):
    html_path = os.path.join(out_folder, f'{uid}.html')
    doc = fitz.open(pdf_path)
    html = ''
    for page in doc:
        html += page.get_text('html')
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    return html_path

# HTML to PDF
def html_to_pdf(html_path, out_folder, uid):
    from xhtml2pdf import pisa
    pdf_path = os.path.join(out_folder, f'{uid}.pdf')
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    with open(pdf_path, 'wb') as f:
        pisa.CreatePDF(html, dest=f)
    return pdf_path

# DOC to DOCX
def doc_to_docx(doc_path, out_folder, uid):
    docx_path = os.path.join(out_folder, f'{uid}.docx')
    with open(doc_path, 'rb') as src, open(docx_path, 'wb') as dst:
        dst.write(src.read())
    return docx_path

# DOCX to DOC
def docx_to_doc(docx_path, out_folder, uid):
    doc_path = os.path.join(out_folder, f'{uid}.doc')
    with open(docx_path, 'rb') as src, open(doc_path, 'wb') as dst:
        dst.write(src.read())
    return doc_path

# ODT to PDF
def odt_to_pdf(odt_path, out_folder, uid):
    pdf_path = os.path.join(out_folder, f'{uid}.pdf')
    with open(odt_path, 'rb') as src, open(pdf_path, 'wb') as dst:
        dst.write(src.read())
    return pdf_path

# PDF to ODT
def pdf_to_odt(pdf_path, out_folder, uid):
    odt_path = os.path.join(out_folder, f'{uid}.odt')
    with open(pdf_path, 'rb') as src, open(odt_path, 'wb') as dst:
        dst.write(src.read())
    return odt_path