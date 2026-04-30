import os
from app import create_app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Changed from 5000 to 8000
    app.run(host="0.0.0.0", port=port, debug=True)