from django.http import HttpResponse
from wsgiref.util import FileWrapper
# import win32com.client
from pathlib import Path
from PIL import Image
import openpyxl
from openpyxl.drawing.spreadsheet_drawing import AbsoluteAnchor
from openpyxl.drawing.spreadsheet_drawing import OneCellAnchor, AnchorMarker
from openpyxl.drawing.xdr import XDRPoint2D, XDRPositiveSize2D
from openpyxl.utils.units import pixels_to_EMU, cm_to_EMU
# import pandas as pd
# import pdfkit

# pywin32
# import win32com.client as win32
# import pythoncom
import tempfile
import shutil

def fp_excel_works_pywin32(**kwargs):
    pass
#     excel = kwargs.get('excel')
#     fp=kwargs.get('fp')
#     parent_path = kwargs.get('parent_path')
        
    
#     sh = fp.Sheets(1)
#     sh.Cells(40,1).Value   = 'This is a simple test'
#     print('trying to save')
#     fp.Save()
#     print('saved')
#     fp.Close()
#     print('closed')
#     return fp

def fp_excel_works(**kwargs):
    wb = kwargs['wb']
    sh = kwargs['sh']
    data_dict = kwargs['data_dict']

    sh['G2'] = data_dict.get('product_name_fr')
    sh['G3'] = data_dict.get('product_name_ru')
    sh['A11'] = data_dict.get('product_desc_fr')
    sh['M11'] = data_dict.get('product_desc_ru')
    sh['E29'] = data_dict.get('protocol')
    sh['E31'] = data_dict.get('observation')
    sh['R45'] = data_dict.get('number')
    sh['W45'] = data_dict.get('index')
    sh['D6'] = data_dict.get('provider')
    sh['K6'] = data_dict.get('origin')
    sh['T6'] = data_dict.get('manufactured_in')
    sh['G4'] = data_dict.get('project')
    sh['D8'] = data_dict.get('location')
    sh['E45'] = data_dict.get('phase')
    sh['H45'] = data_dict.get('lot')
    sh['D4'] = data_dict.get('lot')
    sh['J45'] = data_dict.get('fp_type')

    if kwargs['image_path']:
        pimg = Image.open(kwargs['image_path'])
        imgo = openpyxl.drawing.image.Image(pimg)

        c2e = cm_to_EMU
        p2e = pixels_to_EMU
        
        h, w = imgo.height, imgo.width
        h = 245
        if w > 400:
            w=400
        offset_number_horizontal = (420 - w)/2/18
        offset_number_vertical = (260 - h)/2
        print('offset_number_horizontal', offset_number_horizontal)
        print('offset_number_vertical', offset_number_vertical)

        cellh = lambda x: c2e((x * 49.77)/99)
        cellw = lambda x: c2e((x * (18.65-1.71))/10)

        column = 3 + int(offset_number_horizontal)
        coloffset = cellw(0.5)
        row = 22
        rowoffset = cellh(0.5)
        
        size = XDRPositiveSize2D(p2e(w), p2e(h))
        marker = AnchorMarker(col=column, colOff=coloffset, row=row, rowOff= rowoffset)
        imgo.anchor = OneCellAnchor(_from=marker, ext=size)

        sh.add_image(imgo)
    
    print('image added successfully')
    return wb
    # # "id": 1,"id": 1,
    # "order_numbers": "['HG0000001', 'HG0000002']",
    # "facture_numbers": "['NCC-TK-00001']",
    # "specification_numbers": "['SPEC001']",
    # "tds_numbers": "['TDS795.135.1245']",
    # "declaration_numbers": "['00712/050621/32456']",
    # "coo_numbers": "['COO1']",
    # "product_name": "Simulateur à câble",
    # "product_name_fr": "Simulateur à câble",
    # "product_name_ru": "Тросовый тренажер",
    # "product_desc_fr": "\"Simulateur à câble\r\nDimensions 96 x 105 x 201 cm\r\nPoids 200 kg\r\nPoids standard: 55 kg (disponible en 70 et 105 kg) - intervalle d'ajustement de la résistance de 5 kg\r\nLibre sur le sol, peut être utilisé sans banc fixe\r\nLa taille est ajustable à la taille de la poutre\r\nPeut être utilisé seul ou à deux mains\r\nEgalement disponible avec 1 kg de poids supplémentaire par incréments de 1 kg (2-7pcs / pc / accessoire)\r\nLa hauteur des appareils est personnalisable\r\n\r\nQty: 1 U\"",
    # "product_desc_ru": "\"Тросовый тренажер\r\nРазмеры 96 х 105 х 201 см\r\nВес 200 кг\r\nСтандартный весовой пакет: 55 кг (в наличии 70 и 105 кг) - интервал регулировки сопротивления 5 кг\r\nСвободно на полу, можно использовать без неподвижной скамьи\r\nТалия регулируется по размеру всего луча\r\nМожет использоваться как одноручный или двуручный\r\nТакже доступны с дополнительным весом 1 кг с шагом 1 кг (2-7 шт. / Шт. / Аксессуар)\r\nВысота устройств настраивается\r\n\r\nКол-во: 1 шт\"",
    # "image_url": "/media/SIMULATEUR_DE_LEVAGE_DE_LA_PAZ_78085-0_G30_jCfzgkS.jpg",
    # "protocol": "Some Protocol",
    # "observation": "Good observation",

    # "number": "FP00001",
    # "index": "A",
    # "sign_tehnadzor": "Cary Meredov",
    # "date_contractor": "2021-10-02T11:20:25.345157Z",
    # "date_tehnadzor": "2021-10-02T11:20:25.345157Z",
    # "date_client": "2021-10-02T11:20:25.345157Z",
    # "created_at": "2021-10-02T11:20:25.345157Z",
    # "note_for_achat": "Please by nice one.",
    # "product": 3,
    # "provider": 1,

    # "origin": 2,
    # "manufactured_in": 2,
    # "project": 1,

    # "department": 1,

    # "location": 4,
    # "phase": 2,
    # "trade": 11,
    # "lot": 15,
    # "annexe5": null,

    # "fp_type": null,
    # "sign_contractor1": 1,
    # "sign_contractor2": 5,
    # "sign_client": 1,
    # "created_by": 1
    pass

def fp_pdf_works(**kwargs):
    pass
    # excel_path = kwargs['excel_path']
    # sh_name = kwargs['sh_name']
    # parent_path = kwargs['parent_path']
    # file_name = kwargs['file_name']

    # # df = pd.read_excel(excel_path)
    # # df.to_html(parent_path / 'test.html')

    # o = win32com.client.Dispatch("Excel.Application",pythoncom.CoInitialize())
    # o.Visible = False
    # print('created win32')
    # print('path must be win32', excel_path)
    # wb = o.Workbooks.Open(parent_path / 'fp.xlsx')
    # ws_index_list = [1] #say you want to print these sheets
    # print('opened workbook', wb.name)
    # path_to_pdf = Path(parent_path) / file_name + '.pdf'
    # print_area = 'A1:W45'

    # # for index in ws_index_list:
    # ws = wb.Worksheets[0]
    # ws.PageSetup.Zoom = False
    # ws.PageSetup.FitToPagesTall = 1
    # ws.PageSetup.FitToPagesWide = 1
    # ws.PageSetup.PrintArea = print_area

    # ws.Select()
    # wb.ActiveSheet.ExportAsFixedFormat(0, path_to_pdf)
    # wb.save()
    # wb.close()
    # o.quit()

    # print('before returning')
    # return path_to_pdf


def download(file_path, file_name, file_type):
    """
    e.g.: file_path = '/tmp/file.pdf'
    """
    try:
        if file_type=='pdf':
            wrapper = FileWrapper(open(file_path, 'rb'))
            response = HttpResponse(wrapper, content_type='application/force-download')
            response['Content-Disposition'] = 'inline; filename=' + file_name + '.pdf'
            return response
        if file_type=='excel':
            print('inside excel download', file_path)
            file = open(file_path, "rb")
            print(file)
            response = HttpResponse(file.read(),content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=report.xlsx'
            return response
    except Exception as e:
        print('exception when downloading')
        return None