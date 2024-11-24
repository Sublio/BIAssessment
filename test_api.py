import pytest
import requests
import json

# Define the base URL for the API
BASE_URL = "https://api.restful-api.dev/objects"

object_id = None

headers = {"Content-Type": "application/json"}


@pytest.fixture
def create_object():
    """Fixture to create an object before the test and return its ID."""
    new_object = {"name": "Apple AirPods", "data": {"generation": "3rd", "price": 120}}

    response = requests.post(BASE_URL, json=new_object, headers=headers)

    assert (
        response.status_code == 200
    ), f"Failed to create object, status code: {response.status_code}"

    created_object = response.json()
    object_id = created_object["id"]

    print(f"Created object with ID: {object_id}")

    return object_id


def test_update_price_using_patch(create_object):
    """Test case to update the price using PATCH."""
    object_id = create_object
    
    updated_data = {
        "data": {
            "price": 135
        }
    }

    patch_url = f"{BASE_URL}/{object_id}"
    patch_response = requests.patch(patch_url, json=updated_data, headers=headers)

    assert patch_response.status_code == 200, f"Failed to update price, status code: {patch_response.status_code}"

    updated_object_response = patch_response.json()

    assert updated_object_response["id"] == object_id, "Object ID mismatch"
    assert updated_object_response["data"]["price"] == 135, "Price mismatch"
    assert "color" not in updated_object_response["data"], "Color should not be added with PATCH"

    print(f"Updated object details (price): {updated_object_response}")


def test_update_color_using_patch(create_object):
    """Test case to update the color using PATCH."""
    object_id = create_object
    
    updated_data = {
        "data": {
            "color": "white"
        }
    }

    patch_url = f"{BASE_URL}/{object_id}"
    patch_response = requests.patch(patch_url, json=updated_data, headers=headers)

    assert patch_response.status_code == 200, f"Failed to update color, status code: {patch_response.status_code}"

    updated_object_response = patch_response.json()

    assert updated_object_response["id"] == object_id, "Object ID mismatch"
    assert updated_object_response["data"]["color"] == "white", "Color mismatch"

    print(f"Updated object details (color): {updated_object_response}")

def test_update_generation_using_patch(create_object):
    """Test case to update the generation using PATCH."""
    object_id = create_object
    
    updated_data = {
        "data": {
            "generation": "4th"
        }
    }

    patch_url = f"{BASE_URL}/{object_id}"
    patch_response = requests.patch(patch_url, json=updated_data, headers=headers)

    assert patch_response.status_code == 200, f"Failed to update generation, status code: {patch_response.status_code}"

    updated_object_response = patch_response.json()

    assert updated_object_response["id"] == object_id, "Object ID mismatch"
    assert updated_object_response["data"]["generation"] == "4th", "Generation mismatch"
    assert "color" not in updated_object_response["data"], "Color should not be added with PATCH"

    print(f"Updated object details (generation): {updated_object_response}")