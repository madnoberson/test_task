# Secunda Test Task

## Build

```bash
docker-compose up
```

## Run migrations

```bash
docker exec -it test_task.web_api alembic upgrade head
```

## Create fake data

```bash
docker exec -it test_task.web_api create-fake-data
```
