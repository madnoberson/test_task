# Secunda Test Task

> [!IMPORTANT]  
> All API methods require an API key. The default key is "123".

## Run

### Build

```bash
# This will run the web API, accessible at 127.0.0.1:8000
docker-compose up -d
```

### Run migrations

```bash
docker exec -it test_task.web_api test-task alembic upgrade head
```

### Create fake data

```bash
docker exec -it test_task.web_api test-task create-fake-data
```

## Fake data

### Buildings

```json
[
  {
    "id": 1,
    "address": "ул. Пушкина, д.27, Москва, 143350",
    "lat": 55.609715,
    "lon": 37.211006
  },
  {
    "id": 2,
    "address": "пр. Столыпина 27, Саратов",
    "lat": 51.531541,
    "lon": 46.027244
  },
  {
    "id": 3,
    "address": "1206 Van Ness Ave, Fresno, CA 93721, USA",
    "lat": 36.737289,
    "lon": -119.792144
  }
]
```

### Domains

```json
[
  {
    "id": 1,
    "parent_id": null,
    "name": "Торты"
  },
  {
    "id": 2,
    "parent_id": 1,
    "name": "Маленькие торты"
  },
  {
    "id": 3,
    "parent_id": 2,
    "name": "Мельчайшие торты"
  },
  {
    "id": 4,
    "parent_id": 1,
    "name": "Большие торты"
  },
  {
    "id": 5,
    "parent_id": null,
    "name": "Техника"
  },
  {
    "id": 6,
    "parent_id": 5,
    "name": "Ноутбуки"
  },
  {
    "id": 7,
    "parent_id": 6,
    "name": "Сенсорные ноутбуки"
  }
]
```

### Organizations

```json
[
  {
    "id": 1,
    "building_id": 1,
    "name": "КНОПКАБАБЛО",
    "phone_numbers": ["+79993999999", "+79893396959"],
    "domain_ids": [3, 4]
  },
  {
    "id": 2,
    "building_id": 2,
    "name": "СИНЕЕ ЧЕРНОЕ",
    "phone_numbers": ["+79178894242"],
    "domain_ids": [5]
  },
  {
    "id": 3,
    "building_id": 3,
    "name": "Lenovo",
    "phone_numbers": ["+19999999999"],
    "domain_ids": [6]
  }
]
```
