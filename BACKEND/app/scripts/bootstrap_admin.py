"""One-time, explicit bootstrap for the first Velora administrator."""

import argparse
import sys

from sqlalchemy import func

from app.database.database import SessionLocal
from app.models.user import User


def bootstrap_admin(email: str) -> int:
    email = email.strip().lower()

    if not email:
        print("ERROR: An email address is required.")
        return 1

    db = SessionLocal()

    try:
        user = (
            db.query(User)
            .filter(func.lower(User.email) == email)
            .with_for_update()
            .first()
        )

        if user is None:
            print(f"ERROR: No existing account found for {email}.")
            return 1

        if not user.is_active:
            print("ERROR: The selected account is inactive.")
            return 1

        if (user.role or "").strip().lower() == "admin":
            print("This account is already an administrator. No changes made.")
            return 0

        existing_admins = (
            db.query(User)
            .filter(func.lower(User.role) == "admin")
            .count()
        )

        if existing_admins:
            print(
                "ERROR: An administrator already exists. "
                "Bootstrap will not create another administrator."
            )
            return 1

        print("\nAccount selected for promotion:")
        print(f"Email: {user.email}")
        print(f"Username: {user.username}")
        print(f"Current role: {user.role}")
        print("New role: admin")

        confirmation = input(
            f"\nType PROMOTE {email} to confirm: "
        ).strip()

        if confirmation != f"PROMOTE {email}":
            print("Confirmation did not match. No changes made.")
            return 1

        user.role = "admin"
        db.commit()
        db.refresh(user)

        print("\nADMIN BOOTSTRAP SUCCESSFUL")
        print(f"Account: {user.email}")
        print(f"Role: {user.role}")
        print("No other accounts were modified.")

        return 0

    except Exception as exc:
        db.rollback()
        print(f"BOOTSTRAP FAILED: {type(exc).__name__}: {exc}")
        return 1

    finally:
        db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Promote one existing Velora account to administrator."
    )
    parser.add_argument("--email", required=True)
    args = parser.parse_args()

    sys.exit(bootstrap_admin(args.email))
