# Mysql-training Project

## Requirements

- [MySQL v8.0.44 ](https://www.mysql.com/): You'll need this running locally for now. I haven't added it to the Docker Compose yet, though it's a straightforward fix if you'd rather run it there..

## Technology Stack and Features
- ⚡ [**FastAPI**](https://fastapi.tiangolo.com) for the Python backend API.
  - 🧰 [SQLModel](https://sqlmodel.tiangolo.com) for the Python SQL database interactions (ORM).
  - 🔍 [Pydantic](https://docs.pydantic.dev), used by FastAPI, for the data validation and settings management.
  - 💾 [MySQL](https://www.mysql.com/) as the SQL database.
- 🐋 [Docker Compose](https://www.docker.com) for development and production.

## How To Use It

You can **just fork or clone** this repository and use it as is.

### Configure

You can then update configs in the `.env` files to customize your configurations.

### How to Run with Docker Compose

If you want to run the project in your computer with completes workflow. You could follow this guide.

- Build docker image:
```bash
docker compose build
```

- Run docker container:
```bash
docker compose up
```

- Close docker container app:
```bash
docker compose down
```
