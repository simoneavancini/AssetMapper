# AssetMapper

Service based reconnaisance tool to find all assets of a given domain or organization

## Requirements

- docker
- docker-compose

### API keys and secrets

IPInfo, BuiltWith and Hunter.io require a (free) API key. These keys must be specified in the `.env` file together with the JWT secret.

```
JWT_SECRET=<secret>
IPINFO_API_KEY=<ipinfo_key>
BUILTWITH_API_KEY=<builtwith_key>
HUNTERIO_API_KEY=<hunterio_key>
```

## How to run

To run the application run the following command:

```
docker-compose up --build
```

Then you can use the application through the CLI

```
./cli/app.py --help
```

## Testing

Individual services can be tested through the reverse proxy accessible at `http://127.0.0.1:8080/<service_name>/<path>`

Example:

```bash
curl 'http://127.0.0.1:8080/authentication/register' \
    -d '{"email":"user@example.com","username":"user","password":"1234"}' \
    -H 'Content-type: application/json'
```
