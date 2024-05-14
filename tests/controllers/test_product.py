from typing import List

import pytest
from tests.factories import product_data
from fastapi import HTTPException, status

async def test_controller_create_should_return_success(client, products_url):
    response = await client.post(products_url, json=product_data())
    content = response.json()

    del content['id']
    del content['created_at']
    del content['updated_at']

    try:
        assert response.status_code == status.HTTP_201_CREATED

    except HTTPException:
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert content == {'name': 'S20', 'quantity': 10, 'price': "2300", 'status': True,}


async def test_controller_get_should_return_success(client, products_url, product_inserted):
    response = await client.get(f"{products_url}{product_inserted.id}")

    content = response.json()

    del content['created_at']
    del content['updated_at']

    assert response.status_code == status.HTTP_200_OK
    assert content == {'id': str(product_inserted.id), 'name': 'S20', 'quantity': 10, 'price': "2300", 'status': True,}


async def test_controller_get_should_not_found(client, products_url):
    response = await client.get(f"{products_url}e129743e-dbc2-4170-8ab7-2438ee8d8a84")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Product not found with filter: e129743e-dbc2-4170-8ab7-2438ee8d8a84'}

@pytest.mark.usefixtures("products_inserted")
async def test_controller_query_should_return_success(client, products_url):
    response = await client.get(products_url)

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), List)
    assert len(response.json()) > 1

async def test_controller_patch_should_return_success(client, products_url, product_inserted):
    response = await client.patch(f"{products_url}{product_inserted.id}", json={'price': '550'})

    content = response.json()

    del content['created_at']
    del content['updated_at']

    assert response.status_code == status.HTTP_200_OK
    assert content == {'id': str(product_inserted.id), 'name': 'S20', 'quantity': 10, 'price': "550", 'status': True,}

async def test_controller_delete_should_return_no_content(client, products_url, product_inserted):
    response = await client.delete(f"{products_url}{product_inserted.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT


async def test_controller_delete_should_not_found(client, products_url):
    response = await client.delete(f"{products_url}e129743e-dbc2-4170-8ab7-2438ee8d8a84")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Product not found with filter: e129743e-dbc2-4170-8ab7-2438ee8d8a84'}