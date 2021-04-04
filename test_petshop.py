import pytest
import requests
from typing import List


class Petstore:
    def __init__(self, domain='petstore.swagger.io', proto='https', version=2):
        self.domain = domain
        self.proto = proto
        self.version = version
        self.base_url = f'{self.proto}://{self.domain}/v{version}'

    def get_url(self, element):
        return '/'.join([self.base_url, element])

    def add_pet(self, name: str, photo_urls: List[str]):
        raw_data = {"name": name, "photoUrls": photo_urls}
        data = {}
        for key, value in raw_data.items():
            if value is not None:
                data[key] = value
        url = self.get_url('pet')
        resp = requests.post(url, json=data)
        return resp

    def get_pet(self, pet_id: int):
        url = self.get_url(f'pet/{pet_id}')
        resp = requests.post(url)
        return resp

    def get_inventory(self):
        url = self.get_url('store/inventory')
        resp = requests.get(url)
        return resp


@pytest.fixture(scope='session')
def base_url():
  petstore = Petstore()
  return petstore.base_url


class TestPetstore:
    petstore = Petstore()

    def test_create_pet(self):
        resp = self.petstore.add_pet('test_pet', ['test_photo_url'])
        assert resp.status_code == 200
        assert resp.json() is not None

    def test_create_pet__no_photo(self):
        resp = self.petstore.add_pet('test_pet', photo_urls=None)
        assert resp.status_code == 405
        assert resp.json() is None

    def test_create_pet__no_name(self):
        resp = self.petstore.add_pet(name=None, photo_urls=None)
        assert resp.status_code == 405
        assert resp.json() is None

    def test_get_pet(self):
        resp = self.petstore.get_pet(1)
        assert resp.json()
        assert resp.status_code == 200

    def test_get_inventory(self):
        resp = self.petstore.get_inventory()

        assert resp.json()
        assert resp.status_code == 200
