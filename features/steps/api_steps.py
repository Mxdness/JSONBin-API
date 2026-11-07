from behave import given, when, then

from framework.jsonbin_client import JSONBinClient


# ---------- Background / Given ----------

@given("the JSONBin API client is initialized")
def initialize_client(context):
    context.client = JSONBinClient()
    context.bin_id = None
    context.bin_deleted = False


@given("I create a test bin")
def create_test_bin(context):
    context.payload = {"name": "BDD Test", "type": "Automation"}
    context.response = context.client.create_bin(context.payload)

    assert context.response.status_code == 200, (
        f"Create failed: {context.response.text}"
    )
    context.bin_id = context.response.json()["metadata"]["id"]


@given('I create a bin with name "{name}" and type "{bin_type}"')
def create_bin_with_values(context, name, bin_type):
    context.payload = {"name": name, "type": bin_type}
    context.response = context.client.create_bin(context.payload)

    assert context.response.status_code == 200, (
        f"Create failed: {context.response.text}"
    )
    context.bin_id = context.response.json()["metadata"]["id"]


# ---------- When ----------

@when("I create a bin with the following data")
def create_bin_with_table(context):
    payload = {row["key"]: row["value"] for row in context.table}

    context.payload = payload
    context.response = context.client.create_bin(payload)

    if context.response.status_code == 200:
        context.bin_id = context.response.json().get("metadata", {}).get("id")


@when("I read the created bin")
def read_created_bin(context):
    context.response = context.client.read_bin(context.bin_id)


@when("I delete the created bin")
def delete_created_bin(context):
    context.response = context.client.delete_bin(context.bin_id)
    if context.response.status_code == 200:
        context.bin_deleted = True


@when("I try to read the deleted bin")
def read_deleted_bin(context):
    context.response = context.client.read_bin(context.bin_id)


# ---------- Then ----------

@then("the API response status should be {expected_status:d}")
def verify_status(context, expected_status):
    assert context.response.status_code == expected_status, (
        f"Expected {expected_status}, received {context.response.status_code}. "
        f"Response: {context.response.text}"
    )


@then('the created bin should contain the name "{expected_name}"')
def verify_created_bin(context, expected_name):
    actual_name = context.response.json()["record"]["name"]
    assert actual_name == expected_name, (
        f"Expected name '{expected_name}', got '{actual_name}'"
    )


@then("the bin ID should be saved")
def verify_bin_id(context):
    assert context.bin_id, "No bin ID was returned by the API"


@then("the response should contain the created data")
def verify_response_data(context):
    record = context.response.json()["record"]
    assert record == context.payload, (
        f"Expected {context.payload}, got {record}"
    )
