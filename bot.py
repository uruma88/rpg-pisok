import os
import mimetypes
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn

app = FastAPI()

# Стандартные типы для корректной работы Godot
mimetypes.add_type('application/wasm', '.wasm')
mimetypes.add_type('application/x-pck', '.pck')

# Определяем реальную папку, где лежит этот скрипт
current_dir = os.path.dirname(os.path.abspath(__file__))
# Принудительно заставляем сервер работать именно в этой папке
os.chdir(current_dir)

@app.get("/")
async def serve_game():
    index_path = os.path.join(current_dir, "index.html")
    
    # Если файл найден — отдаем его
    if os.path.exists(index_path):
        return FileResponse(index_path)
    
    # Если не найден — показываем всё, что видит сервер, для диагностики
    return {
        "status": "error",
        "message": "index.html not found",
        "current_dir": current_dir,
        "files_found_here": os.listdir(current_dir)
    }

# Раздаем остальные файлы (js, wasm, pck)
app.mount("/", StaticFiles(directory=current_dir), name="static")

if __name__ == "__main__":
    # BotHost передает порт через переменную PORT
    port = int(os.environ.get("PORT", 3000))
    uvicorn.run(app, host="0.0.0.0", port=port)
