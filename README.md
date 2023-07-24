# TT_FABRIQUE

Данный репозиторий содержит в себе техническое задание для компании "Фабрика Решений".
### Инструкция по установке
(python version 3.11)

```
pip install virtualenv
git clone https://github.com/glebsolovyov/tt_fabrique.git
cd tt_fabrique
python -m virtualenv venv
source venv/bin/activate

pip install -r requirements.txt

cp .env.template .env
```

### Запуск Docker
```
 docker-compose -f docker-compose.yml up --build
```

### Миграции БД
```
docker-compose -f docker-compose.yml run --rm web-app sh -c "python manage.py makemigrations"
docker-compose -f docker-compose.yml run --rm web-app sh -c "python manage.py migrate"       
```

### Задание

https://www.craft.me/s/n6OVYFVUpq0o6L

### Документация Swagger

```
/api/docs
```

### Выполненные дополнительные задания

3, 4, 5