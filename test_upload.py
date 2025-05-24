import requests

def test_csv_upload():
    url = 'http://localhost:8000/api/users/upload/'
    files = {
        'file': ('sample_user_data.csv', open('sample_user_data.csv', 'rb'), 'text/csv')
    }

    try:
        response = requests.post(url, files=files)
        print("Status Code:", response.status_code)
        print("Response:", response.json())
    except Exception as e:
        print("Error:", str(e))
    finally:
        files['file'][1].close()

if __name__ == "__main__":
    test_csv_upload() 