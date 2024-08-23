import tkinter as tk
from tkinter import messagebox
from weather import get_weather, store_weather_data, view_data, delete_specific_data, clear_all_data, delete_database
from init_db import init_db

# Initialize the database
init_db()

def show_weather():
    city = city_entry.get()
    if not city:
        messagebox.showerror("Error", "City field cannot be empty")
        return
    
    api_key = ""  # Replace with OpenWeatherMap API key
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

# buttons for viewing, deleting, and clearing data
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

