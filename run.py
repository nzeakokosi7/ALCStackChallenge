from app import app

app.run(port=4990, debug=app.config['DEBUG'])
