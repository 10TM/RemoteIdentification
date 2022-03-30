import pytesseract
import logging
from PIL import Image
from flask import Flask, jsonify, request

app = Flask(__name__)


# logging.basicConfig(filename = 'filename.log', level=logging.log_level, format = '<message_structure>')


def extract_text (path):
    try:
        img = Image.open(path)
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        preds = pytesseract.image_to_string(img, lang="eng")
    except Exception:
        return -1

    return preds


def getInn (temp):
    inn = str()
    count = 0
    for i in range(len(temp)):
        if temp[i].isnumeric() == True or temp[i] == " ":
            if temp[i] != " ":
                count = count + 1
                inn += temp[i]
            if count == 14:
                break
        else:
            inn = ""
            count = 0
    return inn


# def getmkk(temp):
#     mkk = str()
#     l = 0
#     for i in range(len(temp)):
#         if temp[i].isnumeric() and temp[i - 1] == " " and temp[i - 2] == 'K' and temp[i - 3] == 'K' and temp[
#             i - 4] == 'M':
#             z = i
#             for j in range(6):
#                 mkk += temp[z]
#                 z += 1
#                 l = 1
#         if l == 1:
#             break
#     return mkk


def getId(temp):
    id = str()
    o = 0
    for i in range(len(temp)):
        if temp[i] == 'I' and temp[i + 1] == 'D':
            c = i

            for j in range(9):
                id += temp[c]
                c += 1
                o = 1
        if o == 1:
            break

    return id


def create_person_data (path):
    temp = str(extract_text(path))
    inn = str()
    fullName = str()
    mkk = str()
    id = str()

    if temp == -1:
        status = 1
    else:
        status = 0
        # FIO = str(getFIO(temp))
        # DataBirth = str(getDataBirth(temp))
        # mkk = str(getmkk(temp))
        inn = str(getInn(temp))
        id = str(getId(temp))

    person_data = {
        "status": status,
        "fullName": fullName,
        "mkk": mkk,
        "id": id,
        "inn": inn
    }

    return person_data


@app.route('/todo', methods=['POST'])
def Home ():
    temp = str(request.json)
    try:
        path = str(temp[14: (temp.index(".png") + 4)])
    except Exception:
        return jsonify({
            "status": 1
        })

    return jsonify(create_person_data(path))


if __name__ == '__main__':
    from waitress import serve

    serve(app, host="0.0.0.0", port=5000)
