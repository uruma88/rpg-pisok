import os
import mimetypes
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn

app = FastAPI()

# Добавляем типы для корректной работы Godot
mimetypes.add_type('application/wasm', '.wasm')
mimetypes.add_type('application/x-pck', '.pck')

# Явно указываем путь к текущей папке
current_dir = os.path.dirname(os.path.abspath(__file__))

@app.get("/")
async def serve_game():
    index_path = os.path.join(current_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    
    # Если файла нет, выведем список того, что видит сервер
    return {
        "status": "error",
        "message": "index.html not found",
        "debug_current_dir": current_dir,
        "files_in_directory": os.listdir(current_dir)
    }

# Монтируем статику ПОСЛЕ основного роута
app.mount("/", StaticFiles(directory=current_dir), name="static")

if __name__ == "__main__":
    # На BotHost порт часто передается через переменную PORT
    port = int(os.environ.get("PORT", 8080))
    # ВАЖНО: используем 0.0.0.0, чтобы сервер был виден снаружи
    uvicorn.run(app, host="0.0.0.0", port=port)
