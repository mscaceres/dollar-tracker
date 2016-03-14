import collections
import datetime
import urllib
import bs4

DolarPoint = collections.namedtuple("DolarPoint", "date, buy_price, sell_price")

def get_scrap_functions():
    """Look for funtions with the name 'scrap_<source>' in the current file.
    It return the pair (<source>, function)"""
    return [(k.replace("scrap_", ""), v) for k, v in globals().items() if k.startswith("scrap_") and callable(v)]

def scrap_la_nacion():
    import json
    url = "http://contenidos.lanacion.com.ar/json/dolar?callback=jsonpCallback"
    json_response = str(urllib.request.urlopen(url).read())
    dict = json.loads(json_response[json_response.find("{"):json_response.find("}")+1])
    buy_price = float(dict["CasaCambioCompraValue"].replace(",", "."))
    sell_price = float(dict["CasaCambioVentaValue"].replace(",", "."))
    date = datetime.date.today() #datetime.datetime.strptime(dict["Date"][:dict["Date"].find("T")], "%Y-%m-%d")
    print("La Nacion")
    print("Fecha:", date)
    print("Compra:", buy_price)
    print("Venta:", sell_price)

    return DolarPoint(date=date, buy_price=buy_price, sell_price=sell_price)


def scrap_precio_dolar():
    url = "http://www.preciodolar.com.ar/"
    data = str(urllib.request.urlopen(url).read())
    soup = bs4.BeautifulSoup(data, "html.parser")
    values = soup.find_all("td", class_="Estilo4")
    buy_price = float(values[0].contents[0])
    sell_price = float(values[1].contents[0])
    date = datetime.date.today()
    print("Precio Dolar")
    print("Fecha:", date)
    print("Compra:", buy_price)
    print("Venta:", sell_price)
    return DolarPoint(date=date, buy_price=buy_price, sell_price=sell_price)