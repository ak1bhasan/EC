# Install packages from the terminal, not inside the script:
#   python -m pip install PyMySQL
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
