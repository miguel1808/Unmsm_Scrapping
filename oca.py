import os
import datetime
from bs4 import BeautifulSoup
import requests
import csv

urlBase="https://admision.unmsm.edu.pe/Website20242/"
response=requests.get("https://admision.unmsm.edu.pe/Website20242/index.html", headers={'Content-Type': 'text/html; charset=utf-8'})
# Imprimir el código de estado

def main():
    html = BeautifulSoup(response.content.decode('utf-8'), "html.parser")
    # Imprimir el título de la página
    tbody=html.find("tbody")
    tds=tbody.find_all("td")

    for td in tds:
        
        Modalidad=td.find("a")
        src= Modalidad.get("href")
        scrapPorModalidad(Modalidad.text, src)


def scrapPorModalidad(modalidad, link):
    response=requests.get(urlBase+link, headers={'Content-Type': 'text/html; charset=utf-8'})
    html = BeautifulSoup(response.content.decode('utf-8'), "html.parser", from_encoding="iso-8859-8")
    tbody=html.find("tbody")
    tds=tbody.find_all("td")
    with open("resultados.csv", "a", newline="",encoding="utf-8" ) as file:
            writer = csv.writer(file)
            
            for td in tds:
                
                src=td.find("a").get("href").replace("./", "")
                
                for carrera in scrapPorCarrera(modalidad, src):
                    
                    writer.writerow(carrera)



def scrapPorCarrera(modalidad, link):
    response=requests.get(urlBase+link, headers={'Content-Type': 'text/html; charset=utf-8'})
    html = BeautifulSoup(response.content.decode("utf-8"), "html.parser")
    
    tbody=html.find("tbody")
    trs=tbody.find_all("tr")
    arreglo=[]
    for tr in trs:
        fila=tr.find_all("td")

        codigo=fila[0].text
        nombre=fila[1].text
        carrera=fila[2].text
        if(carrera=="LENGUAS, TRADUCCIÓN E INTERPRETACIÓN"):
            carrera="LENGUAS TRADUCCIÓN E INTERPRETACIÓN"
        puntaje=fila[3].text
        if(puntaje=="71Âº Reglamento de Admisión / Ley Universitaria N.Â"):
            puntaje=puntaje.encode("latin1").decode("utf-8")
        puesto=fila[4].text
        
        vacantes = fila[5].text
        
        segundaOp=fila[6].text
        
        mod=modalidad
        arreglo.append([codigo,nombre,carrera,puntaje,puesto,vacantes,segundaOp,mod])
        
    return arreglo    
    # 
    #     
    #         
    #         
    #         print(fila[0].text, fila[1].text,modalidad)
    
        
        
def es_numero(dato):
    try:
        float(dato)  # Intentar convertir 'dato' a un flotante
        return False
    except ValueError:
        return True
if __name__ == "__main__":
    main()