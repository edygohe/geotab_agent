# setup_repo.ps1

# --- Script para inicializar un repositorio de Git y subirlo a GitHub ---

# 1. Preguntar por la URL del repositorio remoto
$repoUrl = Read-Host -Prompt "Pega la URL de tu repositorio de GitHub (ej: https://github.com/usuario/repo.git)"

if ([string]::IsNullOrWhiteSpace($repoUrl)) {
    Write-Host "Error: No se proporcionó una URL. Abortando." -ForegroundColor Red
    exit 1
}

# 2. Verificar si ya existe un repositorio de Git
if (Test-Path ".git") {
    Write-Host "Este directorio ya es un repositorio de Git. Abortando." -ForegroundColor Yellow
    exit
}

# 3. Ejecutar los comandos de Git
try {
    Write-Host "1. Inicializando repositorio..." -ForegroundColor Cyan
    git init

    Write-Host "2. Añadiendo todos los archivos..." -ForegroundColor Cyan
    git add .

    Write-Host "3. Creando el commit inicial..." -ForegroundColor Cyan
    git commit -m "Initial commit: project structure setup"

    Write-Host "4. Renombrando la rama a 'main'..." -ForegroundColor Cyan
    git branch -M main

    Write-Host "5. Conectando con el repositorio remoto..." -ForegroundColor Cyan
    git remote add origin $repoUrl

    Write-Host "6. Subiendo los cambios a GitHub..." -ForegroundColor Cyan
    git push -u origin main

    Write-Host "Exito, El repositorio se ha configurado y subido a GitHub." -ForegroundColor Green
}
catch {
    Write-Host "Ocurrio un error durante el proceso de Git:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
}
