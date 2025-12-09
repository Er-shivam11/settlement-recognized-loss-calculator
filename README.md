## 📘 Overview

Welcome — this repository hosts a **AI-Powered Recognized Loss Calculator** designed for class-action settlement computations.

The project includes **two independent tools**:

---

### **1️⃣ Streamlit App (`App.py`)**

A full UI-based calculator where users upload a CSV, and the app:

* Cleans & structures the transaction data
* Sends the structured JSON + rules to OpenAI GPT-4.1
* Returns fund-wise recognized loss table
* Works like a real internal calculator tool

---

### **2️⃣ Prompt-Based Script (`prompt_app.py`)**

A very lightweight Python script:

* Loads CSV
* Converts to JSON payload
* Sends to OpenAI GPT-4.1
* Prints the recognized losses directly to console


---

## 📂 Repository Structure

```
recognized-loss-calculator/
│
├── app.py                    ← Streamlit UI app  
├── prompt_app.py        ← Standalone prompt-based loss calculator  
├── masked_twitter.csv           ← example client trade data  
├── requirements.txt          ← Python dependencies  
├── .env              ← template for API key  
├── .gitignore                ← ignore venv & cache  
└── README.md                 ← this file  
```

---

## 🔑 .env Setup

Create `.env`:

```
OPENAI_API_KEY=your_api_key_here
```

Never commit your real key — `.gitignore` already protects `.env`.

---

## 🧰 Requirements

Your `requirements.txt` should include:

```
streamlit
pandas
python-dotenv
openai
```



---

# ▶️ Running the Streamlit App (`App.py`)

### **1. Clone the repository**

```bash
git clone https://github.com/Er-shivam11/settlement-recognized-loss-calculator.git
cd settlement-recognized-loss-calculator
```

### **2. Create virtual environment**

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

### **3. Install dependencies**

```bash
pip install -r requirements.txt
```

### **4. Run the Streamlit app**

```bash
streamlit run app.py
```

The UI will open at:

```
http://localhost:8501
```

### **5. Upload CSV → Get Recognized Loss Table**

The model will respond with:

✔ A clean fund-wise table
✔ Explanation of computation
✔ Notes on zero-loss funds

---

# ▶️ Running the Standalone Script (`prompt_app.py`)

This script runs **without Streamlit**:

### **1. Ensure `.env` is set**

```
OPENAI_API_KEY=your_api_key_here
```

### **2. Run the script**

```bash
python prompt_app.py sample_data.csv
```

### **Output Example**

```
Fund 5   → $1,293
Fund 63  → $7,359

Explanation:
• FIFO matching applied
• Purchases outside class period ignored
• Held shares computed using decline cap
```

---

# 🎯 Why This Two-Tool Design Is Powerful

### **Streamlit App (`App.py`)**

✔ For end-users
✔ Upload CSV → Get losses
✔ UI-friendly & presentation-ready

### **Core Script (`prompt_app.py`)**

✔ For developers / analysts
✔ Quick debugging
✔ Easy integration in other pipelines
