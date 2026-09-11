import requests

url = "http://localhost:1234/v1/models"

respuesta = requests.get(url)

print("Código HTTP:", respuesta.status_code)
print(respuesta.json())