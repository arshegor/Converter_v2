import json
import sys
from fpdf import FPDF
from PIL import Image
import numpy as np


def read_json(path):
    with open(path, 'r') as file:
        return json.load(file)


def create_image(filename, json_file):
    data = np.array(json_file["image"])
    img = Image.fromarray(data.astype('uint8'))
    img.save(filename)


def create_table(json_file, pdf):
    h = 6
    pdf.set_font("DejaVu", size=10)
    for k, v in json_file["meta"].items():
        pdf.set_fill_color(230, 230, 230)
        pdf.cell(42, h, k, border=1, fill=True)
        pdf.set_fill_color(0, 0, 0)
        pdf.cell(148, h, v, border=1)
        pdf.ln(h)
    pdf.set_font("DejaVu", size=12)


def create_pdf(pdf_name, filename, json_file):
    pdf = FPDF()
    pdf.add_page()

    pdf.add_font(family='DejaVu', style='', fname='DejaVuSans-ExtraLight.ttf', uni=True)
    pdf.set_font('DejaVu', '', 12)

    pdf.image("Mtuci_logo.png", x=9, y=1, w=26.5)

    pdf.line(0, 27, 210, 27)
    pdf.cell(200, 10, txt="", ln=1, align="L")
    pdf.cell(200, 10, txt="", ln=1, align="L")
    pdf.set_text_color(43, 43, 43)

    pdf.cell(200, 10, txt="Информация:", ln=1, align="L")
    create_table(json_file, pdf)
    pdf.line(0, 84, 210, 84)

    pdf.set_y(88)
    pdf.cell(200, 10, txt="Результат обработки искусственным интеллектом:", ln=1, align="L")
    pdf.set_font("DejaVu", size=10)
    pdf.cell(200, 10, txt="Общий процент поражения легких: " + json_file["ai_result"] + "%", ln=1, align="L")
    pdf.cell(200, 10, txt=" ", ln=1, align="L")
    pdf.set_font("DejaVu", size=12)
    pdf.line(0, 112, 210, 112)

    pdf.set_y(116)
    pdf.cell(200, 10, txt="Изображения:", ln=1, align="L")
    pdf.image(filename, x=10, y=130, w=90)

    pdf.line(0, 280, 210, 280)

    pdf.output(pdf_name)


def create_filename(json_file):
    name_for_pdf = json_file["meta"]["PatientsName"] + json_file["meta"]["PatientsBirthDate"]
    return name_for_pdf.replace(" ", "_").replace(".", "_")


def main(path):
    filename = "image.png"
    json_file = read_json(path)

    pdf_name = create_filename(json_file) + ".pdf"

    create_image(filename, json_file)

    create_pdf(pdf_name, filename, json_file)


if __name__ == '__main__':
    main(sys.argv[1])
