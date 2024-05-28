import flet as ft
import datetime as dt
from lxml import html
import requests


#URL de las 2 estaciones metereológicas de Montilla
josemari = 'https://www.meteoclimatic.net/perfil/ESAND1400000014550C'
sanrafael = "https://www.meteoclimatic.net/perfil/ESAND1400000014550A"

class Meteoclimatic():

    def __init__(self, estacion):
        
        # USER AGENT PARA PROTEGERNOS DE BANEOS
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            }
        
        self.estacion = estacion

        # REQUERIMIENTO AL SERVIDOR
        self.pagina = requests.get(self.estacion, headers=headers)
        self.pagina.encoding = 'utf-8' # Codificar correctamente caracteres extranos
        
        # PARSEO DEL ARBOL HTML QUE RECIBO COMO RESPUESTA CON LXML
        parser = html.fromstring(self.pagina.content) # Uso .content para poder codificar los caracteres raros
        
        #almacenamos en datos_actuales una lista de python donde:
        #Posición[0]: Es la temperatura actual
        #Posición[1]: Es la humedad actual
        #Posición[2]: Es la velocidad del viento actual
        #Posición[3]: Es la presión atmosférica actual
        #Posición[4]: Es la radiación solar actual
        #Posición[5]: Precipitaciones acumuladas del día
        #Posición[6]: Dias de sequía (dias que llevamos sin que llueva)
        self.datos_actuales = parser.find_class("dadesactuals")
        
        #almacenamos en temp_max una lista de python donde:
        #Posición[0]: Es la temperatura máxima del día
        #Posición[1]: Es la humedad máxima del día
        #Posición[2]: Es la velocidad del viento máxima del día
        #Posición[3]: Es la presión atmosférica máxima del día
        #Posición[4]: Nada 
        #Posición[5]: Es la temperatura máxima del mes
        #Posición[6]: Es la humedad máxima del mes
        #Posición[7]: Es la velocidad del viento máxima del mes
        #Posición[8]: Es la presión atmosférica máxima del mes
        #Posición[9]: Nada
        #Posición[10]: Es la temperatura máxima del año
        #Posición[11]: Es la humedad máxima del año
        #Posición[12]: Es la velocidad del viento máxima del año
        #Posición[13]: Es la presión atmosférica máxima del año        
        self.temp_max = parser.find_class("vermell")

        #almacenamos en temp_min una lista de python donde:
        #Posición[0]: Es la temperatura mínima del día
        #Posición[1]: Es la humedad mínima del día
        #Posición[2]: Es la presión atmosférica mínima del día
        #Posición[3]: Es la temperatura mínima del mes
        #Posición[4]: Es la humedad mínima del mes 
        #Posición[5]: Es la presión atmosférica mínima del mes
        #Posición[6]: Es la temperatura mínima del año
        #Posición[7]: Es la humedad mínima del año
        #Posición[8]: Es la presión atmosférica mínima del año
        self.temp_min = parser.find_class("blau")
        self.ultima_actualizacion=dt.datetime.today().strftime("%H:%M:%S / %d-%m-%Y")

meteoclimatic2 = Meteoclimatic(josemari)
print(meteoclimatic2.datos_actuales[0].text_content())
print(meteoclimatic2.temp_max[0].text_content())
print(meteoclimatic2.temp_min[0].text_content())

def main(page: ft.Page):
    def actualiza_pagina(evento):
        page.update()
        print("he clickado")
        
    meteclimatic = Meteoclimatic(josemari)
    page.bgcolor=ft.colors.BLACK
    page.horizontal_alignment= "center"
    
    box_temp = ft.Container(
        
        bgcolor="#191C24",
        width=300,
        height=150,
        border_radius=10,
        #gradient=ft.LinearGradient(
        #    colors=[ft.colors.CYAN, ft.colors.WHITE],
        #    begin=ft.alignment.bottom_left,
        #    end=ft.alignment.top_right,
        #),
        shadow=ft.BoxShadow(
            blur_radius=5,
            color=ft.colors.WHITE,
        ),
        content=ft.Stack(
            fit=ft.StackFit.EXPAND,
            controls=[
                ft.Image(
                    #src="https://picsum.photos/150/150?9",
                    src="assets/montilla.jpg",
                    fit=ft.ImageFit.FILL
                ),
                ft.Text(
                    value=f"{meteclimatic.datos_actuales[0].text_content()}",
                    color="#191C24",
                    size=35,
                    left=10,
                    top=10,
                    font_family="courier",
                    weight=ft.FontWeight.BOLD,
                    style=ft.TextStyle(
                        shadow= ft.BoxShadow(
                            blur_radius=10,
                            color=ft.colors.BLACK,
                        )
                    )
                ),
                ft.Text(
                    value=f"Máxima: {meteclimatic.temp_max[0].text_content()} º",
                    bottom=10,
                    left= 10,
                    color=ft.colors.RED,
                    weight=ft.FontWeight.BOLD,
                    size=18,
                    style=ft.TextStyle(
                        shadow=ft.BoxShadow(
                            blur_radius=10,
                        )
                    )
                ),
                ft.Text(
                    value=f"Mínima: {meteclimatic.temp_min[0].text_content()} º",
                    bottom=10,
                    right=10,
                    size=18,
                    style=ft.TextStyle(
                        shadow=ft.BoxShadow(
                            blur_radius=10,
                        )
                    )
                ),
                ft.Container(
                    top=30,
                    right=10,
                    on_click=actualiza_pagina,
                    content=ft.Text(
                        value=dt.datetime.today().strftime("%H:%M:%S / %d-%m-%Y"),
                        size=10,
                        color=ft.colors.AMBER,
                        style=ft.TextStyle(
                            shadow=ft.BoxShadow(
                                blur_radius=10
                            )
                        ),
                    ),

                ),
 
            ]
        )

        
    )
    page.add(box_temp)


ft.app(target=main, assets_dir="assets")
