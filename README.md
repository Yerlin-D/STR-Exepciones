# 🏥 Sistema de Monitoreo de Signos Vitales  

Este sistema monitorea en tiempo real los signos vitales de los pacientes, incluyendo temperatura, ritmo cardíaco y presión arterial.  

## ⚡ Manejo de Excepciones  

Para garantizar un funcionamiento estable y evitar fallos inesperados, se implemento **manejo de excepciones** en distintos módulos del sistema:  

### 🚀 **1. En el Servidor (`server.py`)**  
- **Problema:** Datos corruptos o mal formateados pueden hacer fallar el servidor.  
- **Solución:** Se usa `try-except` para capturar errores de formato JSON y notificar al cliente.  
  ```python
  try:
      data = await websocket.receive_text()
      dato = json.loads(data)  # Intenta convertir JSON
  except json.JSONDecodeError:
      print("Error en el formato de datos recibidos.")
      await websocket.send_text(json.dumps({"error": "Formato JSON inválido"}))
