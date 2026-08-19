import requests

class API:
    def __init__(self, base_url):
        self.base_url = base_url

    def fetch_next_task(self):
        response = requests.patch(f'{self.base_url}/robot/next-task')
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch next task: {response.status_code}")
            return None
        
    def get_path(self):
        response = requests.get(f'{self.base_url}/robot/path')
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch path: {response.status_code}")
            return None

# api = API('http://192.168.1.29:8000')
# api.fetch_next_task()
# path = api.get_path()
# print(path["data"]["commands"])