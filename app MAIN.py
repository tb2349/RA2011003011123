from flask import Flask, request, jsonify
import requests
import concurrent.futures
import time

app = Flask(__name__)

def fetch_numbers_from_url(url):
    try:
        response = requests.get(url, timeout=2)  # Timeout set to 2 seconds
        data = response.json()
        if "numbers" in data:
            return data["numbers"]
        else:
            return []
    except Exception as e:
        return []

def merge_and_sort_numbers(number_lists):
    merged_numbers = []
    for numbers in number_lists:
        merged_numbers.extend(numbers)
    merged_numbers = list(set(merged_numbers))  # Remove duplicates
    merged_numbers.sort()  # Sort in ascending order
    return merged_numbers

@app.route('/numbers', methods=['GET'])
def get_numbers():
    urls = request.args.getlist('url')

    number_lists = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(fetch_numbers_from_url, url) for url in urls]
        for future in concurrent.futures.as_completed(futures, timeout=0.5):
            try:
                numbers = future.result()
                number_lists.append(numbers)
            except Exception as e:
                pass  # Ignore timeouts or other errors

    merged_numbers = merge_and_sort_numbers(number_lists)

    return jsonify(numbers=merged_numbers)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8008)
