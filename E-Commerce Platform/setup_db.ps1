<#
PowerShell helper to create the `ecommerce` database, create `ecom_user`, import schema, and update .env

This script will:
- Prompt for a password for the new DB user `ecom_user`
- Run MySQL commands as `root` (you will be prompted for the root password)
- Import `sql/schema.sql` using the new user (you will be prompted for the new user's password)
- Copy `.env.example` to `.env` and update `DATABASE_URI` with the new user credentials

Security note: this script will write the DB password in plain text to `.env` so the app can use it. Do not commit `.env` to source control.
#>

Write-Host "This script automates DB creation, user creation, schema import, and .env setup.`n"

# Ask user for password for the new DB user
$ecomPassSecure = Read-Host "Enter password for new DB user 'ecom_user' (input will be hidden)" -AsSecureString
$ptr = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($ecomPassSecure)
$ecomPass = [System.Runtime.InteropServices.Marshal]::PtrToStringBSTR($ptr)
[System.Runtime.InteropServices.Marshal]::ZeroFreeBSTR($ptr)

Write-Host "You will be prompted for the MySQL root password next."

# Build the SQL commands. The password will be interpolated directly.
$sql = "CREATE DATABASE IF NOT EXISTS ecommerce CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci; `n"
$sql += "CREATE USER IF NOT EXISTS 'ecom_user'@'localhost' IDENTIFIED BY '$ecomPass'; `n"
$sql += "GRANT ALL PRIVILEGES ON ecommerce.* TO 'ecom_user'@'localhost'; `n"
$sql += "FLUSH PRIVILEGES;"

# Run as root (will prompt for root password)
Write-Host "Running MySQL commands as root to create database and user..."
$escapedSql = $sql -replace '"', '"' # ensure safe quoting (basic)
mysql -u root -p -e $escapedSql
if ($LASTEXITCODE -ne 0) {
    Write-Error "MySQL command failed. Please check your root credentials and try again."
    exit 1
}

# Import schema using the new user (will prompt for ecom_user password)
Write-Host "Importing schema from sql/schema.sql using 'ecom_user' (you will be prompted for the user's password)..."
mysql -u ecom_user -p ecommerce < sql/schema.sql
if ($LASTEXITCODE -ne 0) {
    Write-Error "Schema import failed. Ensure the user has privileges and the file 'sql/schema.sql' exists.";
    exit 1
}

# Copy .env.example -> .env (if .env doesn't exist) and update DATABASE_URI
if (-not (Test-Path .env)) {
    if (Test-Path .env.example) {
        Copy-Item .env.example .env
        Write-Host ".env created from .env.example"
    } else {
        Write-Warning ".env.example not found. Creating a minimal .env file."
        "DATABASE_URI=mysql+pymysql://ecom_user:$ecomPass@localhost:3306/ecommerce" | Out-File -FilePath .env -Encoding UTF8
    }
}

# Replace or add DATABASE_URI line in .env
$content = Get-Content .env -ErrorAction SilentlyContinue
$pattern = '^DATABASE_URI='
$replacement = "DATABASE_URI=mysql+pymysql://ecom_user:$ecomPass@localhost:3306/ecommerce"
if ($content -match $pattern) {
    $new = $content -replace $pattern, $replacement
    $new | Set-Content .env -Encoding UTF8
} else {
    Add-Content .env "`n$replacement"
}

Write-Host "Updated .env with DATABASE_URI for 'ecom_user'. Do not commit .env to version control.";
Write-Host "Done. You can now run: `n  python -m pip install -r requirements.txt`n  python seed.py`n  python run.py"

exit 0
