import requests
import sqlite3

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
    import os
    if os.path.exists('weather_data.db'):
        os.remove('weather_data.db')
        print("Database deleted")
    else:
        print("Database does not exist")
