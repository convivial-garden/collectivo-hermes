# Hermes Disposerver

An instance of [collectivo](https://github.com/MILA-Wien/collectivo/) for the Austrian Hermes Radbot:innen colelctiv [HERMES](https://www.hermes.at/).
## Documentation

The documentation of collectivo can be found [here](https://github.com/MILA-Wien/collectivo/).

For local testing of this repository, follow these steps:

1. Install docker and docker-compose.
2. Clone the repository.
3. Copy `.env.example` to `.env` and adopt all the values.
4. Add the following line to your `/etc/hosts/` file: `127.0.0.1 keycloak`
5. Run `docker compose -f ./docker-compose-dev.yml up -d`
6. Access your instance via https://127.0.0.1, and https://keycloak.local (accept security risk on each)



[out:csv ("name")][timeout:2500];
{{geocodeArea:Wien}}->.searchArea;
(
  way["highway"]["name"](area.searchArea);
);
for (t["name"])
{
  make street name=_.val;
  out;
}
