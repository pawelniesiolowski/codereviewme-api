Code Review Me API
==================

# Roles
- **reviewer**: can create, update and delete Reviewers
- **author**: can crete, update and delete Authors and Projects
- **codereviewme_admin**: can create, update and delete Technologies
- *show and index endpoints for Reviewers, Authors, Projects and Technologies are available to all users*.

# Endpoints

## Technologies

### POST /technologies
- It takes technology's name and description and creates technology
- Request example
```json
POST https://codereviewme-api.herokuapp.com/technologies
{
    "name": "Python",
    "description": "An interpreted, high-level, general-purpose programming language"
}
```
- Response example
```json
{
    "href": "/technologies/1"
}
```

### GET /technologies/[technology_id]
- It shows technology's data
- Request example
```
GET https://codereviewme-api.herokuapp.com/technologies/1
```
- Response example
```json
{
    "data": {
        "description": "An interpreted, high-level, general-purpose programming language",
        "id": 1,
        "name": "Python"
    }
}
```

### GET /technologies
- It indexes technologies
- Request example
```
GET https://codereviewme-api.herokuapp.com/technologies
```
- Response example
```json
{
    "data": [
        {
            "description": "An interpreted, high-level, general-purpose programming language",
            "id": 1,
            "name": "Python"
        },
        {
            "description": "A functional, concurrent, general-purpose programming language",
            "id": 2,
            "name": "Elixir"
        }
    ]
}
```

### PATCH /technologies/[technology_id]
- It edits given data for technology
- Request example
```json
PATCH https://codereviewme-api.herokuapp.com/technologies/2
{
	"description": "A functional, concurrent, general-purpose programming language that runs on the Erlang virtual machine (BEAM)"
}
```
- Response example
```
204 NO CONTENT
```

### DELETE /technologies/[technology_id]
- It deletes technology
- Request example
```
DELETE https://codereviewme-api.herokuapp.com/technologies/3
```
- Response example
```
204 NO CONTENT
```

## Authors

### POST /authors
- It takes author's name, surname, email, description and technologies and creates author
- Request example
```json
POST https://codereviewme-api.herokuapp.com/authors
{
    "name": "Paweł",
    "surname": "Niesiołowski",
    "email": "pavel.niesiolowski@gmail.com",
    "description": "Python programmer",
    "technologies": [1]
}
```
- Response example
```json
{
    "href": "/authors/1"
}
```

### GET /authors/[author_id]
- It shows author's data
- Request example
```
GET https://codereviewme-api.herokuapp.com/authors/1
```
- Response example
```json
{
    "data": {
        "description": "Python programmer",
        "email": "pavel.niesiolowski@gmail.com",
        "id": 2,
        "name": "Paweł",
        "surname": "Niesiołowski",
        "technologies": [
            {
                "description": "An interpreted, high-level, general-purpose programming language",
                "id": 1,
                "name": "Python"
            }
        ]
    }
}
```

### GET /authors
- It indexes authors
- Request example
```
https://codereviewme-api.herokuapp.com/authors
```
- Response example
```json
{
    "data": [
        {
            "description": "Python programmer",
            "email": "pavel.niesiolowski@gmail.com",
            "id": 2,
            "name": "Paweł",
            "surname": "Niesiołowski",
            "technologies": [
                {
                    "description": "An interpreted, high-level, general-purpose programming language",
                    "id": 1,
                    "name": "Python"
                }
            ]
        }
    ]
}
```

### PATCH /authors/[author_id]
- It edits given data for author
- Request example
```json
PATCH https://codereviewme-api.herokuapp.com/authors/1
{
    "description": "Elixir programmer",
    "technologies": [2]
}
```
- Response example
```
204 NO CONTENT
```

### DELETE /authors/[author_id]
- It deletes author
- Request example
```
DELETE https://codereviewme-api.herokuapp.com/authors/1
```
- Response example
```
204 NO CONTENT
```

## Projects

### POST /authors/[author_id]/projects
- It takes name, description, repository url and technologies and creates project for given author
- Request example
```json
POST https://codereviewme-api.herokuapp.com/authors/1/projects
{
    "name": "Code Review Me",
    "description": "This is the main API for the Code Review Me application that helps novice programmers find experienced mentors",
    "repository_url": "https://github.com/pawelniesiolowski/codereviewme-api",
    "technologies": [1]
}
```
- Response example
```json
{
    "href": "/authors/1/projects/1"
}
```

### GET /authors/[author_id]/projects/[project_id]
- It shows project's data
- Request example
```
GET https://codereviewme-api.herokuapp.com/authors/1/projects/1
```
- Response example
```json
{
    "data": {
        "author_id": 1,
        "description": "This is the main API for the Code Review Me application that helps novice programmers find experienced mentors",
        "id": 1,
        "name": "Code Review Me",
        "repository_url": "https://github.com/pawelniesiolowski/codereviewme-api",
        "technologies": [
            {
                "description": "An interpreted, high-level, general-purpose programming language",
                "id": 1,
                "name": "Python"
            }
        ]
    }
}
```

### GET /authors/[author_id]/projects
- It indexes projects for given author
- Request example
```
GET https://codereviewme-api.herokuapp.com/authors/1/projects
```
- Response example
```json
{
    "data": [
        {
            "author_id": 1,
            "description": "This is the main API for the Code Review Me application that helps novice programmers find experienced mentors",
            "id": 1,
            "name": "Code Review Me",
            "repository_url": "https://github.com/pawelniesiolowski/codereviewme-api",
            "technologies": [
                {
                    "description": "An interpreted, high-level, general-purpose programming language",
                    "id": 1,
                    "name": "Python"
                }
            ]
        }
    ]
}
```

### PATCH /authors/[author_id]/projects/[project_id]
- I edits given data for project
- Request example
```json
PATCH https://codereviewme-api.herokuapp.com/authors/1/projects/1
{
    "name": "Code Review Me API"
}
```
- Response example
```
204 NO CONTENT
```

### DELETE /authors/[author_id]/projects/[project_id]
- It deletes project
- Request example
```
DELETE https://codereviewme-api.herokuapp.com/authors/1/projects/1
```
- Response example
```
204 NO CONTENT
```

## Reviewers

### POST /reviewers
- It takes reviewer's name, surname, email, description, repository url and technologies and creates reviewer
- Request example
```json
POST https://codereviewme-api.herokuapp.com/reviewers
{
    "name": "Paweł",
    "surname": "Niesiołowski",
    "email": "pavel.niesiolowski@gmail.com",
    "repository_url": "https://github.com/pawelniesiolowski/codereviewme-api",
    "description": "Passionate and experienced programmer",
    "technologies": [1, 2]
}
```
- Response example
```json
{
    "href": "/reviewers/1"
}
```

### GET /reviewers/[reviewer_id]
- It shows reviewer's data
- Request example
```
GET https://codereviewme-api.herokuapp.com/reviewers/1
```
- Response example
```json
{
    "data": {
        "description": "Passionate and experienced programmer",
        "email": "pavel.niesiolowski@gmail.com",
        "id": 1,
        "name": "Paweł",
        "repository_url": "https://github.com/pawelniesiolowski/codereviewme-api",
        "surname": "Niesiołowski",
        "technologies": [
            {
                "description": "An interpreted, high-level, general-purpose programming language",
                "id": 1,
                "name": "Python"
            },
            {
                "description": "A functional, concurrent, general-purpose programming language that runs on the Erlang virtual machine (BEAM)",
                "id": 2,
                "name": "Elixir"
            }
        ]
    }
}
```

### GET /reviewers
- It indexes reviewers
- Request example
```
GET https://codereviewme-api.herokuapp.com/reviewers
```
- Response example
```json
{
    "data": [
        {
            "description": "Passionate and experienced programmer",
            "email": "pavel.niesiolowski@gmail.com",
            "id": 1,
            "name": "Paweł",
            "repository_url": "https://github.com/pawelniesiolowski/codereviewme-api",
            "surname": "Niesiołowski",
            "technologies": [
                {
                    "description": "An interpreted, high-level, general-purpose programming language",
                    "id": 1,
                    "name": "Python"
                },
                {
                    "description": "A functional, concurrent, general-purpose programming language that runs on the Erlang virtual machine (BEAM)",
                    "id": 2,
                    "name": "Elixir"
                }
            ]
        }
    ]
}
```

### PATCH /reviewers/[reviewer_id]
- It edits given data for reviewer
- Request example
```json
PATCH https://codereviewme-api.herokuapp.com/reviewers/1
{
    "description": "Passionate and experienced Python programmer"
}
```
- Response example
```
204 NO CONTENT
```

### DELETE /reviewers/[reviewer_id]
- It deletes reviewer
- Request example
```
DELETE https://codereviewme-api.herokuapp.com/reviewers/1
```
- Response example
```
204 NO CONTENT
```

## Errors
- **401 Unauthorized** - resource needs authorization
- **404 NOT FOUND** - resource is not available
- **409 Conflict** - resource already exists
- **422 Unprocessable Entity** - given data is not valid
- **500 Internal Server Error** - something goes wrong on server side, for example with database connection

# Get authorization headers to test API on production
To print all tokens for all different roles execute test_tokens.py script: `python test_tokens.py`
