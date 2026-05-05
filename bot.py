import os
import mimetypes
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn

app = FastAPI()

# Добавляем типы для Godot
mimetypes.add_type('application/wasm', '.wasm')
mimetypes.add_type('application/x-pck', '.pck')

current_dir = os.path.dirname(os.path.abspath(__file__))

# 1. Сначала ставим статику, но на путь /static или просто убедимся, что она не мешает корню
# Но лучше всего для Godot работает такой вариант:
@app.get("/")
async def serve_game():
    index_path = os.path.join(current_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"error": "index.html not found", "files": os.listdir(current_dir)}

# Монтируем всё остальное
app.mount("/", StaticFiles(directory=current_dir), name="static")

if __name__ == "__main__":
    # На BotHost порт часто передается через переменную PORT
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
