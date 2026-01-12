# Running Locally

You can run the full stack locally using `sam local` (requires Docker) or `chalice local` (Python only). This guide assumes you want to connect to your **deployed DynamoDB table** in AWS (requires AWS credentials configured).

## Prerequisites
1.  **AWS Credentials**: Ensure `aws configure` is run and you have access to your account.
2.  **DynamoDB Table Name**: You need the name of the table created by the deployment.
3.  **Python 3.14** (or compatible).

## Step 1: Get the Table Name
Run this command to find your Tic-Tac-Toe table name:
```bash
aws dynamodb list-tables --output text --query "TableNames[?contains(@, 'GamesTable')]"
```
*Take note of the output name (e.g., `tic-tac-toe-stack-GamesTable-XXXX`).*

## Step 2: Set Environment Variables
### Option A: Using `env.json` (for SAM)
Create a file named `env.json` in the root directory:
```json
{
  "TicTacToeFunction": {
    "TABLE_NAME": "YOUR_TABLE_NAME_FROM_STEP_1",
    "SECRET_KEY": "dev-secret"
  }
}
```

### Option B: Export (for Chalice/Direct)
**PowerShell:**
```powershell
$env:TABLE_NAME="YOUR_TABLE_NAME_FROM_STEP_1"
$env:SECRET_KEY="dev-secret"
```

## Step 3: Run the API
### Using SAM Local (Recommended)
This runs the API on port 3000.
```bash
sam local start-api --env-vars env.json
```

### Using Chalice
This runs the API on port 8000.
```bash
chalice local --port 3000
```
*Note: We use port 3000 to match the configuration in `index.html`.*

## Step 4: Run the UI
Open a new terminal and serve the static files:
```bash
python -m http.server 8080 --directory app/static
```

## Step 5: Play!
Open your browser to: [http://localhost:8080](http://localhost:8080)

The UI is configured to detect `localhost` and automatically try to connect to the API at `http://127.0.0.1:3000`.
