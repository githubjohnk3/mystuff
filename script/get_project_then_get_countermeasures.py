import requests
import json

# Set your base URL and API key if needed
base_url = "https://jk.iriusrisk.com/api/v2"
api_key = "5dca7b8c-0670-47d5-938a-321befb53d0d"  # Add your API key here if authentication is needed

# First API call to get the list of projects
projects_url = f"{base_url}/projects?page=0&size=50"
headers = {
    "api-token": api_key,  
    "Content-Type": "application/json"
}

response = requests.get(projects_url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    projects = response.json()
    project_list = projects["_embedded"]["items"]  # Adjust according to the actual structure of the JSON response

    # Display list of project names and ids
    print("List of Projects:")
    for i, project in enumerate(project_list):
        print(f"{i + 1}. {project['name']} (ID: {project['id']})")

    # Prompt the user to pick a project
    selected_index = int(input("Enter the number of the project you want to use: ")) - 1

    # Get the selected project ID
    selected_project_id = project_list[selected_index]['id']

    # Make the second API call using the selected project ID
    version = "your-uuid-version"  # Replace with actual version/UUID if needed
    countermeasures_url = f"{base_url}/projects/{selected_project_id}/countermeasures?size=200"
    
    countermeasures_response = requests.get(countermeasures_url, headers=headers)

    if countermeasures_response.status_code == 200:
        countermeasures_data = countermeasures_response.json()
         # Pretty print the countermeasures JSON response
         #print(json.dumps(countermeasures_data, indent=4))

           # Loop through the items and print only the desired fields
        for item in countermeasures_data["_embedded"]["items"]:  # Access items under _embedded
            print({
                "Component": item.get("component", {}).get("name"),
                "name": item.get("name"),
                "state": item.get("state"),
                "id": item.get("id"),
                "referenceId": item.get("referenceId") 
            })
    else:
        print(f"Failed to fetch countermeasures: {countermeasures_response.status_code}")
else:
    print(f"Failed to fetch projects: {response.status_code}")
