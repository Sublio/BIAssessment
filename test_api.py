import pytest
import requests
import json

# Define the base URL for the API
BASE_URL = "https://api.restful-api.dev/objects"

# Set the object ID for testing, initially None (it will be set after creation)
object_id = None

# Define the headers for the requests
headers = {"Content-Type": "application/json"}


@pytest.fixture
def create_object():
    """Fixture to create an object before the test and return its ID."""
    # Prepare the new object data for creation
    new_object = {"name": "Apple AirPods", "data": {"generation": "3rd", "price": 120}}

    # Send the POST request to create the object
    response = requests.post(BASE_URL, json=new_object, headers=headers)

    # Ensure the POST request was successful
    assert (
        response.status_code == 200
    ), f"Failed to create object, status code: {response.status_code}"

    # Get the created object's ID
    created_object = response.json()
    object_id = created_object["id"]

    print(f"Created object with ID: {object_id}")

    # Return the object ID for use in other tests
    return object_id


def test_update_object(create_object):
    """Test case to update the object with a new price and add color."""
    # Get the object ID from the fixture
    object_id = create_object

    # Retrieve the current object details before updating
    get_url = f"{BASE_URL}/{object_id}"
    response = requests.get(get_url)
    assert (
        response.status_code == 200
    ), f"Failed to retrieve object, status code: {response.status_code}"
    current_object = response.json()
    print(f"Current object details: {current_object}")

    # Prepare the updated object with new price and added color
    updated_object = {
        "id": object_id,
        "name": current_object["name"],
        "data": {
            "color": "white",  # New color attribute
            "generation": current_object["data"]["generation"],
            "price": 135,  # Updated price
        },
    }

    # Send the PUT request to update the object
    put_url = f"{BASE_URL}/{object_id}"
    payload = json.dumps(updated_object)
    put_response = requests.put(put_url, data=payload, headers=headers)

    # Assert that the PUT request was successful
    assert (
        put_response.status_code == 200
    ), f"Failed to update object, status code: {put_response.status_code}"

    # Get the updated object from the response
    updated_object_response = put_response.json()

    # Assert that the updated details are correct
    assert updated_object_response["id"] == object_id, "Object ID mismatch"
    assert (
        updated_object_response["name"] == updated_object["name"]
    ), "Object name mismatch"
    assert updated_object_response["data"]["color"] == "white", "Color mismatch"
    assert updated_object_response["data"]["price"] == 135, "Price mismatch"
    assert (
        updated_object_response["data"]["generation"]
        == current_object["data"]["generation"]
    ), "Generation mismatch"

    # Print the updated object details
    print(f"Updated object details: {updated_object_response}")
