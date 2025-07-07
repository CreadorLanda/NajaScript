# NajaScript v1.2.0 - Windows

## 🚀 Instalação Concluída!

NajaScript foi instalado com sucesso em seu sistema Windows.

## 🎯 Como Usar

### Executar Programas
```cmd
# Executar um arquivo .naja
najascript meu_programa.naja

# Ver ajuda
najascript --help

# Verificar versão
najascript --version
```

### Package Manager
```cmd
# Listar pacotes disponíveis
naja_pkg list

# Instalar um pacote
naja_pkg install math-utils

# Buscar pacotes
naja_pkg search matemática

# Ver ajuda do package manager
naja_pkg --help
```

## 🧮 Biblioteca Math-Utils Incluída

A biblioteca math-utils com 24 funções matemáticas está pré-instalada:

```naja
import { pi, sqrt, sin, cos, factorial } from "math-utils";

fun exemplo_matematica() {
    // Constantes
    println("Pi: " + pi());
    
    // Funções básicas
    println("√25: " + sqrt(25.0));
    
    // Trigonometria
    println("sin(90°): " + sin(deg2rad(90.0)));
    
    // Funções especiais
    println("5! = " + factorial(5));
}

exemplo_matematica();
```

## 📁 Estrutura de Arquivos

```
C:\Program Files\NajaScript\
├── najascript.py          # Interpretador principal
├── najascript.bat         # Launcher Windows
├── naja_pkg.bat          # Package manager
├── modules\              # Módulos padrão
├── packages\             # Pacotes instalados
├── examples\             # Exemplos de código
└── assets\               # Recursos e ícones
```

## 📚 Exemplos Incluídos

Na pasta `examples\`:
- `hello_world.naja` - Primeiro programa
- `calculator.naja` - Calculadora simples
- `teste_class.naja` - Programação orientada a objetos
- `complete_math_test.naja` - Teste da biblioteca matemática
- `flappy_bird_completo.naja` - Jogo completo

## 🔧 Resolução de Problemas

### "Python não encontrado"
1. Instale Python 3.6+ de https://python.org
2. Certifique-se de marcar "Add to PATH" durante a instalação
3. Reinicie o Prompt de Comando

### "Comando não reconhecido"
1. Verifique se NajaScript está no PATH do sistema
2. Reinicie o Prompt de Comando
3. Execute como Administrador se necessário

### Problemas com Pacotes
```cmd
# Verificar configuração
naja_pkg info

# Limpar cache
naja_pkg clear-cache

# Reinstalar math-utils
naja_pkg install math-utils --force
```

## 🆘 Suporte

- **Documentação**: https://najascript.github.io
- **Issues**: https://github.com/NajaScript/Naja/issues
- **Discussões**: https://github.com/NajaScript/Naja/discussions

## 📝 Changelog v1.2.0

- ✅ Sistema de package manager funcional
- ✅ Biblioteca math-utils com 24 funções
- ✅ Melhorias na sintaxe e performance
- ✅ Novos exemplos e documentação
- ✅ Suporte aprimorado para Windows

---

**Desenvolvido com ❤️ pela comunidade NajaScript**
