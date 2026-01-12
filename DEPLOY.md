# Deployment Instructions

## Prerequisites
1.  **AWS CLI**: Installed and configured with `aws configure`.
2.  **AWS SAM CLI**: Installed.
3.  **Python 3.12+**: Required for the runtime.
4.  **uv**: For dependency management (`uv` CLI).

## 1. Backend Deployment (API)

The backend is an AWS Serverless Application Model (SAM) application.

1.  **Build the application**:
    ```bash
    sam build
    ```

2.  **Deploy to AWS**:
    ```bash
    sam deploy --guided
    ```
    *Follow the prompts. Saving the configuration to `samconfig.toml` makes future deploys easier.*

## 2. Frontend Deployment (UI)

The frontend is a static `index.html` file hosted on S3 and served via CloudFront.

1.  **Get Stack Outputs**:
    After a successful `sam deploy`, find the S3 bucket name in the outputs or run:
    ```bash
    aws cloudformation describe-stacks --stack-name tic-tac-toe-stack --query "Stacks[0].Outputs"
    ```
    *Look for `TicTacToeWebBucket`.*

2.  **Upload `index.html`**:
    Replace `YOUR_BUCKET_NAME` with the actual bucket name (e.g., `tic-tac-toe-stack-tictactoewebbucket-...`).
    ```bash
    aws s3 cp app/static/index.html s3://YOUR_BUCKET_NAME/index.html
    ```

3.  **Invalidate CloudFront Cache**:
    To see changes immediately, invalidate the CloudFront cache.
    Find your Distribution ID:
    ```bash
    aws cloudfront list-distributions --query "DistributionList.Items[*].{Id:Id,DomainName:DomainName}"
    ```
    Run invalidation:
    ```bash
    aws cloudfront create-invalidation --distribution-id YOUR_DIST_ID --paths "/*"
    ```

## 3. Verification

1.  **Get the Game URL**:
    From the stack outputs (`TicTacToeCustomDomain`), usually `https://tic-tac-toe.garifull.in/`.

2.  **Test**:
    - Open the URL in a browser.
    - Click "Start New Game".
    - Open Developer Tools (F12) to verify logs (e.g., `Initializing game v2...`).

## CI/CD

A GitHub Action (`.github/workflows/ci.yml`) is configured to run tests and linting on every push to `main`.
