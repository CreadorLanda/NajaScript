#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GitHub Registry Setup for NajaScript
Script para configurar a estrutura inicial do registry no GitHub
"""

import json
import os
from pathlib import Path

def create_registry_structure():
    """Criar estrutura de diretórios e arquivos para o GitHub registry"""
    
    # Estrutura de diretórios
    dirs_to_create = [
        "registry",
        "packages",
        "docs",
        "examples"
    ]
    
    for dir_name in dirs_to_create:
        Path(dir_name).mkdir(exist_ok=True)
        print(f"✅ Criado diretório: {dir_name}/")
    
    # Criar index.json do registry
    registry_index = {
        "name": "NajaScript Official Package Registry",
        "description": "Registry oficial de pacotes para a linguagem NajaScript",
        "version": "1.0.0",
        "last_updated": "2025-01-03T00:00:00Z",
        "packages": {
            "exemplo-basico": {
                "name": "exemplo-basico",
                "description": "Pacote de exemplo básico para NajaScript",
                "author": "NajaScript Team",
                "license": "MIT",
                "repository": "https://github.com/NajaScript/Naja",
                "keywords": ["exemplo", "basico", "tutorial"],
                "versions": ["1.0.0"],
                "latest": "1.0.0"
            }
        },
        "total_packages": 1,
        "categories": {
            "utilities": ["exemplo-basico"],
            "games": [],
            "web": [],
            "math": [],
            "ai": []
        }
    }
    
    # Salvar index.json
    registry_file = Path("registry/index.json")
    with open(registry_file, 'w', encoding='utf-8') as f:
        json.dump(registry_index, f, indent=2, ensure_ascii=False)
    print(f"✅ Criado: {registry_file}")
    
    # Criar estrutura do pacote exemplo
    example_package_dir = Path("packages/exemplo-basico/1.0.0")
    example_package_dir.mkdir(parents=True, exist_ok=True)
    
    # index.naja do pacote exemplo
    example_code = '''// Pacote Exemplo Básico
// Demonstra a estrutura básica de um pacote NajaScript

classe ExemploBasico {
    funcao construtor() {
        println("ExemploBasico carregado!");
    }
    
    funcao saudar(string nome) {
        return "Olá " + nome + " do pacote ExemploBasico!";
    }
    
    funcao calcular(int a, int b) {
        return a + b;
    }
    
    funcao info() {
        dicionario info = {};
        info.add("nome", "exemplo-basico");
        info.add("versao", "1.0.0");
        info.add("autor", "NajaScript Team");
        return info;
    }
}

// Exportar instância
var exemploBasico = ExemploBasico();
'''
    
    example_main_file = example_package_dir / "index.naja"
    with open(example_main_file, 'w', encoding='utf-8') as f:
        f.write(example_code)
    print(f"✅ Criado: {example_main_file}")
    
    # package.json do pacote exemplo
    example_package_json = {
        "name": "exemplo-basico",
        "version": "1.0.0",
        "description": "Pacote de exemplo básico para NajaScript",
        "main": "index.naja",
        "keywords": ["exemplo", "basico", "tutorial"],
        "author": "NajaScript Team",
        "license": "MIT",
        "repository": {
            "type": "git",
            "url": "https://github.com/NajaScript/Naja"
        },
        "homepage": "https://najascript.github.io",
        "dependencies": {},
        "najascript": {
            "min_version": "1.0.0"
        }
    }
    
    example_json_file = example_package_dir / "package.json"
    with open(example_json_file, 'w', encoding='utf-8') as f:
        json.dump(example_package_json, f, indent=2, ensure_ascii=False)
    print(f"✅ Criado: {example_json_file}")
    
    # README do pacote exemplo
    example_readme = '''# Exemplo Básico

Pacote de exemplo básico para demonstrar a estrutura de pacotes NajaScript.

## Instalação

```bash
naja_pkg install exemplo-basico
```

## Uso

```naja
import "exemplo-basico";

// Usar o pacote
string saudacao = exemploBasico.saudar("Mundo");
println(saudacao);

int resultado = exemploBasico.calcular(5, 3);
println("Resultado: " + resultado);

dicionario info = exemploBasico.info();
println("Pacote: " + info.obter("nome"));
```

## API

### Métodos

- `saudar(string nome)` - Retorna uma saudação personalizada
- `calcular(int a, int b)` - Soma dois números
- `info()` - Retorna informações do pacote

## Licença

MIT
'''
    
    example_readme_file = example_package_dir / "README.md"
    with open(example_readme_file, 'w', encoding='utf-8') as f:
        f.write(example_readme)
    print(f"✅ Criado: {example_readme_file}")
    
    # Criar README principal
    main_readme = '''# NajaScript Package Registry

Registry oficial de pacotes para a linguagem de programação NajaScript.

## Estrutura

- `registry/` - Índice de pacotes e metadados
- `packages/` - Código fonte dos pacotes
- `docs/` - Documentação
- `examples/` - Exemplos de uso

## Como Usar

### Instalar um Pacote

```bash
naja_pkg install nome-do-pacote
```

### Listar Pacotes

```bash
naja_pkg list
```

### Pesquisar Pacotes

```bash
naja_pkg search termo
```

## Estrutura de Pacotes

Cada pacote deve seguir esta estrutura:

```
packages/
└── nome-do-pacote/
    └── versao/
        ├── index.naja      # Código principal
        ├── package.json    # Metadados
        └── README.md       # Documentação
```

## Contribuindo

1. Fork este repositório
2. Crie seu pacote seguindo a estrutura acima
3. Atualize o `registry/index.json`
4. Faça um Pull Request

## Pacotes Disponíveis

Veja `registry/index.json` para a lista completa de pacotes.
'''
    
    main_readme_file = Path("README.md")
    with open(main_readme_file, 'w', encoding='utf-8') as f:
        f.write(main_readme)
    print(f"✅ Criado: {main_readme_file}")
    
    # Criar .gitignore
    gitignore_content = '''# Cache
.naja_cache/
*.pyc
__pycache__/

# Logs
*.log

# Sistema
.DS_Store
Thumbs.db
'''
    
    gitignore_file = Path(".gitignore")
    with open(gitignore_file, 'w', encoding='utf-8') as f:
        f.write(gitignore_content)
    print(f"✅ Criado: {gitignore_file}")
    
    print("\n🎉 Estrutura do registry criada com sucesso!")
    print("\n📋 Próximos passos:")
    print("1. Commit e push para o GitHub:")
    print("   git add .")
    print("   git commit -m 'Configuração inicial do registry'")
    print("   git push origin main")
    print("\n2. Testar o package manager:")
    print("   python naja_pkg search exemplo")
    print("   python naja_pkg install exemplo-basico")

if __name__ == "__main__":
    create_registry_structure() 