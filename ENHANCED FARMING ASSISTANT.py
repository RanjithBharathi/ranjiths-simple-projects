import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
import datetime
from plyer import notification

# Function to load CSV file
def load_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print("File not found.")
        return None
    except Exception as e:
        print("Error occurred:", e)
        return None

# Function to find matching rows based on input data
def find_matching_rows(df, data):
    if df is None:
        return None
    
    data = [entry.strip().lower() for entry in data]  # Convert to lowercase and remove whitespace
    matching_rows = df[
        (df['State_Name'].str.strip().str.lower() == data[0]) &
        (df['District_Name'].str.strip().str.lower() == data[1]) &
        (df['Season'].str.strip().str.lower() == data[2])
    ]
    return matching_rows['Crop'] if 'Crop' in matching_rows.columns else pd.Series()

# Function to display crop information
def display_crop_info():
    crop_name = crop_entry.get()
    if crop_name in crop_data:
        crop_info = crop_data[crop_name]
        crop_window = tk.Toplevel(root)
        crop_window.title("Crop Information")
        
        for i, (heading, value) in enumerate(crop_info.items()):
            tk.Label(crop_window, text=heading, font=("Helvetica", 12, "bold")).grid(row=i, column=0, sticky="w", padx=5, pady=5)
            tk.Label(crop_window, text=value, wraplength=400).grid(row=i, column=1, sticky="w", padx=5, pady=5)
    else:
        messagebox.showerror("Error", "Crop not found in database.")

# Function to show search results
def show_results(df):
  
    data = [entry1.get(), entry2.get(), entry3.get()]
    crop_values = find_matching_rows(df, data)
    
    if not crop_values.empty:
        unique_crops = crop_values.unique()  # Filter out duplicate crop entries
        result_textbox.delete(1.0, tk.END)
        result_textbox.insert(tk.END, '\n'.join(unique_crops.astype(str)))
        crop_entry_label.grid(row=7, column=0, columnspan=2, padx=5, pady=5)
        crop_entry.grid(row=8, column=0, columnspan=2, padx=5, pady=5)
    else:
        result_textbox.delete(1.0, tk.END)
        result_textbox.insert(tk.END, "No matching rows found.")
        crop_entry_label.grid(row=7, column=0, columnspan=2, padx=5, pady=5)
        crop_entry.grid(row=8, column=0, columnspan=2, padx=5, pady=5)



# Function to calculate days since planting
def calculate_days_since_planting(start_date):
    try:
        start_date_obj = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
        today = datetime.datetime.now().date()
        days_diff = (today - start_date_obj).days
        return days_diff
    except ValueError:
        return None
    
    

# Function to check reminder for fertilization
def check_fertilizer_reminder():
    crop = crop_var.get()
    start_date = start_date_entry.get()
    days_since_planting = calculate_days_since_planting(start_date)
    
    if days_since_planting is not None and days_since_planting in crop_actions[crop]:
        action = crop_actions[crop][days_since_planting]
        messagebox.showinfo("Fertilizer Reminder", action)
    else:
        messagebox.showinfo("Fertilizer Reminder", f"No fertilizer action for {crop} today.")

    # Schedule the next reminder
    root.after(86400000, check_fertilizer_reminder)  # 86400000 milliseconds = 1 day

# Function to set watering reminder
def set_watering_reminder():
    crop_name = crop_entry.get()
    start_date = start_date_entry.get()
    end_date = end_date_entry.get()
    schedule_days = int(schedule_entry.get())

    # Convert start and end date strings to datetime objects
    start_date_obj = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_date_obj = datetime.datetime.strptime(end_date, "%Y-%m-%d")

    # Check if start date is before end date
    if start_date_obj >= end_date_obj:
        messagebox.showerror("Error", "End date must be after start date.")
        return

    # Calculate the reminder dates
    reminder_dates = []
    current_date = start_date_obj
    while current_date <= end_date_obj:
        reminder_dates.append(current_date)
        current_date += datetime.timedelta(days=schedule_days)

    # Send notifications on reminder dates
    for date in reminder_dates:
        notification_title = f"Water {crop_name}"
        notification_message = f"Don't forget to water your {crop_name} today!"
        notification.notify(
            title=notification_title,
            message=notification_message,
            app_name='Crop Watering Reminder'
        )

    # Show success message
    success_message = f"Reminders set for {crop_name}:\n"
    for date in reminder_dates:
        success_message += f"- {date.strftime('%Y-%m-%d')}\n"
    messagebox.showinfo("Success", success_message)
    root.after(86400000, set_watering_reminder) 

# Load CSV file
df = load_csv(r"D:\MINIPROJECT CSV\crop_production.csv.csv")

# Crop Information Dictionary
crop_data = {
    "Arhar/Tur": {
        "Watering Schedule": {"Frequency": "Every 2 days", "Number of Days": 2},
        "Soil Requirements": "Well-drained sandy loam soil",
        "Fertilizer": "Nitrogen, Phosphorus, Potassium",
        "Fertilization Period": "Before sowing, during flowering and pod formation",
        "Harvesting Time": "90-150 days after sowing",
        "Planting Procedure": "Sow seeds directly into the soil at a depth of 3-4 cm",
        "Planting Distance": "Rows spaced 60-90 cm apart, with 10-15 cm between plants"
    },
    "Bajra": {
        "Watering Schedule": {"Frequency": "Every 3 days", "Number of Days": 3},
        "Soil Requirements": "Sandy loam soil",
        "Fertilizer": "Nitrogen, Phosphorus, Potassium",
        "Fertilization Period": "At sowing and during growth stages",
        "Harvesting Time": "60-80 days after sowing",
        "Planting Procedure": "Sow seeds directly into the soil at a depth of 2-3 cm",
        "Planting Distance": "Rows spaced 30-45 cm apart, with 5-10 cm between plants"
    },
    "Banana": {
        "Watering Schedule": {"Frequency": "Every 4 days", "Number of Days": 4},
        "Soil Requirements": "Loamy soil with good drainage",
        "Fertilizer": "Nitrogen, Phosphorus, Potassium",
        "Fertilization Period": "Regularly throughout the year",
        "Harvesting Time": "9-12 months after planting",
        "Planting Procedure": "Plant suckers at a spacing of 2-3 meters between plants",
        "Planting Distance": "Rows spaced 3-4 meters apart"
    },
    "Cardamom": {
        "Watering Schedule": {"Frequency": "Every 3 days", "Number of Days": 3},
        "Soil Requirements": "Loamy soil with good organic matter",
        "Fertilizer": "Organic manure, Nitrogen, Phosphorus, Potassium",
        "Fertilization Period": "Three times a year",
        "Harvesting Time": "3-4 years after planting",
        "Planting Procedure": "Plant rhizomes in pits of 40 cm depth with a spacing of 2-3 meters between plants",
        "Planting Distance": "Rows spaced 2-3 meters apart"
    },
    "Cashewnut": {
        "Watering Schedule": {"Frequency": "Every 5 days", "Number of Days": 5},
        "Soil Requirements": "Well-drained sandy loam soil",
        "Fertilizer": "Organic manure, Nitrogen, Phosphorus, Potassium",
        "Fertilization Period": "First two years after planting",
        "Harvesting Time": "3-5 years after planting",
        "Planting Procedure": "Plant seeds or grafted seedlings at a spacing of 8-10 meters between plants",
        "Planting Distance": "Rows spaced 8-10 meters apart"
    },
    "Castor seed": {
        "Watering Schedule": {"Frequency": "Every 7 days", "Number of Days": 7},
        "Soil Requirements": "Well-drained sandy loam soil",
        "Fertilizer": "Organic manure, Nitrogen, Phosphorus, Potassium",
        "Fertilization Period": "At sowing and during growth stages",
        "Harvesting Time": "5-6 months after sowing",
        "Planting Procedure": "Sow seeds directly into the soil at a depth of 3-5 cm",
        "Planting Distance": "Rows spaced 90-120 cm apart, with 20-30 cm between plants"
    },
    "Coriander": {
        "Watering Schedule": {"Frequency": "Every 2 days", "Number of Days": 2},
        "Soil Requirements": "Well-drained sandy loam soil",
        "Fertilizer": "Nitrogen, Phosphorus, Potassium",
        "Fertilization Period": "Once at the time of sowing",
        "Harvesting Time": "45-70 days after sowing",
        "Planting Procedure": "Broadcast seeds or sow in furrows at a depth of 1-2 cm",
        "Planting Distance": "Rows spaced 20-30 cm apart"
    },
    "Cotton(lint)": {
        "Watering Schedule": {"Frequency": "Every 5 days", "Number of Days": 5},
        "Soil Requirements": "Sandy loam soil",
        "Fertilizer": "Nitrogen, Phosphorus, Potassium",
        "Fertilization Period": "At sowing and during growth stages",
        "Harvesting Time": "170-220 days after sowing",
        "Planting Procedure": "Sow seeds at a depth of 2-3 cm",
        "Planting Distance": "Rows spaced 90-120 cm apart, with 30-45 cm between plants"
    },
    "Dry chillies": {
        "Watering Schedule": {"Frequency": "Every 3 days", "Number of Days": 3},
        "Soil Requirements": "Sandy loam soil",
        "Fertilizer": "Nitrogen, Phosphorus, Potassium",
        "Fertilization Period": "At sowing and during growth stages",
        "Harvesting Time": "90-100 days after sowing",
        "Planting Procedure": "Sow seeds directly into the soil at a depth of 2-3 cm",
        "Planting Distance": "Rows spaced 45-60 cm apart, with 30-45 cm between plants"
    },
    "Groundnut": {
        "Watering Schedule": {"Frequency": "Every 4 days", "Number of Days": 4},
        "Soil Requirements": "Well-drained sandy loam soil",
        "Fertilizer": "Nitrogen, Phosphorus, Potassium",
        "Fertilization Period": "At sowing and during flowering",
        "Harvesting Time": "90-120 days after sowing",
        "Planting Procedure": "Sow seeds in ridges or flatbeds at a depth of 5-10 cm",
        "Planting Distance": "Rows spaced 30-45 cm apart, with 15-20 cm between plants"
    },
    "Jowar": {
        "Watering Schedule": {"Frequency": "Every 4 days", "Number of Days": 4},
        "Soil Requirements": "Sandy loam soil",
        "Fertilizer": "Nitrogen, Phosphorus, Potassium",
        "Fertilization Period": "At sowing and during growth stages",
        "Harvesting Time": "100-120 days after sowing",
        "Planting Procedure": "Sow seeds directly into the soil at a depth of 2-3 cm",
        "Planting Distance": "Rows spaced 30-45 cm apart, with 10-15 cm between plants"
    },
    "Maize": {
        "Watering Schedule": {"Frequency": "Every 3 days", "Number of Days": 3},
        "Soil Requirements": "Sandy loam soil",
        "Fertilizer": "Nitrogen, Phosphorus, Potassium",
        "Fertilization Period": "At sowing and during growth stages",
        "Harvesting Time": "70-80 days after sowing",
        "Planting Procedure": "Sow seeds directly into the soil at a depth of 3-5 cm",
        "Planting Distance": "Rows spaced 60-75 cm apart, with 20-30 cm between plants"
    },
    "Moong(Green Gram)": {
        "Watering Schedule": {"Frequency": "Every 2 days", "Number of Days": 2},
        "Soil Requirements": "Well-drained sandy loam soil",
        "Fertilizer": "Nitrogen, Phosphorus, Potassium",
        "Fertilization Period": "At sowing and during flowering",
        "Harvesting Time": "60-75 days after sowing",
        "Planting Procedure": "Sow seeds directly into the soil at a depth of 3-4 cm",
        "Planting Distance": "Rows spaced 45-60 cm apart, with 10-15 cm between plants"
    },
    "Onion": {
        "Watering Schedule": {"Frequency": "Every 4 days", "Number of Days": 4},
        "Soil Requirements": "Well-drained sandy loam soil",
        "Fertilizer": "Nitrogen, Phosphorus, Potassium",
        "Fertilization Period": "At sowing and during bulb formation",
        "Harvesting Time": "90-120 days after sowing",
        "Planting Procedure": "Plant bulbs or sets at a depth of 1-2 cm",
        "Planting Distance": "Rows spaced 15-30 cm apart, with 10-15 cm between plants"
    },
    "Pulses total": {
        "Watering Schedule": {"Frequency": "Every 2 days", "Number of Days": 2},
        "Soil Requirements": "Well-drained loamy soil",
        "Fertilizer": "Nitrogen, Phosphorus, Potassium",
        "Fertilization Period": "At sowing and during flowering",
        "Harvesting Time": "Varies depending on the pulse variety",
        "Planting Procedure": "Sow seeds directly into the soil at a depth of 3-5 cm",
        "Planting Distance": "Varies depending on the pulse variety"
    },
    "Ragi": {
        "Watering Schedule": {"Frequency": "Every 3 days", "Number of Days": 3},
        "Soil Requirements": "Sandy loam soil",
        "Fertilizer": "Nitrogen, Phosphorus, Potassium",
        "Fertilization Period": "At sowing and during growth stages",
        "Harvesting Time": "90-120 days after sowing",
        "Planting Procedure": "Sow seeds directly into the soil at a depth of 2-3 cm",
        "Planting Distance": "Rows spaced 20-30 cm apart, with 10-15 cm between plants"
    },
    "Rice": {
        "Watering Schedule": {"Frequency": "Every 2 days", "Number of Days": 2},
        "Soil Requirements": "Clayey soil",
        "Fertilizer": "Nitrogen, Phosphorus, Potassium",
        "Fertilization Period": "During land preparation, at sowing, and during tillering",
        "Harvesting Time": "120-150 days after sowing",
        "Planting Procedure": "Transplant seedlings in puddled soil",
        "Planting Distance": "Rows spaced 20-30 cm apart, with 15-20 cm between plants"
    },
    "Sugarcane": {
        "Watering Schedule": {"Frequency": "Every 7 days", "Number of Days": 7},
        "Soil Requirements": "Sandy loam soil",
        "Fertilizer": "Nitrogen, Phosphorus, Potassium",
        "Fertilization Period": "During land preparation and at regular intervals",
        "Harvesting Time": "10-12 months after planting",
        "Planting Procedure": "Plant setts or cuttings in furrows at a spacing of 0.9-1.2 meters",
        "Planting Distance": "Rows spaced 1.5-1.8 meters apart"
    },
    "Sunflower": {
        "Watering Schedule": {"Frequency": "Every 3 days", "Number of Days": 3},
        "Soil Requirements": "Well-drained loamy soil",
        "Fertilizer": "Nitrogen, Phosphorus, Potassium",
        "Fertilization Period": "At sowing and during flowering",
        "Harvesting Time": "90-120 days after sowing",
        "Planting Procedure": "Sow seeds directly into the soil at a depth of 2-3 cm",
        "Planting Distance": "Rows spaced 45-60 cm apart, with 20-30 cm between plants"
    },
    "Sweet potato": {
        "Watering Schedule": {"Frequency": "Every 4 days", "Number of Days": 4},
        "Soil Requirements": "Well-drained sandy loam soil",
        "Fertilizer": "Organic manure, Nitrogen, Phosphorus, Potassium",
        "Fertilization Period": "Once at the time of planting",
        "Harvesting Time": "3-5 months after planting",
        "Planting Procedure": "Plant vine cuttings or slips at a depth of 5-10 cm",
        "Planting Distance": "Rows spaced 60-90 cm apart, with 30-45 cm between plants"
    },
    "Tapioca": {
        "Watering Schedule": {"Frequency": "Every 5 days", "Number of Days": 5},
        "Soil Requirements": "Sandy loam soil",
        "Fertilizer": "Organic manure, Nitrogen, Phosphorus, Potassium",
        "Fertilization Period": "Once at the time of planting",
        "Harvesting Time": "8-10 months after planting",
        "Planting Procedure": "Plant stem cuttings horizontally in furrows at a spacing of 45-60 cm",
        "Planting Distance": "Rows spaced 90-120 cm apart"
    },
    "Tobacco": {
        "Watering Schedule": {"Frequency": "Every 6 days", "Number of Days": 6},
        "Soil Requirements": "Sandy loam soil",
        "Fertilizer": "Nitrogen, Phosphorus, Potassium",
        "Fertilization Period": "During land preparation and after transplanting",
        "Harvesting Time": "90-120 days after transplanting",
        "Planting Procedure": "Transplant seedlings in rows spaced 60-90 cm apart",
        "Planting Distance": "Rows spaced 60-90 cm apart, with 45-60 cm between plants"
    },
    "Total foodgrain": {
        "Watering Schedule": {"Frequency": "Every 3 days", "Number of Days": 3},
        "Soil Requirements": "Well-drained loamy soil",
        "Fertilizer": "Nitrogen, Phosphorus, Potassium",
        "Fertilization Period": "At sowing and during growth stages",
        "Harvesting Time": "Varies depending on the grain",
        "Planting Procedure": "Sow seeds directly into the soil at a depth of 3-5 cm",
        "Planting Distance": "Varies depending on the grain"
    },
    "Turmeric": {
        "Watering Schedule": {"Frequency": "Every 4 days", "Number of Days": 4},
        "Soil Requirements": "Loamy soil with good drainage",
        "Fertilizer": "Organic manure, Nitrogen, Phosphorus, Potassium",
        "Fertilization Period": "Once at the time of planting",
        "Harvesting Time": "8-10 months after planting",
        "Planting Procedure": "Plant rhizomes in pits of 20-30 cm depth with a spacing of 30-45 cm between plants",
        "Planting Distance": "Rows spaced 45-60 cm apart"
    },
    "Urad": {
        "Watering Schedule": {"Frequency": "Every 2 days", "Number of Days": 2},
        "Soil Requirements": "Well-drained sandy loam soil",
        "Fertilizer": "Nitrogen, Phosphorus, Potassium",
        "Fertilization Period": "At sowing and during flowering",
        "Harvesting Time": "70-90 days after sowing",
        "Planting Procedure": "Sow seeds directly into the soil at a depth of 3-4 cm",
        "Planting Distance": "Rows spaced 30-45 cm apart, with 10-15 cm between plants"
    },
    "Black pepper": {
        "Watering Schedule": {"Frequency": "Every 3 days", "Number of Days": 3},
        "Soil Requirements": "Loamy soil with good organic matter",
        "Fertilizer": "Organic manure, Nitrogen, Phosphorus, Potassium",
        "Fertilization Period": "Three times a year",
        "Harvesting Time": "3-4 years after planting",
        "Planting Procedure": "Plant cuttings or rooted vine segments in pits of 50 cm depth with a spacing of 2-3 meters between plants",
        "Planting Distance": "Rows spaced 2-3 meters apart"
    },
    "Guar seed": {
        "Watering Schedule": {"Frequency": "Every 5 days", "Number of Days": 5},
        "Soil Requirements": "Sandy loam soil",
        "Fertilizer": "Nitrogen, Phosphorus, Potassium",
        "Fertilization Period": "At sowing and during flowering",
        "Harvesting Time": "90-110 days after sowing",
        "Planting Procedure": "Sow seeds directly into the soil at a depth of 2-3 cm",
        "Planting Distance": "Rows spaced 30-45 cm apart, with 15-20 cm between plants"
    },
    "Potato": {
        "Watering Schedule": {"Frequency": "Every 4 days", "Number of Days": 4},
        "Soil Requirements": "Well-drained sandy loam soil",
        "Fertilizer": "Nitrogen, Phosphorus, Potassium",
        "Fertilization Period": "During land preparation and after planting",
        "Harvesting Time": "90-120 days after planting",
        "Planting Procedure": "Plant seed tubers in trenches or furrows at a spacing of 30-45 cm",
        "Planting Distance": "Rows spaced 60-75 cm apart"
    },
    "Arecanut": {
        "Watering Schedule": {"Frequency": "Every 4 days", "Number of Days": 4},
        "Soil Requirements": "Sandy loam soil",
        "Fertilizer": "Nitrogen, Phosphorus, Potassium",
        "Fertilization Period": "Two to three times a year",
        "Harvesting Time": "3-5 years after planting",
        "Planting Procedure": "Plant suckers or seedlings at a spacing of 2-3 meters between plants",
        "Planting Distance": "Rows spaced 3-4 meters apart"
    },
    "Ash Gourd": {
        "Watering Schedule": {"Frequency": "Every 5 days", "Number of Days": 5},
        "Soil Requirements": "Well-drained loamy soil",
        "Fertilizer": "Organic manure, Nitrogen, Phosphorus, Potassium",
        "Fertilization Period": "At sowing and during growth stages",
        "Harvesting Time": "80-100 days after sowing",
        "Planting Procedure": "Sow seeds directly into the soil at a depth of 2-3 cm",
        "Planting Distance": "Rows spaced 90-120 cm apart, with 60-75 cm between plants"
    },
    "Beans & Mutter(Vegetable)": {
        "Watering Schedule": {"Frequency": "Every 3 days", "Number of Days": 3},
        "Soil Requirements": "Loamy soil with good drainage",
        "Fertilizer": "Organic manure, Nitrogen, Phosphorus, Potassium",
        "Fertilization Period": "At sowing and during growth stages",
        "Harvesting Time": "60-80 days after sowing",
        "Planting Procedure": "Direct sow seeds or transplant seedlings",
        "Planting Distance": "Rows spaced 45-60 cm apart, with 15-20 cm between plants"
    },
    "Beet Root": {
        "Watering Schedule": {"Frequency": "Every 4 days", "Number of Days": 4},
        "Soil Requirements": "Loamy soil with good organic matter",
        "Fertilizer": "Organic manure, Nitrogen, Phosphorus, Potassium",
        "Fertilization Period": "At sowing and during growth stages",
        "Harvesting Time": "50-70 days after sowing",
        "Planting Procedure": "Direct sow seeds or transplant seedlings",
        "Planting Distance": "Rows spaced 30-45 cm apart, with 5-10 cm between plants"
    },
    "Bhindi": {
        "Watering Schedule": {"Frequency": "Every 3 days", "Number of Days": 3},
        "Soil Requirements": "Loamy soil with good drainage",
        "Fertilizer": "Organic manure, Nitrogen, Phosphorus, Potassium",
        "Fertilization Period": "At sowing and during growth stages",
        "Harvesting Time": "45-60 days after sowing",
        "Planting Procedure": "Direct sow seeds or transplant seedlings",
        "Planting Distance": "Rows spaced 45-60 cm apart, with 30-45 cm between plants"
    },
    "Bitter Gourd": {
        "Watering Schedule": {"Frequency": "Every 2 days", "Number of Days": 2},
        "Soil Requirements": "Loamy soil with good drainage",
        "Fertilizer": "Organic manure, Nitrogen, Phosphorus, Potassium",
        "Fertilization Period": "At sowing and during growth stages",
        "Harvesting Time": "45-60 days after sowing",
        "Planting Procedure": "Direct sow seeds or transplant seedlings",
        "Planting Distance": "Rows spaced 150-180 cm apart, with 60-75 cm between plants"
    },
    "Bottle Gourd": {
        "Watering Schedule": {"Frequency": "Every 3 days", "Number of Days": 3},
        "Soil Requirements": "Loamy soil with good drainage",
        "Fertilizer": "Organic manure, Nitrogen, Phosphorus, Potassium",
        "Fertilization Period": "At sowing and during growth stages",
        "Harvesting Time": "45-60 days after sowing",
        "Planting Procedure": "Direct sow seeds or transplant seedlings",
        "Planting Distance": "Rows spaced 180-210 cm apart, with 60-75 cm between plants"
    },
    "Brinjal": {
        "Watering Schedule": {"Frequency": "Every 3 days", "Number of Days": 3},
        "Soil Requirements": "Loamy soil with good drainage",
        "Fertilizer": "Organic manure, Nitrogen, Phosphorus, Potassium",
        "Fertilization Period": "At sowing and during growth stages",
        "Harvesting Time": "60-75 days after transplanting",
        "Planting Procedure": "Transplant seedlings",
        "Planting Distance": "Rows spaced 60-75 cm apart, with 45-60 cm between plants"
    },
    "Cabbage": {
        "Watering Schedule": {"Frequency": "Every 3 days", "Number of Days": 3},
        "Soil Requirements": "Loamy soil with good drainage",
        "Fertilizer": "Organic manure, Nitrogen, Phosphorus, Potassium",
        "Fertilization Period": "At sowing and during growth stages",
        "Harvesting Time": "60-90 days after transplanting",
        "Planting Procedure": "Transplant seedlings",
        "Planting Distance": "Rows spaced 45-60 cm apart, with 30-45 cm between plants"
    },
    "Cauliflower": {
        "Watering Schedule": {"Frequency": "Every 3 days", "Number of Days": 3},
        "Soil Requirements": "Loamy soil with good drainage",
        "Fertilizer": "Organic manure, Nitrogen, Phosphorus, Potassium",
        "Fertilization Period": "At sowing and during growth stages",
        "Harvesting Time": "60-90 days after transplanting",
        "Planting Procedure": "Transplant seedlings",
        "Planting Distance": "Rows spaced 45-60 cm apart, with 30-45 cm between plants"
    },
    "Citrus Fruit": {
        "Watering Schedule": {"Frequency": "Every 7 days", "Number of Days": 7},
        "Soil Requirements": "Well-drained loamy soil",
        "Fertilizer": "Organic manure, Nitrogen, Phosphorus, Potassium",
        "Fertilization Period": "Four times a year",
        "Harvesting Time": "Varies depending on the citrus variety",
        "Planting Procedure": "Plant grafted seedlings in pits of 45-60 cm depth with a spacing of 5-6 meters between plants",
        "Planting Distance": "Rows spaced 5-6 meters apart"
    },
    "Coconut": {
        "Watering Schedule": {"Frequency": "Every 7 days", "Number of Days": 7},
        "Soil Requirements": "Well-drained sandy loam soil",
        "Fertilizer": "Organic manure, Nitrogen, Phosphorus, Potassium",
        "Fertilization Period": "Twice a year",
        "Harvesting Time": "5-6 years after planting",
        "Planting Procedure": "Plant seedlings in pits of 60-90 cm depth with a spacing of 7-9 meters between plants",
        "Planting Distance": "Rows spaced 7-9 meters apart"
    },
    "Cucumber": {
        "Watering Schedule": {"Frequency": "Every 2 days", "Number of Days": 2},
        "Soil Requirements": "Loamy soil with good drainage",
        "Fertilizer": "Organic manure, Nitrogen, Phosphorus, Potassium",
        "Fertilization Period": "At sowing and during growth stages",
        "Harvesting Time": "45-60 days after sowing",
        "Planting Procedure": "Direct sow seeds or transplant seedlings",
        "Planting Distance": "Rows spaced 60-75 cm apart, with 30-45 cm between plants"
    },
    "Drum Stick": {
        "Watering Schedule": {"Frequency": "Every 4 days", "Number of Days": 4},
        "Soil Requirements": "Sandy loam soil",
        "Fertilizer": "Organic manure, Nitrogen, Phosphorus, Potassium",
        "Fertilization Period": "During land preparation and at regular intervals",
        "Harvesting Time": "9-12 months after planting",
        "Planting Procedure": "Plant seeds or seedlings at a spacing of 2-3 meters between plants",
        "Planting Distance": "Rows spaced 3-4 meters apart"
    },
    "Grapes": {
        "Watering Schedule": {"Frequency": "Every 7 days", "Number of Days": 7},
        "Soil Requirements": "Well-drained loamy soil",
        "Fertilizer": "Organic manure, Nitrogen, Phosphorus, Potassium",
        "Fertilization Period": "During the growing season",
        "Harvesting Time": "2-3 years after planting",
        "Planting Procedure": "Plant grafted seedlings in pits of 60-90 cm depth with a spacing of 2-3 meters between plants",
        "Planting Distance": "Rows spaced 2-3 meters apart"
    },
    "Jack Fruit": {
        "Watering Schedule": {"Frequency": "Every 4 days", "Number of Days": 4},
        "Soil Requirements": "Well-drained loamy soil",
        "Fertilizer": "Organic manure, Nitrogen, Phosphorus, Potassium",
        "Fertilization Period": "During land preparation and at regular intervals",
        "Harvesting Time": "4-6 years after planting",
        "Planting Procedure": "Plant seeds or seedlings in pits of 90-120 cm depth with a spacing of 8-10 meters between plants",
        "Planting Distance": "Rows spaced 8-10 meters apart"
    },
    "Lab-Lab": {
        "Watering Schedule": {"Frequency": "Every 5 days", "Number of Days": 5},
        "Soil Requirements": "Sandy loam soil",
        "Fertilizer": "Nitrogen, Phosphorus, Potassium",
        "Fertilization Period": "At sowing and during growth stages",
        "Harvesting Time": "70-90 days after sowing",
        "Planting Procedure": "Sow seeds directly into the soil at a depth of 2-3 cm",
        "Planting Distance": "Rows spaced 60-75 cm apart, with 30-45 cm between plants"
    },
    "Mango": {
        "Watering Schedule": {"Frequency": "Every 7 days", "Number of Days": 7},
        "Soil Requirements": "Well-drained loamy soil",
        "Fertilizer": "Organic manure, Nitrogen, Phosphorus, Potassium",
        "Fertilization Period": "Three times a year",
        "Harvesting Time": "3-5 years after planting",
        "Planting Procedure": "Plant grafted seedlings in pits of 1 meter depth with a spacing of 8-10 meters between plants",
        "Planting Distance": "Rows spaced 8-10 meters apart"
    },
    "Orange": {
        "Watering Schedule": {"Frequency": "Every 5 days", "Number of Days": 5},
        "Soil Requirements": "Well-drained loamy soil",
        "Fertilizer": "Organic manure, Nitrogen, Phosphorus, Potassium",
        "Fertilization Period": "Three times a year",
        "Harvesting Time": "3-5 years after planting",
        "Planting Procedure": "Plant grafted seedlings in pits of 60-90 cm depth with a spacing of 6-7 meters between plants",
        "Planting Distance": "Rows spaced 6-7 meters apart"
    },
    "Other Citrus Fruit": {
        "Watering Schedule": {"Frequency": "Every 7 days", "Number of Days": 7},
        "Soil Requirements": "Well-drained loamy soil",
        "Fertilizer": "Organic manure, Nitrogen, Phosphorus, Potassium",
        "Fertilization Period": "Three times a year",
        "Harvesting Time": "Varies depending on the citrus variety",
        "Planting Procedure": "Plant grafted seedlings in pits of 45-60 cm depth with a spacing of 5-6 meters between plants",
        "Planting Distance": "Rows spaced 5-6 meters apart"
    },
    "Other Fresh Fruits": {
        "Watering Schedule": {"Frequency": "Varies", "Number of Days": "Varies"},
        "Soil Requirements": "Varies",
        "Fertilizer": "Varies",
        "Fertilization Period": "Varies",
        "Harvesting Time": "Varies",
        "Planting Procedure": "Varies",
        "Planting Distance": "Varies"
    },
    "Other Vegetables": {
        "Watering Schedule": {"Frequency": "Varies", "Number of Days": "Varies"},
        "Soil Requirements": "Varies",
        "Fertilizer": "Varies",
        "Fertilization Period": "Varies",
        "Harvesting Time": "Varies",
        "Planting Procedure": "Varies",
        "Planting Distance": "Varies"
    },
    "Papaya": {
        "Watering Schedule": {"Frequency": "Every 3 days", "Number of Days": 3},
        "Soil Requirements": "Loamy soil with good drainage",
        "Fertilizer": "Organic manure, Nitrogen, Phosphorus, Potassium",
        "Fertilization Period": "At sowing and during growth stages",
        "Harvesting Time": "7-9 months after planting",
        "Planting Procedure": "Plant seeds or seedlings in pits of 45-60 cm depth with a spacing of 2-3 meters between plants",
        "Planting Distance": "Rows spaced 2-3 meters apart"
    },
    "Pome Fruit": {
        "Watering Schedule": {"Frequency": "Every 5 days", "Number of Days": 5},
        "Soil Requirements": "Well-drained loamy soil",
        "Fertilizer": "Organic manure, Nitrogen, Phosphorus, Potassium",
        "Fertilization Period": "Three times a year",
        "Harvesting Time": "3-5 years after planting",
        "Planting Procedure": "Plant grafted seedlings in pits of 60-90 cm depth with a spacing of 6-7 meters between plants",
        "Planting Distance": "Rows spaced 6-7 meters apart"
    },
    "Pome Granet": {
        "Watering Schedule": {"Frequency": "Every 5 days", "Number of Days": 5},
        "Soil Requirements": "Well-drained loamy soil",
        "Fertilizer": "Organic manure, Nitrogen, Phosphorus, Potassium",
        "Fertilization Period": "Three times a year",
        "Harvesting Time": "3-5 years after planting",
        "Planting Procedure": "Plant grafted seedlings in pits of 60-90 cm depth with a spacing of 6-7 meters between plants",
        "Planting Distance": "Rows spaced 6-7 meters apart"
    },
    "Pump Kin": {
        "Watering Schedule": {"Frequency": "Every 5 days", "Number of Days": 5},
        "Soil Requirements": "Loamy soil with good drainage",
        "Fertilizer": "Organic manure, Nitrogen, Phosphorus, Potassium",
        "Fertilization Period": "At sowing and during growth stages",
        "Harvesting Time": "90-120 days after sowing",
        "Planting Procedure": "Direct sow seeds",
        "Planting Distance": "Rows spaced 180-210 cm apart, with 90-120 cm between plants"
    },
    "Ribed Guard": {
        "Watering Schedule": {"Frequency": "Every 5 days", "Number of Days": 5},
        "Soil Requirements": "Loamy soil with good drainage",
        "Fertilizer": "Organic manure, Nitrogen, Phosphorus, Potassium",
        "Fertilization Period": "At sowing and during growth stages",
        "Harvesting Time": "60-80 days after sowing",
        "Planting Procedure": "Direct sow seeds or transplant seedlings",
        "Planting Distance": "Rows spaced 180-210 cm apart, with 90-120 cm between plants"
    },
    "Snak Guard": {
        "Watering Schedule": {"Frequency": "Every 5 days", "Number of Days": 5},
        "Soil Requirements": "Loamy soil with good drainage",
        "Fertilizer": "Organic manure, Nitrogen, Phosphorus, Potassium",
        "Fertilization Period": "At sowing and during growth stages",
        "Harvesting Time": "60-80 days after sowing",
        "Planting Procedure": "Direct sow seeds or transplant seedlings",
        "Planting Distance": "Rows spaced 180-210 cm apart, with 90-120 cm between plants"
    },
    "Tomato": {
        "Watering Schedule": {"Frequency": "Every 2 days", "Number of Days": 2},
        "Soil Requirements": "Loamy soil with good drainage",
        "Fertilizer": "Organic manure, Nitrogen, Phosphorus, Potassium",
        "Fertilization Period": "At sowing and during growth stages",
        "Harvesting Time": "60-80 days after transplanting",
        "Planting Procedure": "Transplant seedlings",
        "Planting Distance": "Rows spaced 60-75 cm apart, with 30-45 cm between plants"
    },
    "Water Melon": {
        "Watering Schedule": {"Frequency": "Every 3 days", "Number of Days": 3},
        "Soil Requirements": "Loamy soil with good drainage",
        "Fertilizer": "Organic manure, Nitrogen, Phosphorus, Potassium",
        "Fertilization Period": "At sowing and during growth stages",
        "Harvesting Time": "70-90 days after sowing",
        "Planting Procedure": "Direct sow seeds or transplant seedlings",
        "Planting Distance": "Rows spaced 180-210 cm apart, with 90-120 cm between plants"
    },
    "Yam": {
        "Watering Schedule": {"Frequency": "Every 4 days", "Number of Days": 4},
        "Soil Requirements": "Loamy soil with good drainage",
        "Fertilizer": "Organic manure, Nitrogen, Phosphorus, Potassium",
        "Fertilization Period": "At sowing and during growth stages",
        "Harvesting Time": "6-8 months after planting",
        "Planting Procedure": "Plant tubers in pits or mounds",
        "Planting Distance": "Rows spaced 90-120 cm apart, with 60-75 cm between plants"
    },
    "Plums": {
        "Watering Schedule": {"Frequency": "Every 7 days", "Number of Days": 7},
        "Soil Requirements": "Well-drained loamy soil",
        "Fertilizer": "Organic manure, Nitrogen, Phosphorus, Potassium",
        "Fertilization Period": "Three times a year",
        "Harvesting Time": "3-5 years after planting",
        "Planting Procedure": "Plant grafted seedlings in pits of 60-90 cm depth with a spacing of 6-7 meters between plants",
        "Planting Distance": "Rows spaced 6-7 meters apart"
    },
    "Redish": {
        "Watering Schedule": {"Frequency": "Every 4 days", "Number of Days": 4},
        "Soil Requirements": "Loamy soil with good drainage",
        "Fertilizer": "Organic manure, Nitrogen, Phosphorus, Potassium",
        "Fertilization Period": "At sowing and during growth stages",
        "Harvesting Time": "30-45 days after sowing",
        "Planting Procedure": "Direct sow seeds",
        "Planting Distance": "Rows spaced 15-20 cm apart, with 5-10 cm between plants"
    },
    "Horse-gram": {
        "Watering Schedule": {"Frequency": "Every 3 days", "Number of Days": 3},
        "Soil Requirements": "Sandy loam soil",
        "Fertilizer": "Nitrogen, Phosphorus, Potassium",
        "Fertilization Period": "At sowing and during flowering",
        "Harvesting Time": "90-110 days after sowing",
        "Planting Procedure": "Sow seeds directly into the soil at a depth of 2-3 cm",
        "Planting Distance": "Rows spaced 30-45 cm apart, with 10-15 cm between plants"
    },
    "Sesamum": {
        "Watering Schedule": {"Frequency": "Every 4 days", "Number of Days": 4},
        "Soil Requirements": "Sandy loam soil",
        "Fertilizer": "Nitrogen, Phosphorus, Potassium",
        "Fertilization Period": "At sowing and during flowering",
        "Harvesting Time": "90-120 days after sowing",
        "Planting Procedure": "Sow seeds directly into the soil at a depth of 2-3 cm",
        "Planting Distance": "Rows spaced 45-60 cm apart, with 15-20 cm between plants"
    },
    "Small millets": {
        "Watering Schedule": {"Frequency": "Every 3 days", "Number of Days": 3},
        "Soil Requirements": "Well-drained loamy soil",
        "Fertilizer": "Nitrogen, Phosphorus, Potassium",
        "Fertilization Period": "At sowing and during growth stages",
        "Harvesting Time": "70-90 days after sowing",
        "Planting Procedure": "Sow seeds directly into the soil at a depth of 2-3 cm",
        "Planting Distance": "Rows spaced 15-20 cm apart, with 5-10 cm between plants"
    },
    "Gram": {
        "Watering Schedule": {"Frequency": "Every 5 days", "Number of Days": 5},
        "Soil Requirements": "Sandy loam soil",
        "Fertilizer": "Nitrogen, Phosphorus, Potassium",
        "Fertilization Period": "At sowing and during flowering",
        "Harvesting Time": "90-110 days after sowing",
        "Planting Procedure": "Sow seeds directly into the soil at a depth of 2-3 cm",
        "Planting Distance": "Rows spaced 30-45 cm apart, with 10-15 cm between plants"
    }
}

# Fertilizer Schedule Dictionary
crop_actions = {
    # Include fertilizer schedule for crops
    "Arhar/Tur": {
        0: "Apply phosphorus and potassium fertilizer (e.g., 10-26-26) at planting time.",
        30: "Side-dress with nitrogen fertilizer."
    },
    "Bajra": {
        0: "Apply a balanced fertilizer (e.g., 10-10-10) at planting time.",
        20: "Side-dress with nitrogen fertilizer."
    },
    "Banana": {
        0: "Apply a balanced fertilizer (e.g., 6-6-12) at planting time.",
        60: "Apply a fertilizer high in potassium (e.g., 0-0-50)."
    },
    "Cardamom": {
        0: "Apply a slow-release fertilizer at planting time.",
        90: "Apply organic fertilizer or compost."
    },
    "Cashewnut": {
        0: "Apply a balanced fertilizer (e.g., 12-6-12) at planting time.",
        60: "Apply a fertilizer high in potassium (e.g., 0-0-50)."
    },
    "Castor seed": {
        0: "Apply a balanced fertilizer (e.g., 10-10-10) at planting time.",
        30: "Side-dress with nitrogen fertilizer."
    },
    "Coriander": {
        0: "Apply a balanced fertilizer (e.g., 10-10-10) at planting time.",
        15: "Apply nitrogen fertilizer (e.g., urea)."
    },
    "Cotton(lint)": {
        0: "Apply a balanced fertilizer (e.g., 10-10-10) at planting time.",
        30: "Side-dress with nitrogen fertilizer."
    },
    "Dry chillies": {
        0: "Apply a balanced fertilizer (e.g., 10-10-10) at planting time.",
        20: "Side-dress with nitrogen fertilizer."
    },
    "Groundnut": {
        0: "Apply a balanced fertilizer (e.g., 10-10-10) at planting time.",
        30: "Side-dress with nitrogen fertilizer."
    },
    "Jowar": {
        0: "Apply a balanced fertilizer (e.g., 10-10-10) at planting time.",
        20: "Side-dress with nitrogen fertilizer."
    },
    "Maize": {
        0: "Apply a balanced fertilizer (e.g., 10-10-10) at planting time.",
        30: "Side-dress with nitrogen fertilizer."
    },
    "Moong(Green Gram)": {
        0: "Apply a balanced fertilizer (e.g., 10-10-10) at planting time.",
        30: "Side-dress with nitrogen fertilizer."
    },
    "Onion": {
        0: "Apply a balanced fertilizer (e.g., 10-10-10) at planting time.",
        30: "Side-dress with nitrogen fertilizer."
    },
    "Ragi": {
        0: "Apply a balanced fertilizer (e.g., 10-10-10) at planting time.",
        30: "Side-dress with nitrogen fertilizer."
    },
    "Rice": {
        0: "Apply nitrogen fertilizer (e.g., urea) at planting time.",
        20: "Apply a topdressing of nitrogen fertilizer."
    },
    "Sugarcane": {
        0: "Apply a balanced fertilizer (e.g., 12-32-16) at planting time.",
        60: "Apply a fertilizer high in potassium (e.g., 0-0-50)."
    },
    "Sunflower": {
        0: "Apply a balanced fertilizer (e.g., 10-10-10) at planting time.",
        30: "Side-dress with nitrogen fertilizer."
    },
    "Sweet potato": {
        0: "Apply a balanced fertilizer (e.g., 10-10-10) at planting time.",
        30: "Side-dress with nitrogen fertilizer."
    },
    "Tapioca": {
        0: "Apply a balanced fertilizer (e.g., 10-10-10) at planting time.",
        30: "Side-dress with nitrogen fertilizer."
    },
    "Tobacco": {
        0: "Apply a balanced fertilizer (e.g., 10-10-10) at planting time.",
        30: "Side-dress with nitrogen fertilizer."
    },
    "Turmeric": {
        0: "Apply a balanced fertilizer (e.g., 10-10-10) at planting time.",
        30: "Apply a fertilizer high in potassium (e.g., 0-0-50)."
    },
    "Urad": {
        0: "Apply a balanced fertilizer (e.g., 10-10-10) at planting time.",
        30: "Side-dress with nitrogen fertilizer."
    },
    "Black pepper": {
        0: "Apply a balanced fertilizer (e.g., 10-10-10) at planting time.",
        30: "Apply organic compost."
    },
    "Guar seed": {
        0: "Apply a balanced fertilizer (e.g., 10-10-10) at planting time.",
        30: "Side-dress with nitrogen fertilizer."
    },
    "Potato": {
        0: "Apply a balanced fertilizer (e.g., 10-10-10) at planting time.",
        30: "Hill-up soil and side-dress with nitrogen fertilizer."
    },
    "Arecanut": {
        0: "Apply a balanced fertilizer (e.g., 10-10-10) at planting time.",
        60: "Apply a fertilizer high in potassium (e.g., 0-0-50)."
    },
    "Ash Gourd": {
        0: "Apply a balanced fertilizer (e.g., 10-10-10) at planting time.",
        30: "Side-dress with nitrogen fertilizer."
    },
    "Beans & Mutter(Vegetable)": {
        0: "Apply a balanced fertilizer (e.g., 10-10-10) at planting time.",
        30: "Side-dress with nitrogen fertilizer and provide support."
    },
    "Beet Root": {
        0: "Apply a balanced fertilizer (e.g., 10-10-10) at planting time.",
        30: "Side-dress with nitrogen fertilizer."
    },
    "Bhindi": {
        0: "Apply a balanced fertilizer (e.g., 10-10-10) at planting time.",
        30: "Side-dress with nitrogen fertilizer and provide support."
    },
    "Bitter Gourd": {
        0: "Apply a balanced fertilizer (e.g., 10-10-10) at planting time.",
        30: "Side-dress with nitrogen fertilizer and provide support."
    },
    "Bottle Gourd": {
        0: "Apply a balanced fertilizer (e.g., 10-10-10) at planting time.",
        30: "Side-dress with nitrogen fertilizer and provide support."
    },
    "Brinjal": {
        0: "Apply a balanced fertilizer (e.g., 10-10-10) at planting time.",
        30: "Side-dress with nitrogen fertilizer and provide support."
    },
    "Cabbage": {
        0: "Apply a balanced fertilizer (e.g., 10-10-10) at planting time.",
        30: "Side-dress with nitrogen fertilizer."
    },
    "Cauliflower": {
        0: "Apply a balanced fertilizer (e.g., 10-10-10) at planting time.",
        30: "Side-dress with nitrogen fertilizer."
    },
    "Citrus Fruit": {
        0: "Apply a balanced fertilizer (e.g., 10-10-10) at planting time.",
        60: "Apply a fertilizer high in potassium (e.g., 0-0-50)."
    },
    "Coconut": {
        0: "Apply a balanced fertilizer (e.g., 12-6-12) at planting time.",
        60: "Apply a fertilizer high in potassium (e.g., 0-0-50)."
    },
    "Cucumber": {
        0: "Apply a balanced fertilizer (e.g., 10-10-10) at planting time.",
        20: "Side-dress with nitrogen fertilizer."
    },
    "Drum Stick": {
        0: "Apply a balanced fertilizer (e.g., 10-10-10) at planting time.",
        30: "Apply organic compost."
    },
    "Grapes": {
        0: "Apply a balanced fertilizer (e.g., 10-10-10) at planting time.",
        90: "Apply a fertilizer high in potassium (e.g., 0-0-50)."
    },
    "Jack Fruit": {
        0: "Apply a balanced fertilizer (e.g., 10-10-10) at planting time.",
        60: "Apply a fertilizer high in potassium (e.g., 0-0-50)."
    },
    "Lab-Lab": {
        0: "Apply a balanced fertilizer (e.g., 10-10-10) at planting time.",
        60: "Apply a balanced slow-release fertilizer."
    },
    "Mango": {
        0: "Apply a balanced fertilizer (e.g., 10-10-10) at planting time.",
        60: "Apply a fertilizer high in potassium (e.g., 0-0-50)."
    },
    "Orange": {
        0: "Apply a balanced fertilizer (e.g., 10-10-10) at planting time.",
        60: "Apply a fertilizer high in potassium (e.g., 0-0-50)."
    },
    "Papaya": {
        0: "Apply a balanced fertilizer (e.g., 10-10-10) at planting time.",
        60: "Apply a fertilizer high in potassium (e.g., 0-0-50)."
    },
    "Pome Fruit": {
        0: "Apply a balanced fertilizer (e.g., 10-10-10) at planting time.",
        60: "Apply a fertilizer high in potassium (e.g., 0-0-50)."
    },
    "Pome Granet": {
        0: "Apply a balanced fertilizer (e.g., 10-10-10) at planting time.",
        60: "Apply a fertilizer high in potassium (e.g., 0-0-50)."
    },
    "Pump Kin": {
        0: "Apply a balanced fertilizer (e.g., 10-10-10) at planting time.",
        30: "Side-dress with nitrogen fertilizer."
    },
    "Ribed Guard": {
        0: "Apply a balanced fertilizer (e.g., 10-10-10) at planting time.",
        30: "Side-dress with nitrogen fertilizer."
    },
    "Snak Guard": {
         0: "Apply a balanced fertilizer (e.g., 10-10-10) at planting time.",
        30: "Side-dress with nitrogen fertilizer."
     },
    "Tomato": {
        0: "Apply a balanced fertilizer (e.g., 10-10-10) at planting time.",
        7: "Water-soluble fertilizer with higher nitrogen content (e.g., 20-10-10).",
        14: "Apply a balanced slow-release fertilizer around the base of each plant.",
        21: "Water-soluble fertilizer with balanced nutrients (e.g., 15-15-15).",
        28: "Apply a fertilizer high in phosphorus and potassium (e.g., 5-10-10) to promote flowering and fruiting.",
        35: "Water-soluble fertilizer with micronutrients (e.g., iron, magnesium) for overall plant health.",
        42: "Apply compost or organic fertilizer to replenish soil nutrients.",
        49: "Water-soluble fertilizer with calcium to prevent blossom end rot.",
        56: "Apply a balanced slow-release fertilizer to sustain plant growth.",
        63: "Water-soluble fertilizer with higher potassium content (e.g., 10-20-20) to support fruit development.",
        70: "Apply compost tea or liquid seaweed fertilizer for additional micronutrients.",
        77: "Water-soluble fertilizer with a balanced nutrient profile to maintain plant vigor.",
        84: "Apply a final dose of slow-release fertilizer to sustain the plant until harvest.",
        91: "Water-soluble fertilizer with low nitrogen content to avoid excessive vegetative growth before harvest."
    },
    "Water Melon": {
        0: "Apply a balanced fertilizer (e.g., 10-10-10) at planting time.",
        30: "Side-dress with nitrogen fertilizer."
    },
    "Yam": {
        0: "Apply a balanced fertilizer (e.g., 10-10-10) at planting time.",
        30: "Side-dress with nitrogen fertilizer."
    },
    "Plums": {
        0: "Apply a balanced fertilizer (e.g., 10-10-10) at planting time.",
        60: "Apply a fertilizer high in potassium (e.g., 0-0-50)."
    },
    "Redish": {
        0: "Apply a balanced fertilizer (e.g., 10-10-10) at planting time.",
        30: "Side-dress with nitrogen fertilizer."
    },
    "Horse-gram": {
        0: "Apply a balanced fertilizer (e.g., 10-10-10) at planting time.",
        30: "Side-dress with nitrogen fertilizer."
    },
    "Sesamum": {
        0: "Apply a balanced fertilizer (e.g., 10-10-10) at planting time.",
        30: "Side-dress with nitrogen fertilizer."
    },
    "Small millets": {
        0: "Apply a balanced fertilizer (e.g., 10-10-10) at planting time.",
        30: "Side-dress with nitrogen fertilizer."
    },
    "Gram": {
        0: "Apply a balanced fertilizer (e.g., 10-10-10) at planting time.",
        30: "Side-dress with nitrogen fertilizer."
    }
}

# Create GUI
root = tk.Tk()
root.title("ENHANCED FARMING ASSISTANT")

# Create two columns
left_frame = tk.Frame(root)
left_frame.pack(side="left", padx=5, pady=5, expand=True, fill="both")
right_frame = tk.Frame(root)
right_frame.pack(side="left", padx=5, pady=5, expand=True, fill="both")

# Widgets for left frame (Search, Display, Crop Information)
label1 = tk.Label(left_frame, text="State Name:")
label1.grid(row=0, column=0, padx=5, pady=5)
entry1 = tk.Entry(left_frame)
entry1.grid(row=0, column=1, padx=5, pady=5)
entry1_example = tk.Entry(left_frame)
entry1_example.insert(0, "Eg: Tamil Nadu")
entry1_example.config(state='readonly')
entry1_example.grid(row=0, column=2, padx=5, pady=5)

label2 = tk.Label(left_frame, text="District Name:")
label2.grid(row=1, column=0, padx=5, pady=5)
entry2 = tk.Entry(left_frame)
entry2.grid(row=1, column=1, padx=5, pady=5)
entry2_example = tk.Entry(left_frame)
entry2_example.insert(0, "Eg: Theni")
entry2_example.config(state='readonly')
entry2_example.grid(row=1, column=2, padx=5, pady=5)

label3 = tk.Label(left_frame, text="Season:")
label3.grid(row=2, column=0, padx=5, pady=5)
entry3 = tk.Entry(left_frame)
entry3.grid(row=2, column=1, padx=5, pady=5)
entry3_example = tk.Entry(left_frame)
entry3_example.insert(0, "Eg: Kharif")
entry3_example.config(state='readonly')
entry3_example.grid(row=2, column=2, padx=5, pady=5)

# Season information
season_info_label = tk.Label(left_frame, text="SEASONS TO BE GIVEN AND THEIR TIMELINES", font=("Arial", 12, "bold"))
season_info_label.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

season_info_text = """Kharif - June to October
(Sown nearly June-July & harvested within October end / November beginning)

Rabi - November to April/May
(Sown near November-December and harvested within April-May)

Whole Year"""
season_info_textbox = tk.Text(left_frame, height=10, width=50, wrap=tk.WORD)
season_info_textbox.grid(row=4, column=0, columnspan=3, padx=5, pady=5)
season_info_textbox.insert(tk.END, season_info_text)
season_info_textbox.config(state=tk.DISABLED)

# Buttons for search and display
search_button = tk.Button(left_frame, text="Search", command=lambda: show_results(df))
search_button.grid(row=5, column=0, padx=5, pady=5)

next_button = tk.Button(left_frame, text="Next", command=display_crop_info)
next_button.grid(row=5, column=1, padx=5, pady=5)

# Result textbox
result_textbox = tk.Text(left_frame, height=10, width=50)
result_textbox.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

# Entry for crop name
crop_entry_label = tk.Label(left_frame, text="ENTER THE CROP NAME", font=("Helvetica", 14, "bold"))
crop_entry_label.grid(row=7, column=0, columnspan=2, padx=5, pady=5)
crop_entry = tk.Entry(left_frame)
crop_entry.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

# Crop dropdown menu
crop_options = list(crop_actions.keys())
crop_var = tk.StringVar(left_frame)

if crop_options:
    crop_var.set(crop_options[0])  # Default crop selection
else:
    crop_var.set("")  # Set default value to empty string

crop_menu = ttk.Combobox(left_frame, textvariable=crop_var, values=crop_options)
crop_menu.grid(row=9, column=0, columnspan=2, padx=5, pady=5)

# Widgets for right frame (Watering Reminder, Fertilizer Reminder)
start_date_label = tk.Label(right_frame, text="Enter planting date (YYYY-MM-DD):")
start_date_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
start_date_entry = tk.Entry(right_frame)
start_date_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

end_date_label = tk.Label(right_frame, text="Enter harvesting date (YYYY-MM-DD):")
end_date_label.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
end_date_entry = tk.Entry(right_frame)
end_date_entry.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

schedule_label = tk.Label(right_frame, text="Enter watering schedule (days):")
schedule_label.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
schedule_entry = tk.Entry(right_frame)
schedule_entry.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

watering_button = tk.Button(right_frame, text="Set Watering Reminder", command=set_watering_reminder)
watering_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

fertilizer_button = tk.Button(right_frame, text="Check Fertilizer Reminder", command=check_fertilizer_reminder)
fertilizer_button.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

# Run the GUI main loop
root.mainloop()
