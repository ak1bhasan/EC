import os

from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv

load_dotenv()


def main():
    uri = os.environ.get(
        "DATABASE_URI", "mysql+pymysql://root:root@localhost:3306/ecommerce"
    )
    print(f"Using DATABASE_URI={uri!r}")

    engine = create_engine(uri, echo=False, pool_pre_ping=True)

    try:
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            print("Connection OK, SELECT 1 returned:", list(result))
    except OperationalError as exc:
        print("\n[ERROR] Could not connect to MySQL via SQLAlchemy.\n")
        print(exc)
        print(
            "\nCheck that:\n"
            "- MySQL is running on localhost:3306\n"
            "- The username/password in DATABASE_URI are correct\n"
            "- The 'ecommerce' database exists (or update the name in DATABASE_URI)\n"
        )


if __name__ == "__main__":
    main()
