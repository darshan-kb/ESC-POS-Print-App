from flask import Flask, request, render_template, jsonify
# from flask_cors import CORS, cross_origin
import win32ui
import win32print
import win32con
from PIL import Image, ImageWin, ImageDraw, ImageFont
from barcode import EAN13
from barcode.writer import ImageWriter

app = Flask(__name__)
# if __name__ == "__main__":
#      app.run(debug=True ,port=8080,use_reloader=False)
# cors = CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'

# @app.route('/print', methods=['POST'])

# def print_page():
#     string_to_print = request.form.get('text')
#     # Code to print the string on the printer page goes herecd
#     return 'String printed successfully!'
@app.route('/', methods=["POST"])
def print_string_on_page():
    input_json = request.get_json(force=True)
    print(input_json['ticketId'])
    print(input_json['data'])
    text(input_json)
    #dictToReturn = {'text':input_json['text']}
    printImage()
    # INCH=1440
    #  
    # 
    # print(input_json['text'])
    # hDC = win32ui.CreateDC()
    # hDC.CreatePrinterDC(win32print.GetDefaultPrinter())
    # hDC.StartDoc("Test doc")
    # hDC.StartPage()
    # hDC.SetMapMode(win32con.MM_TWIPS)
    # hDC.DrawText(input_json['text'], (-4000, 0, 8000, -6000), win32con.DT_CENTER)
    # hDC.EndPage()
    # hDC.EndDoc()



    return jsonify()

    
    #pass
    #return None
def text(input_json):

    ticketId = input_json['ticketId']
    data = input_json['data']
    number = ticketId
    my_code = EAN13(number, writer=ImageWriter())
    my_code.save("new_code1")
    img = Image.open('new_code1.png', 'r')
    
    barcode_size = img.size
    resized = img.resize((barcode_size[0]//2,barcode_size[1]//2),resample=Image.Resampling.LANCZOS)
    image = Image.new("RGB", (400, 400), "white")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("Gidole-Regular.ttf", size=30)
    draw.text((110, 0), ticketId,font=font,fill="black")
    draw.text((110, 35), data,font=font,fill="red")

    image.paste(resized,(80,300))
    #final = image.resize((302*2, 1122*2), resample=Image.Resampling.NEAREST)
    image.save("text.jpg")

def printImage():
    
    HORZRES = 8
    VERTRES = 10
#
# LOGPIXELS = dots per inch
#
    LOGPIXELSX = 88
    LOGPIXELSY = 90
#
# PHYSICALWIDTH/HEIGHT = total area
#
    PHYSICALWIDTH = 110
    PHYSICALHEIGHT = 111
#
# PHYSICALOFFSETX/Y = left / top margin
#
    PHYSICALOFFSETX = 112
    PHYSICALOFFSETY = 113

    printer_name = win32print.GetDefaultPrinter ()
    file_name = "text.jpg"

#
# You can only write a Device-independent bitmap
#  directly to a Windows device context; therefore
#  we need (for ease) to use the Python Imaging
#  Library to manipulate the image.
#
# Create a device context from a named printer
#  and assess the printable size of the paper.
#
    hDC = win32ui.CreateDC ()
    hDC.CreatePrinterDC (printer_name)
    printable_area = hDC.GetDeviceCaps (HORZRES), hDC.GetDeviceCaps (VERTRES)
    printer_size = hDC.GetDeviceCaps (PHYSICALWIDTH), hDC.GetDeviceCaps (PHYSICALHEIGHT)
    printer_margins = hDC.GetDeviceCaps (PHYSICALOFFSETX), hDC.GetDeviceCaps (PHYSICALOFFSETY)


#
# Open the image, rotate it if it's wider than
#  it is high, and work out how much to multiply
#  each pixel by to get it as big as possible on
#  the page without distorting.
#
    bmp = Image.open (file_name)
# if bmp.size[0] > bmp.size[1]:
#   bmp = bmp.rotate (90)

    ratios = [1.0 * printable_area[0] / bmp.size[0], 1.0 * printable_area[1] / bmp.size[1]]
    scale = min (ratios)

#
# Start the print job, and draw the bitmap to
#  the printer device at the scaled size.
#
    hDC.StartDoc (file_name)
    hDC.StartPage ()


    dib = ImageWin.Dib (bmp)
    scaled_width, scaled_height = [int (scale * i) for i in bmp.size]
    x1 = int ((printer_size[0] - scaled_width) / 2)
    y1 = int ((printer_size[1] - scaled_height) / 2)
    x2 = x1 + scaled_width
    y2 = y1 + scaled_height
# hDC.SetMapMode(win32con.MM_TWIPS)
# hDC.DrawText("Hello world", (-4000, 0, 8000, -6000), win32con.DT_CENTER)
    dib.draw (hDC.GetHandleOutput (), (x1, y1, x2, y2))
    hDC.DrawText("Hello world", (-4000, 0, 8000, -6000))
    hDC.EndPage ()
    hDC.EndDoc ()
    hDC.DeleteDC ()


# @app.route('/print', methods=['POST'])
# def print_page():
#     string_to_print = request.form.get('text')
#     print_string_on_page(str_to_print) #string_to_print
#     return 'String printed successfully!'


# if __name__ == '__main__':
#     app.run(debug=True)


#from pywin import win32print