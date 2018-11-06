ROOMING
=======

### 1. Run django project container with docker compose

This project has developed on docker container, python and potgres.
Once clone into your local environment, run following command to build up docker containers.

```sh
$ cd rooming
$ docker-compose up -d
```

If you have not installed docker and docker compose, please download and install from under links.

+ windows : [Install Docker Toolbox on Windows
](https://docs.docker.com/toolbox/toolbox_install_windows/)
+ macOS: [Install Docker Toolbox on Mac](https://docs.docker.com/toolbox/toolbox_install_mac/)

Only linux operation system, it will installed with bash commands.

1\. Run this command to download the latest version of Docker Compose:

```sh
sudo curl -L "https://github.com/docker/compose/releases/download/1.22.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```

2\. Apply executable permissions to the binary:

```sh
sudo chmod +x /usr/local/bin/docker-compose
```

3\. Optionally, install command completion for the bash and zsh shell.

4\. Test the installation.

```sh
$ docker-compose --version
docker-compose version 1.22.0, build 1719ceb
```

### 2. Rebuild web container

If you changes or customizes container environment in, `Dockerfile` / `docker-compose.yml`, run this command to rebuild web container.

```sh
$ docker-compose  up -d --build
```

### 3. Apply database migrations

When add migration in django project, apply database changes using django migration command in web container.

```sh
$ docker-compose run web python /code/manage.py migrate --noinput
```
