#app/services/transacciones_api_productos.py
import requests

BASE ="http://localhost:8000/products"
TIME_OUT=10

#Obtiene la lista de productos de FastAPI
def list_products(limit:int=20, offset:int=0) -> dict:
    try:
        #request.get se conecta al api y entrega la información en r
        r=requests.get(f"{BASE}/", params={"limit":limit, "offset":offset}, timeout=TIME_OUT)
        #si el status_code es cualquier código 200 se entrega el resultado en formato json
        if 200 <= r.status_code < 300:
            return r.json() if r.content else {}
        raise ValueError(f"Error {r.status_code}", r.status_code, r.text)
    except requests.exceptions.RequestException as e:
        raise ValueError("Error de conexión", None, str(e))

#Obtiene el productos con el id que se le pasa como parametro
def get_product(product_id:str) -> dict:
    try:
        r=requests.get(f"{BASE}/{product_id}", timeout=TIME_OUT)
        if 200 <= r.status_code < 300:
            return r.json() if r.content else {}
        raise ValueError(f"Error {r.status_code}", r.status_code, r.text)
    except requests.exceptions.RequestException as e:
        raise ValueError("Error de conexión", None, str(e))

#Crea un producto nuevo con los datos que se le pasan como parametro en un diccionario
def create_product(data:dict)->dict:
    try:
        r=requests.post(f"{BASE}/", json=data, timeout=TIME_OUT)
        if 200 <= r.status_code < 300:
            return r.json() if r.content else {}
        raise ValueError(f"Error {r.status_code}", r.status_code, r.text)
    except requests.exceptions.RequestException as e:
        raise ValueError("Error de conexión", None, str(e))

#Actualiza el producto que se le indica con el id y los datos nuevos en un diccionario
def update_product(product_id:str, data:dict)->dict:
    try:
        r=requests.put(f"{BASE}/{product_id}", json=data, timeout=TIME_OUT)
        if 200 <= r.status_code < 300:
            return r.json() if r.content else {}
        raise ValueError(f"Error {r.status_code}", r.status_code, r.text)
    except requests.exceptions.RequestException as e:
        raise ValueError("Error de conexión", None, str(e))

#Borra el producto que se le indica con el id
def delete_product(product_id:str):
    try:
        r=requests.delete(f"{BASE}/{product_id}", timeout=TIME_OUT)
        if 200 <= r.status_code < 300:
            return r.json() if r.content else {}
        raise ValueError(f"Error {r.status_code}", r.status_code, r.text)
    except requests.exceptions.RequestException as e:
        raise ValueError("Error de conexión", None, str(e))

print(list_products())
