from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import red
import io
import os
from datetime import datetime

# Çalışma dizinini yazdır
print("Çalışma Dizini:", os.getcwd())

# Dosyaların varlığını kontrol et
def check_file_existence(file_path):
    if not os.path.exists(file_path):
        print(f"Hata: '{file_path}' dosyası bulunamadı.")
        return False
    return True

# Damga oluşturma
def create_stamp():
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont("Helvetica-Bold", 12)  # Kalın font ayarı
    can.setFillColor(red)  # Kırmızı renk ayarı
    can.drawString(10, 20, "Bu belge Canias ERP tarafindan onaylanmistir.")  # Sayfanın altına yaz
    can.save()
    packet.seek(0)
    return packet

# PDF'ye damga ekleme
def add_stamp_to_pdf(input_pdf, output_pdf, stamp_stream):
    if not check_file_existence(input_pdf):
        return  # Eğer girdi PDF dosyası yoksa işlemi durdur

    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    # Her sayfaya damgayı ekle
    for page in reader.pages:
        overlay = PdfReader(stamp_stream)
        page.merge_page(overlay.pages[0])
        writer.add_page(page)

    # Sonuç PDF'ini yaz
    with open(output_pdf, "wb") as f_out:
        writer.write(f_out)

# Klasördeki tüm PDF'leri işle
def process_all_pdfs(source_dir, destination_dir):
    current_time = datetime.now().strftime("%d.%m.%Y %H.%M.%S")
    for filename in os.listdir(source_dir):
        if filename.endswith(".pdf"):
            input_pdf_path = os.path.join(source_dir, filename)
            new_filename = filename.replace(".pdf", f" {current_time}_damgali.pdf")
            output_pdf_path = os.path.join(destination_dir, new_filename)
            stamp = create_stamp()
            add_stamp_to_pdf(input_pdf_path, output_pdf_path, stamp)

# Ana işlem
source_directory = "Source"  # Kaynak klasör yolu
destination_directory = "Destination"  # Hedef klasör yolu
process_all_pdfs(source_directory, destination_directory)


