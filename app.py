from app import app, db
from app.models import Item

app.config["SECRET_KEY"] = "my-super-secret-key"

@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "Item": Item,
    }
    
if __name__ == "__main__":
    app.run(debug=True)