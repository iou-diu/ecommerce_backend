DCL Backend Documentation 
---
1. Clone Project from github
2. Create virtualenv
      ```sh
    $ virtualenv venv
    ```
3. Activate Virtualenv
   ```sh
    $ source venv/Scripts/activate
    ```
4. Add project specific information in .env
5. Make migration
    ```sh
    $ python manage.py makemigrations
    ```
6. Migrate
    ```sh
    $ python manage.py migrate
    ```
7. Create Superuser
    ```sh
    $ python manage.py createsuperuser
    ```
8. Start Server
    ```sh
    $ python manage.py runserver
    ```
9. Run Celery for the background tasks
    ```sh
    $ celery -A core worker -l info -P threads  
    $ celery -A core beat -l info
    ```
10. Run Typesense Commands
    ```sh
    $ python manage.py typesensepro schema
    $ python manage.py typesensepro destroy
    $ python manage.py typesensepro reindex
    ```

11. Docker Setup
    ```sh
    # Start services with the correct environment and build
    $ docker-compose -f docker-compose.prod.yml up --build -d    # for production (.env.prod)
    $ docker-compose -f docker-compose.yml up --build -d          # for local environment (.env)

    # To stop, rebuild, and restart a specific service (e.g., web)
    $ docker-compose -f docker-compose.prod.yml up -d --build web
    $ docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
    $ docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput




    ```


Here's an updated version that accounts for using multiple Docker Compose files like `docker-compose.prod.yml`:

---

You don't necessarily need to stop and rebuild the `web` container every time you pull changes from Git. It depends on the nature of the changes. Here's a breakdown:

### 1. **Code-only changes** (e.g., Python files, HTML, templates):
If you're only pulling updates to the code (such as Django views, models, or templates), you **don't need to rebuild** the container.  
In this case, you can simply restart the `web` service to load the new code:

```bash
docker-compose -f docker-compose.prod.yml restart web
```

### 2. **Dependency changes** (e.g., changes to `requirements.txt`, Python packages):
If the pull includes changes to dependencies (such as updates in `requirements.txt`), you'll need to **rebuild the image** so that the new dependencies are installed.  
In this case, follow the process of stopping, rebuilding, and restarting the `web` service:

```bash
docker-compose -f docker-compose.prod.yml stop web
docker-compose -f docker-compose.prod.yml up --no-deps --build web
```

### 3. **Configuration or environment changes** (e.g., `Dockerfile`, `docker-compose.yml`, or `.env` file):
If you modify the Docker configuration (e.g., `Dockerfile`, `docker-compose.prod.yml`, or `.env` file), then you should **rebuild the container**:

```bash
docker-compose -f docker-compose.prod.yml stop web
docker-compose -f docker-compose.prod.yml up --no-deps --build web
```

### **To summarize:**
- For **code changes only**: just restart the container.
- For **dependency or configuration changes**: stop and rebuild the container.

---

By adding the `-f docker-compose.prod.yml` flag, you can ensure you're working with the correct Docker Compose file each time. If you'd like to avoid specifying the file, you can also set it using environment variables or aliases as mentioned previously.

docker compose -f docker-compose.prod.yml build --no-cache
docker compose -f docker-compose.prod.yml up -d

docker compose -f docker-compose.prod.yml logs web



docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up --build -d

