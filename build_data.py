import os
import json
import requests
from kaggle.api.kaggle_api_extended import KaggleApi

# Configurações iniciais
GITHUB_USERNAME = "SEU_USUARIO_GITHUB"
ARQUIVO_SAIDA = "projetos.json"

def buscar_projetos_github():
    print("Buscando projetos do GitHub...")
    token = os.getenv("GITHUB_TOKEN")
    headers = {"Accept": "application/vnd.github.v3+json"}
    
    if token:
        headers["Authorization"] = f"Bearer {token}"
        
    url = f"https://api.github.com/users/{GITHUB_USERNAME}/repos?sort=updated&per_page=100"
    resposta = requests.get(url, headers=headers)
    resposta.raise_for_status()
    
    projetos = []
    for repo in resposta.json():
        if not repo["fork"]:
            projetos.append({
                "id": f"gh-{repo['id']}",
                "titulo": repo["name"].replace("-", " ").title(),
                "descricao": repo.get("description") or "Projeto em desenvolvimento.",
                "url": repo["html_url"],
                "origem": "GitHub",
                "tecnologias": repo.get("language") or "Várias",
                "atualizado_em": repo["updated_at"]
            })
    return projetos

def buscar_projetos_kaggle():
    print("Buscando notebooks do Kaggle...")
    usuario_kaggle = os.getenv("KAGGLE_USERNAME")
    projetos = []
    
    try:
        api = KaggleApi()
        api.authenticate() # Usa as variáveis KAGGLE_USERNAME e KAGGLE_KEY automaticamente
        
        kernels = api.kernels_list(user=usuario_kaggle)
        for kernel in kernels:
            projetos.append({
                "id": f"kg-{kernel.ref.replace('/', '-')}",
                "titulo": kernel.title,
                "descricao": "Análise Exploratória e Modelagem de Dados",
                "url": f"https://www.kaggle.com/{kernel.ref}",
                "origem": "Kaggle",
                "tecnologias": "Python / Jupyter",
                "atualizado_em": str(kernel.lastRunTime)
            })
    except Exception as e:
        print(f"Erro ao buscar dados do Kaggle: {e}")
        
    return projetos

def principal():
    todos_projetos = []
    todos_projetos.extend(buscar_projetos_github())
    todos_projetos.extend(buscar_projetos_kaggle())
    
    # Ordena do mais recente para o mais antigo
    todos_projetos.sort(key=lambda x: x["atualizado_em"], reverse=True)
    
    # Salva o arquivo JSON que o Frontend vai ler
    with open(ARQUIVO_SAIDA, "w", encoding="utf-8") as f:
        json.dump(todos_projetos, f, ensure_ascii=False, indent=2)
    
    print(f"Sucesso! {len(todos_projetos)} projetos salvos em {ARQUIVO_SAIDA}.")

if __name__ == "__main__":
    principal()