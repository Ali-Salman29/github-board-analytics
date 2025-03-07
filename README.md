# GitHub Project Report Generator

## Overview
This script fetches issues from a specified GitHub project, categorizes them by status and contributor, and generates a structured report.

## Features
- Retrieves issues from a GitHub project using GraphQL API.
- Categorizes issues by their status (To Do, In Progress, Done, etc.).
- Categorizes issues by assigned contributors.
- Outputs a formatted report as a text file.

## Prerequisites
- Python 3.x installed.
- A GitHub personal access token with the required permissions.

## Installation
1. Clone the repository or download the script.
2. Install dependencies using:
   ```sh
   pip install requests
   ```

## Usage
Run the script with the following command:
```sh
python script.py --org <organization> --project <project_number> --token <github_token> --output <output_filename>
```

### Arguments
- `--org` (optional): GitHub organization name (default: `edly-io`).
- `--project` (optional): GitHub project number (default: `5`).
- `--token` (required): GitHub personal access token (can also be set as `GITHUB_TOKEN` environment variable).
- `--output` (optional): Output file name (default: `github_project_report.txt`).

## Example
```sh
python script.py --token YOUR_GITHUB_TOKEN
```
This will generate `github_project_report.txt` with categorized issues.

## Output Format
The report will include:
1. Issues categorized by status (To Do, In Progress, Done, etc.).
2. Issues categorized by contributor, including unassigned issues.

## License
This project is licensed under the MIT License.

