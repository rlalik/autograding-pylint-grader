## GitHub Classroom Python Pylint Grader

### Overview
**GitHub Classroom Python Pylint Grader** is a plugin for GitHub Classroom's Autograder. Seamlessly integrate your CS class with GitHub using this action to facilitate the grading process.

### Key Features
- **Automatic Grading**: Evaluate student code submissions and provide immediate feedback.
- **Customizable Test Setup**: Define pre-test setup commands and specific testing commands.
- **Command Execution**: Run any command and determine the success based on the exit code.
- **Timeout Control**: Limit the runtime of tests to prevent excessive resource usage, with a maximum duration of 6 hours.
- **Scoring System**: Assign a maximum score for tests, awarding points upon successful test completion.

### Inputs

| Input Name      | Description                                                                                                     | Required |
|-----------------|-----------------------------------------------------------------------------------------------------------------|----------|
| `timeout`       | Duration (in minutes) before the test is terminated. Defaults to 10 minutes with a maximum limit of 6 hours.    | Yes      |
| `max-score`     | Points to be awarded if the test passes.                                                                        | No       |
| `setup-command` | Command to execute prior to the test, typically for environment setup or dependency installation.               | No       |
| `pylint-args`   | Additional arguments for pylint.                                                                                | No       |
| `files`         | Files to be checked. Bash-like files list.                                                                      | Yes      |

### Outputs

| Output Name | Description                        |
|-------------|------------------------------------|
| `result`    | Outputs the result of the grader, indicating the success or failure of the test.  |

### Usage

1. Add the GitHub Classroom Python Grader action to your workflow.

```
name: Autograding Tests

on:
  push

jobs:
  run-tests:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    - name: Linter
      id: pylint-test
      uses: rlalik/autograding-pylint-grader@v1
      with:
        timeout: '15'
        max-score: '100'
        pylint-args: '--disable=unused-variable'
        files: 'module_a.py module_b.py'
    - name: Autograding Reporter
      uses: ...
```
