# PyCap Supplement Tracker

> **Disclaimer:** This is my first ever Python capstone project, and it's quite messy! It was built as a learning experience to explore Python fundamentals, JSON data handling, and basic application logic.

PyCap Supplement Tracker is a CLI-based application designed to help users manage their supplement inventory and track daily consumption automatically.

## 🚀 Features

- **Automatic Deduction:** Automatically calculates and deducts supplement consumption based on the time elapsed since your last login.
- **Inventory Management:** Add, edit, and delete supplements with details like type (Pill, Liquid, Sachet), dosage, and remarks.
- **Smart Restock Alerts:** Calculates how many days your current stock will last and provides an estimated restock date based on average delivery times.
- **"Time Travel" Correction:** Easily adjust your current stock if you forgot to log consumption for a few days.
- **Data Persistence:** All your supplement data and user information are saved locally in JSON files (`data.json` and `user_info.json`).
- **Interactive Menu:** A simple, number-based menu system for easy navigation.

## 🛠️ Project Structure

- `main.py`: The entry point of the application.
- `functions.py`: Contains the core logic for the menu and supplement management.
- `time_auto.py`: Handles time-based calculations and automatic deductions.
- `helper_functions.py`: Utility functions for input validation and ID generation.
- `load_dump_json.py`: Manages reading from and writing to JSON files.

## 📦 How to Use

1. Ensure you have Python installed.
2. Clone the repository:
   ```bash
   git clone https://github.com/myoihatsu/PyCap_SupplementTracker.git
   ```
3. Navigate to the project directory:
   ```bash
   cd PyCap_SupplementTracker
   ```
4. Run the application:
   ```bash
   python main.py
   ```

## 📝 Note

This project uses local JSON files for data storage. Make sure `data.json` and `user_info.json` are present in the root directory for the application to function correctly.
