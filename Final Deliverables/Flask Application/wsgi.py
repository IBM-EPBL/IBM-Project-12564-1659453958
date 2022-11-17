"""Application entry point."""
from user_login import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response
