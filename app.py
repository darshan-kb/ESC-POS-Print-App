from flask import Flask, request, render_template, jsonify
# from flask_cors import CORS, cross_origin
import win32ui
import win32print
import win32con

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
    INCH=1440
    input_json = request.get_json(force=True) 
    dictToReturn = {'text':input_json['text']}
    print(input_json['text'])
    hDC = win32ui.CreateDC()
    hDC.CreatePrinterDC(win32print.GetDefaultPrinter())
    hDC.StartDoc("Test doc")
    hDC.StartPage()
    hDC.SetMapMode(win32con.MM_TWIPS)
    hDC.DrawText(input_json['text'], (-4000, 0, 8000, -6000), win32con.DT_CENTER)
    hDC.EndPage()
    hDC.EndDoc()



    return jsonify(dictToReturn)

    
    #pass
    #return None

# @app.route('/print', methods=['POST'])
# def print_page():
#     string_to_print = request.form.get('text')
#     print_string_on_page(str_to_print) #string_to_print
#     return 'String printed successfully!'


# if __name__ == '__main__':
#     app.run(debug=True)


#from pywin import win32print