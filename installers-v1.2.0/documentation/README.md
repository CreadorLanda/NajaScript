# NajaScript v1.2.0 - Instaladores Atualizados

## 🚀 Novidades da Versão 1.2.0

### ✅ Novas Funcionalidades:
- **🧮 Biblioteca math-utils**: 24 funções matemáticas completas
- **📦 Package Manager**: Sistema completo de gerenciamento de pacotes
- **🔧 Ferramentas aprimoradas**: Novos módulos e exemplos
- **📚 Documentação atualizada**: Guias completos e exemplos práticos

### 📦 Biblioteca Math Utils:
- Constantes matemáticas: pi(), e(), phi()
- Funções básicas: abs(), max(), min(), pow(), sqrt()
- Trigonometria: sin(), cos(), tan(), deg2rad(), rad2deg()
- Estatística: mean(), sum()
- Funções especiais: factorial(), fibonacci(), gcd(), lcm(), isPrime()
- Arredondamento: floor(), ceil(), round()

### 🛠️ Package Manager:
- Instalação de pacotes: `naja_pkg install package-name`
- Busca de pacotes: `naja_pkg search keyword`
- Listagem: `naja_pkg list`
- Registry integrado com GitHub

## 📥 Instalação

### Linux (Ubuntu/Debian):
```bash
# Baixar e instalar
wget https://github.com/NajaScript/Naja/releases/download/v1.2.0/najascript-1.2.0-linux.deb
sudo dpkg -i najascript-1.2.0-linux.deb

# Resolver dependências se necessário
sudo apt-get install -f
```

### Windows:
1. Baixar `NajaScript_Setup_v1.2.0.exe`
2. Executar como administrador
3. Seguir instruções do instalador

## 🎯 Uso Rápido

```bash
# Verificar instalação
najascript --version

# Executar programa
najascript meu_programa.naja

# Gerenciar pacotes
naja_pkg list
naja_pkg install math-utils

# Usar biblioteca math-utils
```

```naja
import { pi, sqrt, factorial } from "math-utils";

fun exemplo() {
    float area = pi() * pow(5.0, 2);
    int fat = factorial(5);
    println("Área: " + area);
    println("5! = " + fat);
}
```

## 🔗 Links Úteis

- **Documentação**: https://najascript.github.io
- **Repositório**: https://github.com/NajaScript/Naja
- **Issues**: https://github.com/NajaScript/Naja/issues

## 📝 Changelog v1.2.0

- ✅ Adicionada biblioteca math-utils completa
- ✅ Sistema de package manager funcional
- ✅ Registry de pacotes integrado
- ✅ Novos exemplos e documentação
- ✅ Melhorias na sintaxe e performance
- ✅ Suporte aprimorado para Linux e Windows

---

**Feito com ❤️ pela comunidade NajaScript**
