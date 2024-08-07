import requests

API_KEY = "d090cb0cda63b5f349a5cfcc3514560f"  # Api will work for 5 days


def get_data(place, forecast_days=None):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={place}&appid={API_KEY}"
    response = requests.get(url)
    data = response.json()
    filtered_Data = data['list']
    num_values = 8 * forecast_days
    filtered_Data = filtered_Data[:num_values]
    return filtered_Data


if __name__ == "__main__":
    print(get_data(place='Tokyo',forecast_days=3))