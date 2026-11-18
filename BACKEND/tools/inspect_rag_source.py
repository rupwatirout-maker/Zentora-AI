import os
import sqlite3
import traceback
from pathlib import Path

try:
    root = Path.cwd()
    print("BACKEND:", root)

    db_path = root / "chroma_db" / "chroma.sqlite3"
    print("\nDATABASE:", db_path)
    print("EXISTS:", db_path.exists())

    if db_path.exists():
        conn = sqlite3.connect(str(db_path))
        tables = {
            row[0] for row in
            conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        }

        if "embedding_metadata" in tables:
            print("\nMETADATA COUNTS:")
            for row in conn.execute(
                "SELECT key, COUNT(*) FROM embedding_metadata GROUP BY key"
            ):
                print(row)
        else:
            print("embedding_metadata table not found")

        conn.close()

    files = [
        "app/ai/rag/vector_store.py",
        "app/ai/rag/rag_service.py",
        "app/ai/rag/embedding_service.py",
        "app/ai/rag/document_processor.py",
        "app/ai/rag/text_splitter.py",
        "app/services/upload_service.py",
        "app/repositories/upload_repository.py",
        "app/api/upload.py",
        "app/ai/agents/agent_manager.py",
    ]

    for name in files:
        path = root / name
        print("\n" + "=" * 90)
        print("FILE:", name)
        print("=" * 90)

        if path.is_file():
            print(path.read_text(encoding="utf-8", errors="replace"))
        else:
            print("FILE NOT FOUND")

except Exception:
    traceback.print_exc()
    raise
