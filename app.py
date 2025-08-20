from flask import Flask, render_template, request, send_file
import os
from utils.db import get_session
from utils.importer import import_excel
from utils.exporter import export_samples
from utils.models import File

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["OUTPUT_FOLDER"] = "outputs"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files["file"]
    if file:
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)

        db = get_session()
        try:
            new_file = File(filename=file.filename)
            db.add(new_file)
            db.commit()
            db.refresh(new_file)  # get the new file.id

            # Import Excel data
            import_excel(new_file.id, filepath, db)

            # Export processed samples
            output_path = export_samples(new_file.id, app.config["OUTPUT_FOLDER"], db)

            return send_file(output_path, as_attachment=True)
        finally:
            db.close()

if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)
    app.run(debug=True)
