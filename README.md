# 🖨️ ColabPrinter

Convert your Jupyter or Google Colab notebooks into **beautiful, print-ready PDFs** with just one click.

> No more ugly prints from the browser! 🚫🖨️ This tool makes your notebook submissions **look clean, professional, and shareable** — perfect for students, educators, and researchers.

---

## 🚀 Features

✅ Upload a `.ipynb` notebook file **OR** paste a Google Colab share link  
✅ Converts to high-quality **PDF** format using `nbconvert` + `WeasyPrint`  
✅ Works on mobile & desktop  
✅ Simple and clean user interface  
✅ Automatically deletes files after download (privacy-safe)  
✅ Free and open-source 🎉

---

## 🧑‍🎓 Who's This For?

- **Students** who need to submit Jupyter notebooks as proper PDFs
- **Teachers** who want neatly formatted assignment solutions
- **Anyone** tired of printing code with broken layouts from Colab or browser

---

## 🌐 Try It Live

**[🔗 https://colabprinter.onrender.com](https://colabprinter.onrender.com)**  
> (Link will work after deployment on Render)

---

## 📦 How It Works

1. Upload a `.ipynb` file OR paste a **Google Colab shareable link**
2. We fetch the notebook and convert it to HTML using `nbconvert`
3. We then use `WeasyPrint` to generate a PDF with clean layout and formatting
4. PDF is served to the user and the temp files are deleted

---

## 🛠️ Tech Stack

- Python 🐍
- Flask 🌶️
- nbconvert 📘
- WeasyPrint 🖨️
- HTML/CSS + Jinja2 templates

---

## 🧪 Run Locally

```bash
git clone https://github.com/sambhandavale/ColabPrinter.git
cd ColabPrinter
pip install -r requirements.txt
python app.py
