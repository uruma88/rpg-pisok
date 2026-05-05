import os
import mimetypes
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import uvicorn

app = FastAPI()

# Типы файлов для Godot
mimetypes.add_type('application/wasm', '.wasm')
mimetypes.add_type('application/x-pck', '.pck')

@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
    response.headers["Cross-Origin-Embedder-Policy"] = "require-corp"
    return response

@app.get("/")
async def root():
    # Собираем список всех файлов в проекте для диагностики
    all_files = []
    found_index = None
    for root_dir, dirs, files in os.walk("."):
        for file in files:
            rel_path = os.path.join(root_dir, file)
            all_files.append(rel_path)
            if file == "index.html":
                found_index = rel_path

    # Если нашли игру — запускаем
    if found_index:
        return FileResponse(found_index)
    
    # Если не нашли — показываем список файлов, чтобы понять, где они
    return JSONResponse(content={
        "error": "index.html не найден",
        "where_am_i": os.getcwd(),
        "files_visible_to_bot": all_files
    })

# Монтируем корень для доступа к .wasm и .pck
app.mount("/", StaticFiles(directory="."), name="static")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
