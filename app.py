import pytesseract
from PIL import Image
from flask import Flask, jsonify, request

app = Flask(__name__)


def extract_text (path):  # Вытаскиваем данные с паспорта
    img = Image.open(path)
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    preds = pytesseract.image_to_string(img, config="digits")
    return preds


def getInn (temp):
    inn = str()
    count = 0
    for i in range(len(temp)):
        if (temp[i].isnumeric() == True or temp[i] == " "):
            if (temp[i] != " "):
                count = count + 1
                inn += temp[i]
            if (count == 14):
                break
        else:
            inn = ""
            count = 0
    return (inn)


# def getmkk(temp):
#     mkk = str()
#     l = 0
#     z = 0
#     for i in range(len(temp)):
#         if(temp[i].isnumeric() and temp[i-1] == " " and temp[i-2] == 'K' and temp[i-3] == 'K' and temp[i-4] == 'M'):
#             z = i
#             for j in range(6):
#                 mkk += temp[z]
#                 z += 1
#                 l = 1
#         if(l == 1):
#             break
#     return(mkk)


# def getid(temp):
#     id = str()
#     o = 0
#     c = 0
#     for i in range(len(temp)):
#         if(temp[i].isnumeric() and temp[i-1] == ' ' and temp[i-2] == 'I' and temp[i-3] == 'D'):
#             c = i

#             for j in range(7):
#                 id += temp[c]
#                 c += 1
#                 o = 1
#         if(o == 1):
#             break
#         #print(temp)
#         return(id)


def create_person_data (path):
    temp = str(extract_text(path))
    # FIO = str(getFIO(temp))
    # DataBirth = str(getDataBirth(temp))
    # mkk = str(getmkk(temp))
    inn = str(getInn(temp))
    # id = str(getid(temp))

    person_data = {
        # "FIO": FIO,
        # "DataBirth": DataBirth,
        # "ID": ,
        # "Dataf": ,
        # "MKK": mkk,
        # "ID": id,
        # "DateI": ,
        "INN": inn
    }

    return person_data


@app.route('/todo', methods=['POST'])
def Home ():
    temp = str(request.json)
    return jsonify(create_person_data(temp[14: (temp.index(".png") + 4)]))


if __name__ == '__main__':
    app.run(debug=True)
