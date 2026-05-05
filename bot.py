import os
import mimetypes
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn

app = FastAPI()

# 1. Настройка типов файлов (чтобы Godot 4 не выдавал ошибки)
mimetypes.add_type('application/wasm', '.wasm')
mimetypes.add_type('application/x-pck', '.pck')

# 2. Обязательные заголовки для работы движка в браузере
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
    response.headers["Cross-Origin-Embedder-Policy"] = "require-corp"
    return response

# 3. Автоматическое определение папки, где лежит этот файл
current_dir = os.path.dirname(os.path.abspath(__file__))

@app.get("/")
async def serve_game():
    index_path = os.path.join(current_dir, "index.html")
    
    # Если файл index.html найден — отдаем его
    if os.path.exists(index_path):
        return FileResponse(index_path)
    
    # Если не нашли — выводим список файлов для диагностики (поможет нам понять ошибку)
    return {
        "error": "index.html not found",
        "current_directory": current_dir,
        "files_in_directory": os.listdir(current_dir)
    }

# 4. Раздача всей статики (wasm, pck, js) из текущей папки
app.mount("/", StaticFiles(directory=current_dir), name="static")

if __name__ == "__main__":
    # Читаем PORT из переменных окружения BotHost (по умолчанию 8080)
    port = int(os.environ.get("PORT", 8080))
    print(f"Сервер запускается на порту {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port)
