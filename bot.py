import os
import mimetypes
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn

app = FastAPI()

# Важно для Godot: правильно определяем типы файлов
mimetypes.add_type('application/wasm', '.wasm')
mimetypes.add_type('application/x-pck', '.pck')

# Раздаем статические файлы игры из корня репозитория
app.mount("/static", StaticFiles(directory="."), name="static")

@app.get("/")
async def serve_game():
    # Отдаем скомпилированный index.html от Godot
    return FileResponse("index.html")

# API для сохранения прогресса (то, что отправляет HTTPRequest из Godot)
@app.post("/api/update_score")
async def update_score(data: dict):
    print(f"Обновление счета: {data}")
    return {"status": "success", "received": data}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)
