Feature: Task Management

  Scenario: Loading tasks from a non-existent file
    Given the tasks file does not exist
    When I load the tasks
    Then the task list should be empty

  Scenario: Generating a unique ID for a new task
    Given there are 3 existing tasks with IDs 1, 2, and 5
    When I generate a unique ID
    Then the ID should be 6

  Scenario: Filtering tasks by priority
    Given I have tasks with High and Low priority
    When I filter tasks by priority "High"
    Then only High priority tasks should be returned

  Scenario: Searching for a keyword in tasks
    Given I have tasks with various titles and descriptions
    When I search for the keyword "meeting"
    Then I should get only tasks containing "meeting" in the title and/or description

  Scenario: Sorting tasks by title
    Given I have tasks with titles "Zebra", "apple", and "Monkey"
    When I sort tasks by "Title"
    Then the tasks should be in alphabetical order
