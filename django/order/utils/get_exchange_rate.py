import requests
import xml.etree.ElementTree as ET


xml_file = "cbr.xml"
exchange_rates_by_date = {}


def loadRSS(date: str) -> None:
    """
    Get exchange rate file by date from internet
    :param date: date from sheet table
    :return:
    """
    url = f'https://www.cbr.ru/scripts/XML_daily.asp?date_req={date}'
    resp = requests.get(url)

    with open(xml_file, 'wb') as f:
        f.write(resp.content)


def parseXML() -> float:
    """
    parse XML file
    :return: exchange rate
    """

    tree = ET.parse(xml_file)
    root = tree.getroot()

    is_found = False
    rate = 0

    for row in root.findall('./'):
        for item in row:
            if is_found and item.tag == "Value":
                rate = float(str(item.text).replace(",", "."))
                break
            elif item.tag == "Name" and item.text == "Доллар США":
                is_found = True

    return rate


def get_exchange_rate(date: str) -> float:
    """
    Main function to handle getting the exchange rate by date
    :param date:
    :return:
    """
    if date not in exchange_rates_by_date:
        loadRSS(date)
        rate = parseXML()
        exchange_rates_by_date[date] = rate
    else:
        rate = exchange_rates_by_date[date]
    return rate

