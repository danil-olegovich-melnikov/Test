import requests
import xml.etree.ElementTree as ET


xml_file = "cbr.xml"

def loadRSS(date: str) -> None:
    url = f'https://www.cbr.ru/scripts/XML_daily.asp?date_req={date}'
    resp = requests.get(url)

    with open(xml_file, 'wb') as f:
        f.write(resp.content)


def parseXML() -> float:
    tree = ET.parse(xml_file)
    root = tree.getroot()
    is_found = False
    rate = 0

    for row in root.findall('./'):
        for item in row:
            if rate != 0:
                break
            elif is_found and item.tag == "Value":
                rate = float(str(item.text).replace(",", "."))
            elif item.tag == "Name" and item.text == "Доллар США":
                is_found = True

    return rate


def get_exchange_rate(date: str) -> float:
    loadRSS(date)
    rate = parseXML()

    return rate

