# 📦 NajaScript v1.2.0 - Guia de Instalação Completo

## 🚀 Novidades da Versão 1.2.0

### ✅ Principais Funcionalidades:
- **🧮 Biblioteca math-utils**: 24 funções matemáticas completas
- **📦 Package Manager**: Sistema completo de gerenciamento de pacotes
- **🔧 Ferramentas aprimoradas**: Novos módulos e exemplos
- **📚 Documentação atualizada**: Guias completos e exemplos práticos

## 📥 Downloads Disponíveis

### 🐧 Linux (Ubuntu/Debian)
- **Arquivo**: `najascript-1.2.0-linux-structure.tar.gz` (3.9 MB)
- **Compatibilidade**: Ubuntu 20.04+, Debian 11+, Fedora 34+
- **Dependências**: Python 3.6+, pip

### 🪟 Windows
- **Arquivo**: `NajaScript_Setup_v1.2.0.exe` (8 MB)
- **Compatibilidade**: Windows 10, Windows 11
- **Arquitetura**: x64

## 🔧 Instalação - Linux

### Método 1: Instalação Rápida (Recomendado)

```bash
# 1. Baixar o arquivo
wget https://github.com/NajaScript/Naja/releases/download/v1.2.0/najascript-1.2.0-linux-structure.tar.gz

# 2. Extrair o arquivo
tar -xzf najascript-1.2.0-linux-structure.tar.gz

# 3. Converter para pacote .deb
cd najascript-1.2.0-linux-structure
dpkg-deb --build . ../najascript_1.2.0.deb

# 4. Instalar o pacote
cd ..
sudo dpkg -i najascript_1.2.0.deb
sudo apt-get install -f  # Resolver dependências se necessário
```

### Método 2: Instalação Manual

```bash
# 1. Extrair arquivo
tar -xzf najascript-1.2.0-linux-structure.tar.gz

# 2. Copiar arquivos manualmente
sudo cp -r najascript-1.2.0-linux-structure/usr/* /usr/

# 3. Tornar executáveis
sudo chmod +x /usr/bin/najascript
sudo chmod +x /usr/bin/naja
sudo chmod +x /usr/bin/naja_pkg

# 4. Atualizar banco de dados MIME
sudo update-mime-database /usr/share/mime
sudo update-desktop-database /usr/share/applications
```

### Verificação da Instalação

```bash
# Verificar versão
najascript --version

# Testar package manager
naja_pkg list

# Executar programa de teste
echo 'println("Olá, NajaScript!");' > teste.naja
najascript teste.naja
```

## 🔧 Instalação - Windows

### Instalação com Executável

1. **Baixar** o arquivo `NajaScript_Setup_v1.2.0.exe`
2. **Executar como Administrador** (botão direito → "Executar como administrador")
3. **Seguir o assistente** de instalação
4. **Reiniciar** o prompt de comando após a instalação

### Instalação Manual (Inno Setup)

Se você tem o Inno Setup instalado:

```batch
# Compilar instalador manualmente
ISCC.exe najascript_setup.iss
```

### Verificação da Instalação

```batch
# Verificar versão
najascript --version

# Testar package manager
naja_pkg list

# Executar programa de teste
echo println("Olá, NajaScript!"); > teste.naja
najascript teste.naja
```

## 📦 Usando o Package Manager

### Comandos Básicos

```bash
# Listar pacotes disponíveis
naja_pkg list

# Instalar um pacote
naja_pkg install math-utils

# Buscar pacotes
naja_pkg search math

# Informações sobre um pacote
naja_pkg info math-utils

# Desinstalar um pacote
naja_pkg uninstall math-utils
```

### Usando a Biblioteca Math-Utils

```naja
// Importar funções matemáticas
import { pi, sqrt, factorial, sin, cos, deg2rad } from "math-utils";

fun exemplo_matematico() {
    // Constantes
    float pi_value = pi();
    float e_value = e();
    
    // Cálculos básicos
    float area = pi() * pow(5.0, 2);
    float hipotenusa = sqrt(pow(3.0, 2) + pow(4.0, 2));
    
    // Funções especiais
    int fatorial_5 = factorial(5);
    bool eh_primo = isPrime(17);
    
    // Trigonometria
    float seno_90 = sin(deg2rad(90.0));
    float coseno_0 = cos(deg2rad(0.0));
    
    println("π = " + pi_value);
    println("Área do círculo (r=5): " + area);
    println("Hipotenusa (3,4): " + hipotenusa);
    println("5! = " + fatorial_5);
    println("17 é primo: " + eh_primo);
    println("sin(90°) = " + seno_90);
}

exemplo_matematico();
```

## 🧮 Funções da Biblioteca Math-Utils

### Constantes Matemáticas
- `pi()` - Valor de π (pi)
- `e()` - Número de Euler
- `phi()` - Proporção áurea

### Funções Básicas
- `abs(x)` - Valor absoluto
- `max(a, b)` - Valor máximo
- `min(a, b)` - Valor mínimo
- `pow(base, exp)` - Potenciação
- `sqrt(x)` - Raiz quadrada

### Trigonometria
- `sin(x)` - Seno (radianos)
- `cos(x)` - Cosseno (radianos)
- `tan(x)` - Tangente (radianos)
- `deg2rad(x)` - Graus para radianos
- `rad2deg(x)` - Radianos para graus

### Estatística
- `mean(lista)` - Média aritmética
- `sum(lista)` - Soma dos elementos
- `factorial(n)` - Fatorial

### Arredondamento
- `floor(x)` - Arredondar para baixo
- `ceil(x)` - Arredondar para cima
- `round(x)` - Arredondar normal

### Funções Especiais
- `gcd(a, b)` - Máximo divisor comum
- `lcm(a, b)` - Mínimo múltiplo comum
- `isPrime(n)` - Verificar se é primo

## 🛠️ Solução de Problemas

### Linux

**Problema**: `najascript: command not found`
```bash
# Verificar se está no PATH
echo $PATH | grep "/usr/bin"

# Adicionar manualmente se necessário
export PATH="/usr/bin:$PATH"
echo 'export PATH="/usr/bin:$PATH"' >> ~/.bashrc
```

**Problema**: Erro de permissão
```bash
# Corrigir permissões
sudo chmod +x /usr/bin/najascript
sudo chmod +x /usr/bin/naja_pkg
```

### Windows

**Problema**: `'najascript' is not recognized`
```batch
# Verificar variável PATH
echo %PATH%

# Adicionar manualmente:
# Painel de Controle → Sistema → Variáveis de Ambiente
# Adicionar: C:\Program Files\NajaScript\
```

**Problema**: Erro de permissão
- Executar prompt como Administrador
- Executar instalador como Administrador

## 📚 Links Úteis

- **Documentação**: https://najascript.github.io
- **Repositório**: https://github.com/NajaScript/Naja
- **Issues**: https://github.com/NajaScript/Naja/issues
- **Releases**: https://github.com/NajaScript/Naja/releases

## 📝 Changelog v1.2.0

- ✅ Adicionada biblioteca math-utils completa (24 funções)
- ✅ Sistema de package manager funcional
- ✅ Registry de pacotes integrado com GitHub
- ✅ Novos exemplos e documentação
- ✅ Melhorias na sintaxe e performance
- ✅ Suporte aprimorado para Linux e Windows
- ✅ Instaladores automáticos para ambas plataformas

---

**🎉 Bem-vindo ao NajaScript v1.2.0!**

*Desenvolvido com ❤️ pela comunidade NajaScript* 