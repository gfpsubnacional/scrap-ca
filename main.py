# -*- coding: utf-8 -*-
"""
Created on Wed Apr 23 14:43:35 2025

@author: Consultor
"""

from fastapi import FastAPI
from pydantic import BaseModel
import time
from scraper import scrape_ca  # Importa tu función de scraping

app = FastAPI()

# Modelo de solicitud para enviar los parámetros de scraping
class ScrapeRequest(BaseModel):
    gobierno_regional: str
    categoria_presupuestal: str

# Endpoint para iniciar el scraping
@app.post("/scrape")
async def scrape(request: ScrapeRequest):
    # Aquí pasamos los parámetros a la función de scraping
    try:
        # Ejecutar scraping con los parámetros recibidos
        result = scrape_ca(request.gobierno_regional, request.categoria_presupuestal)
        return {"status": "success", "data": result.to_dict()}  # Convierte el DataFrame a dict
    except Exception as e:
        return {"status": "error", "message": str(e)}
