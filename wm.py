from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io
import os

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
    can.drawString(10, 100, "Bu belge Canias ERP tarafından onaylanmıştır.")
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

# Ana işlem
input_pdf_path = "Source/1.pdf"  # Girdi olarak kullanılacak PDF dosyası yolu
output_pdf_path = "Destination/n1.pdf"  # Çıktı olarak kaydedilecek damgalı PDF dosyası yolu
stamp = create_stamp()
add_stamp_to_pdf(input_pdf_path, output_pdf_path, stamp)

