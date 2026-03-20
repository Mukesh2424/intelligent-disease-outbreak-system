# yourapp/disease_detector.py

import re

def detect_disease(text):
    text = text.lower()
    if "covid" in text:
        return "covid", 0.9
    elif "dengue" in text:
        return "dengue", 0.85
    elif "flu" in text:
        return "flu", 0.8
    else:
        return "none", 0.0
