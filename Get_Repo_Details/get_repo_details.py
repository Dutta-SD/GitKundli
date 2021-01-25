# Script to GET Repo details from user

import json
import requests
import os
import pprint
import fire

# constants useful for the script
BASE_URL = "https://api.github.com/graphql" # Github base url
GITHUB_TOKEN = os.environ['GITHUB_TOKEN']  # Github token environment variable

def getQuery(repoName, userName):
  '''
  Returns the query string that will fetch data from the API.
  Gets the number of collaborators, number of stars, 
  number of pull requests, and total commits of a particular repository.

  Args:
    repoName : Name of the repository from which to fetch data
    userName : Name of the owner of the repository
  
  Return:
    query : Query string which will be used to query the API endpoint
  '''
  query = """query {{
    repository(name: \"{0}\", owner: \"{1}\") {{
      collaborators {{
        totalCount
      }}
      pullRequests {{
        totalCount
      }}
      stargazers {{
        totalCount
      }}
      object(expression: "master") {{
        ... on Commit {{
          history {{
            totalCount
          }}
        }}
      }}
    }}
  }}""".format(repoName, userName)   # GraphQL Query
  return query


def getRepoDetails(repoName, userName):
  # Main function
  # Set names of Repo and gets data from API Query

  # Sanity check
  assert (repoName is not None and userName is not None), "Invalid Details"

  # Specify Headers
  # Note - Can only see collaborators if it is own repository
  headers = {'Authorization': "Token " + GITHUB_TOKEN}
  # API Request
  response = requests.post(
    BASE_URL,
    json={'query': getQuery(repoName, userName)},
    headers=headers)
  
  json_data = json.loads(response.text)

  # Extract meaningful Information from json data
  # As per Query Structure
  num_collaborators = json_data['data']['repository']['collaborators']['totalCount']
  num_pullRequests = json_data['data']['repository']['pullRequests']['totalCount']
  num_stars = json_data['data']['repository']['stargazers']['totalCount']
  num_commits = json_data['data']['repository']['object']['history']['totalCount']

  return num_collaborators, num_pullRequests, num_stars, num_commits

def displayDetails(repoName, userName):
  num_collaborators, num_pullRequests, num_stars, num_commits = getRepoDetails(repoName, userName)

  # Pretty display 
  print("-" * 80)
  print(f"Stats for Repository {repoName} (Owner : {userName})")
  print(f"Number of collaborators : {num_collaborators}")
  print(f"Number of Pull Requests : {num_pullRequests}")
  print(f"Number of Stars : {num_stars}")
  print(f"Number of Commits : {num_commits}")



if __name__ == '__main__':
  fire.Fire(displayDetails)