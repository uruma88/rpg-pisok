import os
import mimetypes
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn

app = FastAPI()

# Правильные типы для Godot
mimetypes.add_type('application/wasm', '.wasm')
mimetypes.add_type('application/x-pck', '.pck')

# Путь к текущей директории
current_dir = os.path.dirname(os.path.realpath(__file__))

# Сначала монтируем статику, НО НЕ на корень, чтобы не было конфликтов
app.mount("/game_files", StaticFiles(directory=current_dir), name="static")

@app.get("/")
async def serve_game():
    # Явно указываем путь к файлу
    index_path = os.path.join(current_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"error": f"index.html not found. Files in root: {os.listdir(current_dir)}"}

@app.post("/api/update_score")
async def update_score(data: dict):
    print(f"Клики: {data}")
    return {"status": "ok"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    uvicorn.run(app, host="0.0.0.0", port=port)
