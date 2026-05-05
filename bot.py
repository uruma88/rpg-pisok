import os
import mimetypes
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn

app = FastAPI()

mimetypes.add_type('application/wasm', '.wasm')
mimetypes.add_type('application/x-pck', '.pck')

@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
    response.headers["Cross-Origin-Embedder-Policy"] = "require-corp"
    return response

# Проверяем все возможные папки
base_path = os.getcwd() # Текущая папка, где работает бот

@app.get("/")
async def debug_root():
    # Ищем index.html во всех подпапках
    files_tree = []
    found_path = None
    
    for root, dirs, files in os.walk(base_path):
        for file in files:
            full_path = os.path.join(root, file)
            files_tree.append(full_path.replace(base_path, ""))
            if file == "index.html":
                found_path = root

    if found_path:
        return FileResponse(os.path.join(found_path, "index.html"))
    
    # Если не нашли — покажем дерево файлов прямо в браузере
    return {
        "status": "index.html not found",
        "i_am_searching_in": base_path,
        "files_i_found": files_tree
    }

# Монтируем статику на всякий случай везде
app.mount("/static", StaticFiles(directory=base_path), name="static")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
