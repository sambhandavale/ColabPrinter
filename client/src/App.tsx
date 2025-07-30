import React, { useState } from "react";
import axios from "axios";

const App: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [colabUrl, setColabUrl] = useState<string>("");
  const [error, setError] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if ((file && colabUrl) || (!file && !colabUrl)) {
      setError("❗ Please provide either a file or a Colab URL, not both.");
      return;
    }

    const formData = new FormData();
    if (file) formData.append("notebook", file);
    if (colabUrl) formData.append("colab_url", colabUrl);

    setLoading(true);
    setError("");

    try {
      const response = await axios.post("https://colabprinter-backend.onrender.com/convert", formData, {
        responseType: "blob",
      });

      const blob = new Blob([response.data], { type: "application/pdf" });
      const link = document.createElement("a");
      link.href = window.URL.createObjectURL(blob);
      link.download = "converted.pdf";
      link.click();
    } catch (err: any) {
      const msg = await err?.response?.data?.text?.();
      setError(msg || "Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <nav className="navbar">
        <span className="brand">📘 Notebook Converter</span>
        <a
          href="https://github.com/sambhandavale/ColabPrinter"
          target="_blank"
          rel="noopener noreferrer"
          className="github-link"
        >
          ⭐ Star on GitHub
        </a>
      </nav>

      <div className="container">
        <h1>Notebook to PDF Converter</h1>
        {error && <div className="error">{error}</div>}
        <form onSubmit={handleSubmit}>
          <label>Upload a .ipynb File</label>
          <input
            type="file"
            accept=".ipynb"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
          />

          <div className="divider">OR</div>

          <label>Paste Google Colab Notebook URL</label>
          <input
            type="text"
            placeholder="https://colab.research.google.com/..."
            value={colabUrl}
            onChange={(e) => setColabUrl(e.target.value)}
          />

          <button type="submit" disabled={loading}>
            {loading ? "Converting..." : "Convert to PDF"}
          </button>
        </form>
      </div>
    </>
  );

};

export default App;
