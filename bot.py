import os
import mimetypes
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn

app = FastAPI()

# Принудительно устанавливаем типы для Godot
mimetypes.add_type('application/wasm', '.wasm')
mimetypes.add_type('application/x-pck', '.pck')

# Путь к директории, где лежит этот скрипт
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.get("/")
async def serve_game():
    index_path = os.path.join(BASE_DIR, "index.html")
    
    # Если файл найден — отдаем его
    if os.path.isfile(index_path):
        return FileResponse(index_path)
    
    # Если не найден — показываем список файлов, чтобы понять, где мы
    files_in_dir = os.listdir(BASE_DIR)
    return {
        "error": "index.html not found",
        "current_directory": BASE_DIR,
        "files_available": files_in_dir
    }

# Раздаем все остальные файлы (js, wasm, pck)
app.mount("/", StaticFiles(directory=BASE_DIR), name="static")

if __name__ == "__main__":
    # Используем порт 3000 или тот, что даст хостинг
    port = int(os.environ.get("PORT", 3000))
    uvicorn.run(app, host="0.0.0.0", port=port)
