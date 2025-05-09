# NajaScript Package Registry

O NajaScript Package Registry é um sistema completo para gerenciar, distribuir e descobrir pacotes para a linguagem NajaScript. Ele consiste em três componentes principais:

1. **Servidor de Registro** - Um servidor HTTP simples para hospedar pacotes
2. **Cliente de Registro** - Uma ferramenta CLI para interagir com o registro
3. **Interface Web** - Uma interface visual para navegar e gerenciar pacotes

## Requisitos

- Python 3.6+
- NajaScript Package Manager

## Instalação

Os arquivos do registro estão incluídos na distribuição padrão do NajaScript. Para verificar se eles estão instalados corretamente, execute:

```bash
python naja.py registry -h
```

Se receber uma mensagem de erro sobre módulos não encontrados, verifique se os seguintes arquivos estão presentes:

- `naja_registry_server.py`
- `naja_registry_client.py`
- `naja_registry_web.py`

## Iniciar um Servidor de Registro Local

Para iniciar um servidor de registro local:

```bash
python naja.py registry server
```

Isso iniciará o servidor na porta padrão (8765). Para especificar uma porta diferente:

```bash
python naja.py registry server --port 9000
```

O servidor armazenará os dados no diretório `naja_registry` por padrão. Para usar um diretório diferente:

```bash
python naja.py registry server --dir minha_pasta_registro
```

## Iniciar a Interface Web

A interface web permite navegar pelo registro de pacotes em um navegador:

```bash
python naja.py registry web
```

Isso iniciará a interface web na porta 8766. Acesse `http://localhost:8766` no seu navegador.

Para especificar uma porta diferente:

```bash
python naja.py registry web --port 9001
```

Se o servidor de registro estiver em um endereço diferente do padrão:

```bash
python naja.py registry web --registry http://servidor-remoto:8765
```

## Comandos do Cliente

### Definir URL do Registro

Para usar um registro diferente do padrão:

```bash
python naja.py registry set-registry http://meu-servidor:8765
```

### Buscar Pacotes

```bash
# Buscar todos os pacotes
python naja.py registry search

# Buscar pacotes por termo
python naja.py registry search MathUtils
```

### Ver Informações de um Pacote

```bash
# Informações gerais do pacote
python naja.py registry info MathUtils

# Informações de uma versão específica
python naja.py registry info MathUtils --version 1.0.0
```

### Instalar um Pacote

```bash
# Instalar a versão mais recente
python naja.py registry install MathUtils

# Instalar uma versão específica
python naja.py registry install MathUtils --version 1.0.0

# Instalar como dependência de desenvolvimento
python naja.py registry install MathUtils --dev
```

### Publicar um Pacote

```bash
# Publicar um pacote existente localmente
python naja.py registry publish MathUtils

# Especificar versão e descrição
python naja.py registry publish MathUtils --version 1.1.0 --description "Biblioteca de matemática avançada"
```

## API do Registro

O servidor de registro expõe uma API HTTP simples:

### Endpoints

- `GET /` - Informações sobre o registro
- `GET /packages` - Listar todos os pacotes
- `GET /package/{name}` - Obter informações de um pacote
- `GET /package/{name}/{version}` - Obter informações de uma versão específica
- `GET /download/{name}/{version}` - Baixar um pacote
- `GET /search?q={query}` - Buscar pacotes
- `POST /publish` - Publicar um pacote (requer autenticação)

## Diferenças em Relação ao Sistema Anterior

O novo sistema de registro oferece várias vantagens em relação ao sistema anterior baseado em GitHub:

1. **Interface Web** - Navegação visual de pacotes
2. **API Dedicada** - Endpoints específicos para cada operação
3. **Busca Avançada** - Busca por nome, descrição e outros metadados
4. **Empacotamento Simples** - Formato zip padronizado
5. **Hospedagem Local** - Não depende de serviços externos
6. **Integração Direta** - Comandos integrados ao CLI principal
7. **Escalabilidade** - Pode ser hospedado em qualquer servidor

## Exemplos de Uso

### Fluxo de trabalho típico para criar e publicar um pacote:

```bash
# Inicializar um projeto
mkdir meu-pacote
cd meu-pacote
python ../naja.py init

# Criar um pacote
python ../naja.py create MeuPacote --description "Meu incrível pacote"

# Iniciar servidor de registro (em outro terminal)
python ../naja.py registry server

# Publicar o pacote
python ../naja.py registry publish MeuPacote
```

### Consumir pacotes:

```bash
# Buscar pacotes disponíveis
python naja.py registry search

# Instalar um pacote
python naja.py registry install MeuPacote

# Usar o pacote em seu código NajaScript
# import MeuPacote from "MeuPacote";
```

## Configuração Avançada

O registro armazena sua configuração no arquivo `naja_registry_config.json`. Você pode editar este arquivo manualmente para configurações avançadas.

## Suporte e Contribuição

Para relatar problemas ou contribuir com o desenvolvimento do NajaScript Package Registry, visite o repositório oficial do NajaScript. 