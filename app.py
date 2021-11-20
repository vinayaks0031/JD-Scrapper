from flask import Flask, send_file, render_template, request
import requests
from bs4 import BeautifulSoup as BS
import xlsxwriter

app = Flask(__name__)


def scrapper(url):
    # making excel sheet
    workbook = xlsxwriter.Workbook('ScrappedFile.xlsx')
    worksheet = workbook.add_worksheet()

    # getting from justdial
    agent = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    page = requests.get(url, headers=agent)

    soup = (BS(page.content, 'html.parser'))

    contacts = list(soup.find_all(class_='contact-info'))
    shopNames = list(soup.find_all(class_='lng_cont_name'))
    addresses = list(soup.find_all(class_='cont_fl_addr'))

    icons = dict()

    # All posible classes
    icons["icon-yz"] = "1"
    icons["icon-wx"] = "2"
    icons["icon-vu"] = "3"
    icons["icon-ts"] = "4"
    icons["icon-rq"] = "5"
    icons["icon-po"] = "6"
    icons["icon-nm"] = "7"
    icons["icon-lk"] = "8"
    icons["icon-ji"] = "9"
    icons["icon-acb"] = "0"
    icons["icon-dc"] = "+"
    icons["icon-fe"] = "("
    icons["icon-hg"] = ")"
    icons["icon-ba"] = "-"

    # storing numbers
    number = dict()
    id = 0
    for i in contacts:
        numbers = i.find_all(class_="mobilesv")
        number[id] = ""
        for j in numbers:
            number[id] += icons[j["class"][1]]
        id = id + 1

    # storing names of shops
    idC = 0
    shopName = dict()
    for k in shopNames:
        shopName[idC] = ""
        shopName[idC] += k['data-cn']
        idC = idC+1

    # storing address
    idA = 0
    address = dict()
    for add in addresses:
        address[idA] = ""
        address[idA] += add.contents[0]
        idA = idA+1

    row = 0
    columnShop = 1
    columnNum = 2
    columnAddr = 3
    # writing data in excel file
    for name in shopName:
        worksheet.write(row, columnShop, shopName[name])
        worksheet.write(row, columnNum, number[name])
        worksheet.write(row, columnAddr, address[name])
        row += 1

    workbook.close()
    return


@app.route('/', methods=['GET', 'POST'])
def gettingData():
    if request.method == 'POST':
        url = request.form['url']
        scrapper(url)
    return render_template('index.html')


@app.route('/download')
def download_file():
    path = "ScrappedFile.xlsx"
    return send_file(path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
