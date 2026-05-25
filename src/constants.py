MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 1024
NICHES_PER_RUN = 12
REQUEST_DELAY_SECS = 0.8

NICHES_SEED = [
    "accesorios para perros",
    "organizadores de cocina",
    "luces LED decorativas",
    "cargadores inalámbricos",
    "termos Stanley",
    "productos de skincare coreano",
    "repuestos para bicicleta",
    "juguetes Montessori",
    "funda para mate",
    "herramientas eléctricas pequeñas",
    "ropa deportiva mujer",
    "snacks importados",
    "impresoras 3D filamento",
    "suplementos deportivos",
    "zapatillas running",
    "artículos de camping",
    "mochilas escolares",
    "equipos de jardinería",
    "auriculares bluetooth",
    "sillas gamer",
]

SYSTEM_PROMPT = """\
Eres un experto analista de mercado especializado en Mercado Libre Argentina.
Tu tarea es analizar nichos de productos y devolver ÚNICAMENTE un objeto JSON válido, sin texto adicional, sin markdown, sin explicaciones.

El JSON debe tener exactamente esta estructura:
{
  "nicho": "nombre del nicho",
  "score": <número entero del 1 al 10>,
  "demanda": "alta" | "media" | "baja",
  "competencia": "alta" | "media" | "baja",
  "margen_estimado": "X%-Y%",
  "precio_rango": "$X.000 - $Y.000 ARS",
  "tendencia": "creciendo" | "estable" | "bajando",
  "oportunidad": "una oración describiendo la oportunidad principal",
  "riesgo": "una oración describiendo el riesgo principal",
  "productos_estrella": ["producto1", "producto2", "producto3"],
  "veredicto": "EXCELENTE" | "BUENO" | "REGULAR" | "EVITAR"
}"""

VERDICT_COLORS = {
    "EXCELENTE": "bold green",
    "BUENO": "bold cyan",
    "REGULAR": "bold yellow",
    "EVITAR": "bold red",
}

DEMAND_COLORS = {
    "alta": "green",
    "media": "yellow",
    "baja": "red",
}

COMPETITION_COLORS = {
    "alta": "red",
    "media": "yellow",
    "baja": "green",
}

TREND_COLORS = {
    "creciendo": "green",
    "estable": "yellow",
    "bajando": "red",
}
