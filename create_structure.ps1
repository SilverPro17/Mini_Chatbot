# Lista de todos os caminhos (relativos)
$paths = @(
    # arquivos raiz
    "README.md",
    "requirements.txt",
    "setup.py",
    "quickstart.sh",
    "Dockerfile",
    "docker-compose.yml",
    "demo.ipynb",
    ".env",
    ".gitignore",

    # dentro de data
    "data\texts\receitas_brasileiras.txt",
    "data\texts\ingredientes_brasileiros.txt",
    "data\texts\tecnicas_culinarias.txt",
    "data\texts\[adicione_mais_aqui].txt",
    "data\vectorstore\index.faiss",
    "data\vectorstore\index.pkl",

    # dentro de models
    "models\dialogpt-medium\config.json",
    "models\dialogpt-medium\pytorch_model.bin",
    "models\dialogpt-medium\tokenizer.json",
    "models\dialogpt-medium\vocab.json",
    # embeddings é só pasta
    "models\embeddings\sentence-transformers\",

    # src
    "src\download_model.py",
    "src\create_vectorstore.py",
    "src\chatbot.py",
    "src\app_streamlit.py",

    # docs
    "docs\arquitetura.md",
    "docs\como_contribuir.md",
    "docs\exemplos.md",

    # tests
    "tests\test_vectorstore.py",
    "tests\test_chatbot.py",
    "tests\test_integration.py",

    # scripts
    "scripts\backup_data.sh",
    "scripts\update_vectorstore.py",
    "scripts\evaluate_model.py",

    # config
    "config\model_config.yaml",
    "config\app_config.yaml",

    # logs
    "logs\chatbot.log",
    "logs\vectorstore.log"
)

foreach ($p in $paths) {
    $p = $p.TrimEnd('\')                      # remover possível '\' no fim (pastas)
    $dir = Split-Path $p
    if ($dir -and -not (Test-Path $dir)) {
        New-Item -Path $dir -ItemType Directory -Force | Out-Null
    }
    # se tiver extensão (é arquivo), cria; senão, pula
    if ($p -match '\.[A-Za-z0-9]+$') {
        New-Item -Path $p -ItemType File -Force | Out-Null
    }
}

Write-Host "Estrutura completa criada com sucesso!"
