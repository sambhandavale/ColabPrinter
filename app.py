from flask import Flask, request, send_file, render_template, after_this_request
import nbformat
from nbconvert import HTMLExporter
from weasyprint import HTML as WeasyHTML
from pathlib import Path
import tempfile
import os
import re
import requests

app = Flask(__name__)

def convert_ipynb_to_pdf(ipynb_file_path, output_pdf_path):
    with open(ipynb_file_path, 'r', encoding='utf-8') as f:
        notebook_node = nbformat.read(f, as_version=4)
    
    html_exporter = HTMLExporter()
    html_exporter.template_name = "lab"
    (body, _) = html_exporter.from_notebook_node(notebook_node)
    
    WeasyHTML(string=body).write_pdf(str(output_pdf_path))

def extract_drive_file_id(colab_url):
    match = re.search(r'/drive/([a-zA-Z0-9_-]+)', colab_url)
    return match.group(1) if match else None

def download_ipynb_from_drive(file_id, destination_path):
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    response = requests.get(url)
    if "text/html" in response.headers.get("Content-Type", ""):
        raise ValueError("⚠️ Could not download the file. Make sure it's shared publicly.")
    with open(destination_path, 'wb') as f:
        f.write(response.content)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files.get('notebook')
        colab_url = request.form.get('colab_url', '').strip()

        tmpdir = tempfile.mkdtemp()
        ipynb_path = None

        try:
            if file and file.filename.endswith('.ipynb'):
                ipynb_path = Path(tmpdir) / file.filename
                file.save(ipynb_path)

            elif colab_url:
                file_id = extract_drive_file_id(colab_url)
                if not file_id:
                    return render_template("index.html", error="❌ Could not extract file ID from the provided Colab URL.")

                ipynb_path = Path(tmpdir) / "downloaded_notebook.ipynb"
                download_ipynb_from_drive(file_id, ipynb_path)

            else:
                return render_template("index.html", error="❌ Please upload a file or provide a Colab URL.")

            pdf_path = ipynb_path.with_suffix('.pdf')
            convert_ipynb_to_pdf(ipynb_path, pdf_path)

            @after_this_request
            def cleanup(response):
                try:
                    os.remove(ipynb_path)
                    os.remove(pdf_path)
                    os.rmdir(tmpdir)
                except Exception as e:
                    print(f"Cleanup failed: {e}")
                return response

            return send_file(pdf_path, as_attachment=True, download_name=pdf_path.name)

        except Exception as e:
            return render_template("index.html", error=f"❌ Error: {str(e)}")

    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
