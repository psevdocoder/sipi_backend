# sipi_backend

## About
This is project for Systems and software engineering subject, which should solve such problems as:
- chaos and monopoly by of the group's headman close friends during creating queues for turning in course assignments
- optimize group polls, and take it out specific place
- transfer student attendance records into electronic format, make this process easier for group's headman
- choose personal version of tasks

## Roles:
Administrator - can create users, subjects, and has same features as Moderator \
Moderator - can create and delete polls, queues, get group list, and has same features as Basic user \
Basic user - can participate in polls, join and leave queues, choose tasks

## Members
Kautarov Maksim - Backend-development \
Lysyutin Dmitriy - Mobile application development \
Gordeev Ilya - formally team leader, in fact useless person in projecet, so we put all the paperwork on him.\
Sotninov Daniil - testin and deployment (or not)

## Installation guide
### Preparing Postgres:
1. docker-compose.yml
```yml
version: '3.9'
services:
   postgres:
      container_name: postgres
      image: postgres:15-alpine
      restart: unless-stopped
      volumes:
        - ./postgresdata:/var/lib/postgresql/data
      ports:
        - 5432:5432
      networks:
        - default
      environment:
        - POSTGRES_USER=admin
        - POSTGRES_PASSWORD=admin_password
        - POSTGRES_INITDB_ARGS=--encoding=UTF-8 --lc-collate=C --lc-ctype=C

networks:
  default:
    name: your_docker_network
    external: true
```
2. Launch docker container:
```bash
docker-compose up -d
```
3. Enter inside postgres container
```bash
docker exec -it postgres psql -U admin
```
4. Create DB and PostgreSQL user, exit:
```postgresql
CREATE USER sipi_user WITH PASSWORD 'pg_user_password';
CREATE DATABASE sipi_db OWNER sipi_user TEMPLATE template0 ENCODING 'UTF8';
GRANT ALL PRIVILEGES ON DATABASE sipi_db TO sipi_user;
\q
```
---
### Preparing application
1. Clone this repository:
```bash
git clone https://github.com/psevdocoder/sipi_backend
```

2. cd to the locaton, where Dockerfile is.
```
.
????????? docker-compose.yml
????????? Dockerfile
????????? README.md
????????? requirements.txt
????????? sipi_back
 ???? ??????? 
 ???? ...
```

3. Build an application docker image
```bash
docker build --tag sipi_back .
```

4. Modify docker-compose.yml
```yaml
version: '3.8'

services:
  sipi_back:
    image: sipi_back:latest
    container_name: sipi_back
    env_file: env
    networks:
      - default
    volumes:
      - ./static:/sipi/sipi_back/static

networks:
  default:
    name: your_docker_network
    external: true
```

5. Create env file with your variables
```env
PG_HOST=postgres_host
PG_PORT=postgres_port
PG_DB_NAME=project_db_name
PG_USER=sipi_user
PG_USER_PWD=pg_user_password
SECRET_KEY=django_secret_key
DEBUG_STATUS=0
DJANGO_LOGLEVEL=debug
```

6. Run the application
```bash
docker-compose up -d
```

7. Login inside the container
```
docker exec -it sipi_back bash
```

8. make migrations
```
python manage.py makemigrations
```

9. create superuser
```
python manage.py createsuperuser
```

10. Exit from sipi_back container and modify postgres table with users to give admin role level for superuser
```
docker exec -it postgres psql -U admin
```

11. connect to sipi_db
```postgresql
\c sipi_db
```

12. modify user and exit
```postgresql
update users_user set role = 3 where id = 1 ;
\q
```

---
### Preparing nginx web-server

1. Create new directory for nginx.
2. Create docker-compose.yml for nginx
```yml
version: '3.9'

services:
  nginx:
    container_name: nginx
    restart: unless-stopped
    image: "nginx:1.21.5-alpine"
    ports:
      - 80:80
      - 443:443
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/nginx.conf:ro
      - ./ssl/:/cert:ro
      - ./logs/:/logs
      - /path/to/sipi/sipi_backend/:/sipi_backend
    networks:
      - default

networks:
  default:
    name: your_docker_network
    external: true
```

3. Create nginx.conf
```nginx
server {
    listen 443 ssl http2;
    server_name your.domain.com;
    ssl_certificate_key /cert/your_private.key;
    ssl_certificate /cert/your_cert.pem;
    
    location /static/ {
         root /sipi_backend/;

    }

    location / {
        proxy_pass http://sipi_back:8000/;
        proxy_set_header Host $http_host;
        proxy_set_header X-Forwarded-For $remote_addr;
        proxy_redirect off;
        proxy_set_header X-Forwarded-Proto $scheme;
        client_max_body_size 5m;
    }
}
```

4. Nginx configuration files should have same structure:
```
.
????????? docker-compose.yml
????????? nginx.conf
????????? ssl
    ????????? your_cert.pem
    ????????? your_private.key
```
