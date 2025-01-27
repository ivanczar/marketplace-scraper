from webserver import create_app

PORT = 5000

app = create_app()

# Webserver entrypoint
if __name__ == "__main__":
    app.run(debug=True, port=PORT, host="0.0.0.0")
