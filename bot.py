import os
import mimetypes
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn

app = FastAPI()

# Принудительно ставим типы, чтобы браузер не ругался на игру
mimetypes.add_type('application/wasm', '.wasm')
mimetypes.add_type('application/x-pck', '.pck')
mimetypes.add_type('text/javascript', '.js')

# Определяем путь к текущей папке
current_dir = os.path.dirname(os.path.realpath(__file__))

# 1. Главная страница
@app.get("/")
async def serve_index():
    index_path = os.path.join(current_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"error": "index.html not found in root directory"}

# 2. Раздача всех остальных файлов игры (js, wasm, pck)
app.mount("/", StaticFiles(directory=current_dir), name="static")

@app.post("/api/update_score")
async def update_score(data: dict):
    print(f"Данные из игры: {data}")
    return {"status": "ok"}

if __name__ == "__main__":
    # Хостинг сам назначит порт через переменную PORT
    port = int(os.environ.get("PORT", 3000))
    uvicorn.run(app, host="0.0.0.0", port=port)
