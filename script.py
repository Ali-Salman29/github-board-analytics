import requests
import argparse
import os

GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"

def fetch_github_project_items(org, project, token):
    query = f"""
    query {{
      organization(login: "{org}") {{
        projectV2(number: {project}) {{
          items(first: 50) {{
            nodes {{
              id
              content {{
                __typename
                ... on Issue {{
                  title
                  url
                  number
                  assignees(first: 5) {{
                    nodes {{
                      login
                    }}
                  }}
                }}
              }}
              fieldValues(first: 10) {{
                nodes {{
                  ... on ProjectV2ItemFieldSingleSelectValue {{
                    name  # This contains the column name (To Do, In Progress, Done, etc.)
                    field {{
                      ... on ProjectV2Field {{
                        name
                      }}
                    }}
                  }}
                }}
              }}
            }}
          }}
        }}
      }}
    }}
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.post(GITHUB_GRAPHQL_URL, json={"query": query}, headers=headers)
    if response.status_code == 200:
        return response.json().get("data", {}).get("organization", {}).get("projectV2", {}).get("items", {}).get("nodes", [])
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return []

def categorize_issues(items):
    columns = {}
    contributors = {}
    
    for item in items:
        issue = item.get("content")
        if issue and issue.get("__typename") == "Issue":
            title = issue["title"]
            url = issue["url"]
            number = issue["number"]
            
            # Extract assignees
            assignees = issue.get("assignees", {}).get("nodes", [])
            assignee_logins = [a["login"] for a in assignees] if assignees else ["Unassigned"]

            # Extract status/column name
            status = "Unknown"
            for field in item.get("fieldValues", {}).get("nodes", []):
                if field and field.get('name', '') in ['Done', 'In Progress', 'Todo']:
                    status = field.get("name", "Unknown")

            # Add to column-based categorization
            if status not in columns:
                columns[status] = []
            columns[status].append(f"- #{number} {title} ({url}) - Assigned to: {', '.join(assignee_logins)}")

            # Add to contributor-based categorization
            for assignee in assignee_logins:
                if assignee not in contributors:
                    contributors[assignee] = []
                contributors[assignee].append(f"- #{number} {title} ({url}) [{status}]")
    
    return columns, contributors

# Generate report text
def generate_report(columns, contributors):
    report = []

    # Report by Status (Column-based)
    report.append("# Issues Categorized by Status\n")
    for column, issues in columns.items():
        report.append(f"## {column} ({len(issues)})\n")
        report.extend(issues)
        report.append("\n")

    # Report by Contributor
    report.append("# Issues Categorized by Contributor\n")
    for contributor, issues in contributors.items():
        report.append(f"## {contributor} ({len(issues)})\n")
        report.extend(issues)
        report.append("\n")

    return "\n".join(report)

def main():
    parser = argparse.ArgumentParser(description="Fetch and categorize GitHub project issues.")
    parser.add_argument("--org", default="edly-io", help="GitHub organization name (default: edly-io)")
    parser.add_argument("--project", type=int, default=5, help="GitHub project number (default: 5)")
    parser.add_argument("--token", default=os.getenv("GITHUB_TOKEN"), help="GitHub personal access token (default: from environment variable GITHUB_TOKEN)")
    parser.add_argument("--output", default="github_project_report.txt", help="Output file name (default: github_project_report.txt)")
    args = parser.parse_args()
    
    if not args.token:
        print("Error: GitHub token is required. Set it using the --token argument or the GITHUB_TOKEN environment variable.")
        return
    
    items = fetch_github_project_items(args.org, args.project, args.token)
    categorized_issues, contributor_issues = categorize_issues(items)
    report_text = generate_report(categorized_issues, contributor_issues)
    
    with open(args.output, "w", encoding="utf-8") as file:
        file.write(report_text)
    
    print(f"Report saved as {args.output}")

if __name__ == "__main__":
    main()

