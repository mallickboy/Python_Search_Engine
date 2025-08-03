
# Python Search Engine (pysearch) Snap

PySearch is a fast, efficient, and easily deployable Python Search Engine packaged as a Snap. It is designed to be both **user-friendly** and **scalable**, allowing near-instant setup on any compatible Linux system.

---

## 📦 Snap Info

PySearch is available as a Snap package in two confinement modes:

| Version | Confinement | Description                                                                                              | Download Link |
|---------|-------------|----------------------------------------------------------------------------------------------------------|---------------|
| `1.4`   | `strict`    | Secure and sandboxed. Recommended for production use. May have some access limitations.                  | [Download](https://drive.google.com/file/d/1c9F2buxxc083r2wCDsyUP-KapKMfsiZw/view?usp=sharing) |
| `1.3`   | `devmode`   | More permissive (less secure), useful for development, debugging, or local testing.                      | [Download](https://drive.google.com/file/d/11Krzo-v8Fy4MFgLLY1vMbmavyVNLVunG/view?usp=sharing) |
---

## 🔧 Installation

### Install from local file:
```bash
sudo snap install --dangerous pysearch_1.4_amd64.snap  # strict version
# or
sudo snap install --dangerous pysearch_1.3_amd64.snap --devmode   # devmode version
```

To update:
```bash
sudo snap remove pysearch
sudo snap install --dangerous --devmode pysearch_1.3_amd64.snap
```

---

## 🚀 Usage

```bash
pysearch -h          # Show help
pysearch --config    # Configure environment interactively
pysearch             # Run the search engine server
```

---

## 📁 Project Structure

```
.
|-- README.md
|-- pysearch
|   |-- app.py
|   |-- config.py
|   |-- main.py
|   |-- search.py
|   |-- static
|   |   |-- css
|   |   |-- js
|   |-- templates
|       |-- index.html
|-- requirements.txt
|-- snap
|   |-- snapcraft.yaml
|-- start-pysearch
```

---

## 🔐 Environment Config (.env)

During the first run with `--config`, the following variables are prompted and stored at: `~/snap/pysearch/common/.env`

Environment values:
```env
PINECONE_KEY=your_key_here
PINECONE_ENVIRONMENT=your_env
HOST=0.0.0.0
PORT=8000
GUNICORN=True
GUNICORN_WORKERS=4
GET_RESULT_COUNT=50
```

Default fallback priority:
1. **User-edited value** from `.env`
2. If empty, fallback to **existing value** in `.env`
3. If still empty, use **default hardcoded value**

---

## ⚙️ Build Snap (for developers)

To build from source:

```bash
snapcraft pack --output installers/pysearch_1.4_amd64.snap
```

---

## ✅ Features

- Easy interactive config system
- Serves via Flask (or Gunicorn optionally)
- REST API with Pinecone-backed semantic search
- Works with both sandboxed and full-access modes
- Fast to scale across machines via Snap installs

---

## ⚠️ Known Warnings

In **strict mode**, due to limited access:
```
/snap/pysearch/x14/lib/python3.10/site-packages/joblib/_multiprocessing_helpers.py:44: UserWarning: [Errno 13] Permission denied.  joblib will operate in serial mode
  warnings.warn("%s.  joblib will operate in serial mode" % (e,))
```

---

## 📞 Support

For issues, open a GitHub issue or contact me.
