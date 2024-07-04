import requests


class ProviderService:
    def __init__(self, provider_url):
        self.provider_url = provider_url
        self.headers = {
            "Content-Type": "application/json",
        }

    def get_plate(self, plate_number):
        url = f"{self.provider_url}/plates/{plate_number}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def create_route(self, data):
        url = f"{self.provider_url}/routes"

        try:
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def create_toll_voucher(self, data):
        url = f"{self.provider_url}/toll_vouchers"

        try:
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def put_data(self, endpoint, data):
        url = f"{self.provider_url}/{endpoint}"

        try:
            response = requests.put(url, headers=self.headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def patch_data(self, endpoint, data):
        url = f"{self.provider_url}/{endpoint}"

        try:
            response = requests.patch(url, headers=self.headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def cancel_toll_voucher(self, code):
        url = f"{self.provider_url}/toll_vouchers/{code}"

        try:
            response = requests.delete(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
