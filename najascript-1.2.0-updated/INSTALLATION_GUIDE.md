# Guia de Instalação - NajaScript v1.2.0

## 🐧 Linux (Ubuntu/Debian)

### Método 1: Instalação via .deb (Recomendado)

```bash
# 1. Baixar o pacote
wget https://github.com/NajaScript/Naja/releases/download/v1.2.0/najascript-1.2.0-linux.deb

# 2. Instalar
sudo dpkg -i najascript-1.2.0-linux.deb

# 3. Resolver dependências (se necessário)
sudo apt-get install -f

# 4. Verificar instalação
najascript --version
naja_pkg --help
```

### Método 2: Instalação manual

```bash
# 1. Extrair arquivos
tar -xzf najascript-1.2.0-linux-structure.tar.gz

# 2. Copiar arquivos
sudo cp -r najascript-1.2.0-linux-structure/usr/* /usr/

# 3. Atualizar permissões
sudo chmod +x /usr/bin/najascript
sudo chmod +x /usr/bin/naja
sudo chmod +x /usr/bin/naja_pkg

# 4. Atualizar MIME types
sudo update-mime-database /usr/share/mime
sudo update-desktop-database /usr/share/applications
```

## 🪟 Windows

### Instalação Automática

1. **Baixar**: `NajaScript_Setup_v1.2.0.exe`
2. **Executar como Administrador**
3. **Seguir o assistente de instalação**
4. **Reiniciar o sistema** (se solicitado)

### Verificação

```cmd
# Prompt de Comando ou PowerShell
najascript --version
naja_pkg list
```

## 🧪 Teste da Instalação

### Teste Básico
```bash
# Criar arquivo de teste
echo 'println("Olá, NajaScript v1.2.0!");' > teste.naja

# Executar
najascript teste.naja
```

### Teste do Package Manager
```bash
# Listar pacotes disponíveis
naja_pkg list

# Instalar math-utils
naja_pkg install math-utils

# Testar biblioteca
echo 'import { pi, sqrt } from "math-utils"; println("Pi: " + pi()); println("√16: " + sqrt(16.0));' > teste_math.naja
najascript teste_math.naja
```

## 🔧 Resolução de Problemas

### Linux

**Erro: "comando não encontrado"**
```bash
# Verificar se está no PATH
echo $PATH | grep -q "/usr/bin" && echo "PATH OK" || echo "Adicionar /usr/bin ao PATH"

# Adicionar ao PATH (se necessário)
echo 'export PATH="/usr/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

**Erro de dependências**
```bash
# Instalar Python 3.6+
sudo apt-get update
sudo apt-get install python3 python3-pip

# Verificar versão
python3 --version
```

### Windows

**Erro: "não é reconhecido como comando"**
1. Verificar se NajaScript está no PATH do sistema
2. Reiniciar o Prompt de Comando
3. Executar como Administrador

**Erro de permissões**
1. Executar Prompt como Administrador
2. Verificar antivírus (pode bloquear)
3. Adicionar exceção para NajaScript

## 📚 Primeiros Passos

### 1. Hello World
```naja
fun main() {
    println("Olá, mundo!");
}

main();
```

### 2. Usando math-utils
```naja
import { pi, factorial, isPrime } from "math-utils";

fun demonstracao() {
    // Constantes
    println("Pi: " + pi());
    
    // Fatorial
    println("5! = " + factorial(5));
    
    // Números primos
    println("17 é primo: " + isPrime(17));
}

demonstracao();
```

### 3. Package Manager
```bash
# Ver pacotes instalados
naja_pkg list

# Procurar pacotes
naja_pkg search math

# Instalar pacote
naja_pkg install nome-do-pacote

# Informações do sistema
naja_pkg info
```

## 🆘 Suporte

- **Documentação**: https://najascript.github.io
- **Issues**: https://github.com/NajaScript/Naja/issues
- **Discussões**: https://github.com/NajaScript/Naja/discussions

---

**NajaScript v1.2.0 - Desenvolvido com ❤️ pela comunidade**
