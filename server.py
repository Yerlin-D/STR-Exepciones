from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json

app = FastAPI()
datos = []  # Almacenará los signos vitales en memoria

@app.get("/")
def home():
    return {"message": "Monitor de Signos Vitales en tiempo real está funcionando"}

@app.get("/historial")
def obtener_historial():
    return {"historial": datos}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Cliente conectado")

    try:
        while True:
            try:
                # Recibir datos del sensor
                data = await websocket.receive_text()
                dato = json.loads(data)

                # Validación de datos esperados
                if not validar_datos(dato):
                    raise ValueError("Datos recibidos inválidos")

                # Determinar si hay alerta
                alerta = detectar_alerta(dato)
                dato["estado"] = "alerta" if alerta else "normal"
                datos.append(dato)

                print(f"Recibido: {dato}")
                await websocket.send_text(json.dumps(dato))

            except ValueError as e:
                print(f"Error en datos recibidos: {e}")
                await websocket.send_text(json.dumps({"error": "Datos inválidos"}))
            except json.JSONDecodeError:
                print("Error al procesar JSON")
                await websocket.send_text(json.dumps({"error": "Formato JSON inválido"}))

    except WebSocketDisconnect:
        print("Cliente desconectado")
    except Exception as e:
        print(f"Error inesperado en WebSocket: {e}")

def detectar_alerta(dato):
    try:
        temp_normal = (36.0, 37.5)
        ritmo_normal = (60, 100)
        presion_normal = (90, 140, 60, 90)

        sistolica, diastolica = map(int, dato["tension_arterial"].split("/"))

        if not (temp_normal[0] <= dato["temperatura"] <= temp_normal[1]):
            return True
        if not (ritmo_normal[0] <= dato["ritmo_cardiaco"] <= ritmo_normal[1]):
            return True
        if not (presion_normal[0] <= sistolica <= presion_normal[1] and presion_normal[2] <= diastolica <= presion_normal[3]):
            return True

        return False
    except (KeyError, ValueError):
        print("Error al analizar los signos vitales")
        return True  # Si hay un error, mejor tratarlo como una alerta

def validar_datos(dato):
    try:
        return all(key in dato for key in ["ritmo_cardiaco", "temperatura", "tension_arterial"])
    except Exception:
        return False
