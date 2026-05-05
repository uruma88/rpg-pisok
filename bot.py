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

# Определяем папку, где лежит сам bot.py
current_dir = os.path.dirname(os.path.abspath(__file__))
# Принудительно меняем рабочую директорию на папку со скриптом
os.chdir(current_dir)

@app.get("/")
async def serve_game():
    # Ищем index.html именно в текущей папке
    if os.path.exists("index.html"):
        return FileResponse("index.html")
    
    # Если не нашли — выводим список файлов для диагностики
    files = os.listdir(".")
    return {
        "status": "error",
        "message": "index.html not found",
        "work_dir": os.getcwd(),
        "files_here": files
    }

# Монтируем корень для раздачи .js, .wasm и .pck
app.mount("/", StaticFiles(directory="."), name="static")

if __name__ == "__main__":
    # BotHost передает порт через переменную PORT
    port = int(os.environ.get("PORT", 3000))
    uvicorn.run(app, host="0.0.0.0", port=port)
