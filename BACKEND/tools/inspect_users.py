"""Utility script to inspect all registered users, chat history, and uploaded files in Zentora AI."""

import os
import sys

# Ensure backend root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database.database import SessionLocal
from app.models.user import User
from app.models.uploaded_file import UploadedFile
from app.models.history import History

def inspect():
    db = SessionLocal()
    try:
        users = db.query(User).all()
        print("\n" + "=" * 70)
        print(" " * 22 + "ZENTORA AI — REGISTERED USERS")
        print("=" * 70)
        
        if not users:
            print("No users registered yet.")
        else:
            for u in users:
                print(f"ID: {u.id} | Username: {u.username} | Email: {u.email}")
                print(f"   Role: {u.role} | Active: {u.is_active} | Created: {u.created_at}")
                
                # Check user uploaded files
                files = db.query(UploadedFile).filter(UploadedFile.user_id == u.id).all()
                if files:
                    print(f"   Uploaded Files ({len(files)}):")
                    for f in files:
                        print(f"     - {f.original_filename} ({round(f.file_size / 1024, 1)} KB) -> {f.file_path}")
                else:
                    print("   Uploaded Files: None")
                
                # Check conversation count
                chat_count = db.query(History).filter(History.user_id == u.id).count()
                print(f"   Saved Conversations: {chat_count}")
                print("-" * 70)

        # Uploads folder on disk
        uploads_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "uploads"))
        if os.path.exists(uploads_dir):
            disk_files = os.listdir(uploads_dir)
            print(f"\nPhysical files in '{uploads_dir}': {len(disk_files)} file(s)")
        print("=" * 70 + "\n")
    finally:
        db.close()

if __name__ == "__main__":
    inspect()
