import tkinter as tk
from tkinter import messagebox
import requests
import sqlite3
import os
import sqlite3

# Connect to SQLite database (it will create the database file if it doesn't exist)
conn = sqlite3.connect('weather_data.db')

# Create a cursor object
cursor = conn.cursor()

# Create a table to store weather records
cursor.execute('''
CREATE TABLE IF NOT EXISTS weather (
    id INTEGER PRIMARY KEY,
    city TEXT NOT NULL,
    temperature REAL NOT NULL,
    pressure INTEGER NOT NULL,
    humidity INTEGER NOT NULL,
    description TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

# Commit changes and close the connection
conn.commit()
conn.close()

def get_weather(api_key, city):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + city + "&units=metric"
    response = requests.get(complete_url)
    return response.json()

def store_weather_data(city, temp, pressure, humidity, description):
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO weather (city, temperature, pressure, humidity, description)
    VALUES (?, ?, ?, ?, ?)
    ''', (city, temp, pressure, humidity, description))
    conn.commit()
    conn.close()

def show_weather():
    city = city_entry.get()
    if not city:
        messagebox.showerror("Error", "City field cannot be empty")
        return
    
    api_key = ""
    weather_data = get_weather(api_key, city)
    
    if weather_data['cod'] != 200:
        messagebox.showerror("Error", weather_data['message'])
        return
    
    temp = weather_data['main']['temp']
    pressure = weather_data['main']['pressure']
    humidity = weather_data['main']['humidity']
    description = weather_data['weather'][0]['description']

    weather_info = f"Temperature: {temp}°C\nPressure: {pressure} hPa\nHumidity: {humidity}%\nDescription: {description.capitalize()}"
    result_label.config(text=weather_info)
    
    # Store the fetched weather data in the database
    store_weather_data(city, temp, pressure, humidity, description)

def view_data():
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM weather')
    rows = cursor.fetchall()
    # Print the records in a readable format
    print("Weather Records:")
    print(f"{'ID':<5} | {'City':<10} | {'Temperature (°C)':<20} | {'Pressure (hPa)':<20} | {'Humidity (%)':<20} | {'Description':<20} | {'Timestamp':<22}")
    print("-"*132)
    for row in rows:
        print(f"{row[0]:<{5}} | {row[1]:<{10}} | {row[2]:<{20}} | {row[3]:<{20}} | {row[4]:<{20}} | {row[5]:<{20}} | {row[6]:<{22}}")
    
    # Close the connection
    conn.close()

def delete_specific_data(city):
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM weather WHERE city = ?', (city,))
    conn.commit()
    conn.close()
    print(f"Records for {city} deleted")

def clear_all_data():
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM weather')
    conn.commit()
    conn.close()
    print("All records cleared")

def delete_database():
    if os.path.exists('weather_data.db'):
        os.remove('weather_data.db')
        print("Database deleted")
    else:
        print("Database does not exist")

# Create the main window
root = tk.Tk()
root.title("Weather App")

# Create and place the widgets
tk.Label(root, text="Enter city name:").grid(row=0, column=0, padx=10, pady=10)

city_entry = tk.Entry(root)
city_entry.grid(row=0, column=1, padx=10, pady=10)

get_weather_button = tk.Button(root, text="Get Weather", command=show_weather)
get_weather_button.grid(row=0, column=2, padx=10, pady=10)

result_label = tk.Label(root, text="", justify=tk.LEFT)
result_label.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

# Additional buttons for viewing, deleting, and clearing data
view_data_button = tk.Button(root, text="View Data", command=view_data)
view_data_button.grid(row=2, column=0, padx=10, pady=10)

delete_data_button = tk.Button(root, text="Delete Data", command=lambda: delete_specific_data(city_entry.get()))
delete_data_button.grid(row=2, column=1, padx=10, pady=10)

clear_data_button = tk.Button(root, text="Clear All Data", command=clear_all_data)
clear_data_button.grid(row=2, column=2, padx=10, pady=10)

delete_db_button = tk.Button(root, text="Delete Database", command=delete_database)
delete_db_button.grid(row=3, column=1, padx=10, pady=10)

# Start the main event loop
root.mainloop()

