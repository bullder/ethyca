# Development

## Installation

1.  Clone the repository.
2.  Install dependencies using `uv`:

    ```bash
    uv sync
    ```

## Running Tests

To run the unit tests:

```bash
uv run pytest
```

## Local Development

You can run the API locally using the AWS SAM CLI. This will start a local API Gateway that mimics the production environment.

```bash
sam local start-api
```

The API will be available at `http://127.0.0.1:3000`.

## Deployment

To deploy the application to AWS:

```bash
sam build
sam deploy --guided
```
