# AI-Powered Recognized Loss Calculator

## Overview
This project provides a dynamic tool to calculate recognized losses for clients based on settlement notices.  
It uses Python, Flask, HTML, and Gemini 2.5 LLM to compute losses accurately.

## Features
- Upload CSV/Excel files dynamically
- Client-wise and fund-wise recognized loss calculations
- AI-powered calculation logic (Gemini 2.5)
- Reusable for new client datasets

## File Structure
recognized_loss_calculator/
│
├─ templates/
│    ├─index.html    # HTML UI
├─ server.py        # Flask backend and calculation logic
├─ prompts.py       # Gemini AI prompts
├─ requirements.txt # Required Python packages
└─ README.md        # Documentation



## Usage
1. Install dependencies: `pip install -r requirements.txt`
2. Run the app: `python app.py`
3. Open `http://127.0.0.1:5000/` in your browser
4. Upload client transaction file
5. View recognized losses per client and fund

## Notes
- The dataset is dynamically handled; no hardcoding of input data.
- AI generates formulas based on settlement rules.



=========================================================================

recognized_loss_calculator/
│
├─ masked_twitter.csv   # csv
├─ app.py        # Flask backend and calculation logic