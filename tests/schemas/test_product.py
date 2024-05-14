from pydantic import ValidationError
import pytest
from tests.factories import product_data
from store.schemas.product import ProductIn

def test_schemas_success():
    data = product_data()
    product = ProductIn.model_validate(data)

    assert product.name == 'S20'

def test_schemas_raise():
    data = {'name': 'S20', 'quantity': 10, 'price': 2300}

    with pytest.raises(ValidationError) as err:
        ProductIn.model_validate(data)

    assert err.value.errors()[0] == {'type': 'missing', 'loc': ('status',), 'msg': 'Field required', 'input': {'name': 'S20', 'quantity': 10, 'price': 2300}, 'url': 'https://errors.pydantic.dev/2.5/v/missing'}