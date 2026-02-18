import unicodedata
import re
from typing import List


# Podríamos implementar un modelo de (NLP AI) para matchear la busqueda realizada con Enum Category
# De momento lo dejaré así (no añado matching en inglés)

category_keywords = {
    "CAMISETAS": ["camiseta", "camisetas", "camisa", "camisas", "polo", "polos"],
    "PANTALONES": ["pantalon", "pantalones", "jean", "jeans", "vaquero", "vaqueros", "bermuda", "bermudas", "chino", "chinos"],
    "ZAPATOS": ["zapato", "zapatos", "zapatilla", "zapatillas", "calzado", "calzados", "tenis"],
    "TELEFONOS": ["telefono", "telefonos", "celular", "celulares", "movil", "moviles", "smartphone", "smartphones"],
    "PORTATILES": ["portatil", "portatiles", "laptop", "laptops", "notebook", "notebooks", "computadora", "computadoras"],
    "OTROS": ["otro", "otros", "varios", "varias", "misc", "diverso", "diversos"]
}

# Clases del squeezenet.onnx (guardadas en squeezenet.txt)
category_keywords["CAMISETAS"].extend(["t-shirt", "jersey", "sweatshirt", "tank top", "maillot", "gown", "suit", "cloak", "robe", "shirt"])
category_keywords["PANTALONES"].extend(["jean", "trouser", "pants", "shorts", "denim", "bloomers", "kilt", "sarong"])
category_keywords["ZAPATOS"].extend(["shoe", "sandal", "loafer", "sneaker", "boot", "oxford", "moccasin", "clog", "running shoe"])
category_keywords["TELEFONOS"].extend(["phone", "cellular", "telephone", "mobile", "smartphone", "ipod"])
category_keywords["PORTATILES"].extend(["laptop", "notebook", "netbook", "computer", "pc", "macbook"])
category_keywords["OTROS"].extend(["misc", "other", "various", "unknown"])


def normalize(text: str) -> str:
    """
    Devuelve la cadena de texto pasada como parámetro normalizada.
    """
    text = unicodedata.normalize("NFD", text) # descompone acentos o signos en dos partes
    text = text.encode("ascii", "ignore").decode("utf-8") # ignora los caracteres que no puedan ser representados en ASCII
    return re.sub(r"[^\w\s]", "", text.lower()) # elimina todos los caracteres que NO sean palabras (\w) ni espacios (\s)

def search_categories_from_text(query: str) -> List[str]:
    """
    Dada una cadena de texto, devuelve una lista de categorías que coinciden
    con las palabras clave definidas. Si no hay coincidencias, devuelve ['OTROS'].
    """
    query = normalize(query)
    query = query.split()
    matches = set()
    
    for category, keywords in category_keywords.items():
        for sub_query in query:
            if (sub_query in keywords):
                matches.add(category)
    
    return ["OTROS"] if not matches else list(matches)

