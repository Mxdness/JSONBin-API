Feature: JSONBin API automation

  Background:
    Given the JSONBin API client is initialized

  @tag1
  Scenario Outline: Create a new bin
    When I create a bin with the following data
      | key  | value  |
      | name | <name> |
      | type | <type> |
    Then the API response status should be 200
    And the created bin should contain the name "<name>"
    And the bin ID should be saved

    Examples:
      | name      | type       |
      | TestUser1 | Automation |
      | TestUser2 | BDD        |

  @tag1
  Scenario: Read an existing bin
    Given I create a test bin
    When I read the created bin
    Then the API response status should be 200
    And the response should contain the created data

  @tag2
  Scenario Outline: Read back bins with different content
    Given I create a bin with name "<name>" and type "<type>"
    When I read the created bin
    Then the API response status should be 200
    And the created bin should contain the name "<name>"

    Examples:
      | name       | type        |
      | ReadUser1  | Smoke       |
      | ReadUser2  | Regression  |

  @tag2
  Scenario: Delete an existing bin
    Given I create a test bin
    When I delete the created bin
    Then the API response status should be 200
    When I try to read the deleted bin
    Then the API response status should be 404
