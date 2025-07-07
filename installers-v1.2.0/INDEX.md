# NajaScript v1.2.0 - Instaladores

## 📅 Informações da Build

- **Data**: 07/07/2025 13:21
- **Versão**: 1.2.0
- **Plataformas**: Linux (Ubuntu/Debian), Windows

## 🚀 Novidades da Versão 1.2.0

### ✅ Funcionalidades Incluídas:
- **🧮 Biblioteca math-utils**: 24 funções matemáticas completas
- **📦 Package Manager**: Sistema completo de gerenciamento de pacotes
- **🔧 Ferramentas aprimoradas**: Novos módulos e exemplos
- **📚 Documentação atualizada**: Guias completos e exemplos práticos

### 📦 Conteúdo dos Instaladores:
- Interpretador NajaScript completo
- Package Manager integrado (naja_pkg)
- Biblioteca math-utils pré-instalada
- Módulos padrão: NajaGame, NajaHack, Matematica, Basico
- Exemplos de código
- Documentação e guias

## 📁 Estrutura dos Arquivos

### 🐧 Linux (`linux/`)
```
- DEB_CONVERSION.md (1.6 KB) - SHA256: 9696f87cab8705d5...
- install_najascript.sh (1.4 KB) - SHA256: 5f16b39452d4be0e...
- najascript_1.2.0_all.tar.gz (3.9 MB) - SHA256: d7116e0ce63ac166...
- uninstall_najascript.sh (1.0 KB) - SHA256: 0c891def436823e8...
```

### 🪟 Windows (`windows/`)
```
- BUILD_INSTRUCTIONS.md (2.3 KB) - SHA256: e54ac95756d98511...
- LICENSE.txt (1.1 KB) - SHA256: 3b00cd9d36e084b0...
- naja.bat (73 B) - SHA256: 3ccef84725e3b85b...
- najascript.bat (569 B) - SHA256: bb826f4ae529172f...
- najascript_setup.iss (5.5 KB) - SHA256: 594b97203036aa2f...
- naja_pkg.bat (518 B) - SHA256: 337a0833f1132785...
- POST_INSTALL.txt (1.2 KB) - SHA256: 61bdcb5fd71398b0...
- README_WINDOWS.md (2.9 KB) - SHA256: 99dde343bd97d89f...
```

### 📚 Documentação (`documentation/`)
```
- INSTALLATION_GUIDE.md (3.5 KB)
- README.md (2.3 KB)
```

## 🛠️ Instruções de Instalação

### 🐧 Linux (Ubuntu/Debian)

#### Método 1: Script Automático (Recomendado)
```bash
# Download e extração
wget https://github.com/NajaScript/Naja/releases/download/v1.2.0/najascript_1.2.0_all.tar.gz
tar -xzf najascript_1.2.0_all.tar.gz

# Instalação automática
chmod +x install_najascript.sh
sudo ./install_najascript.sh
```

#### Método 2: Conversão para .deb
```bash
# No sistema Linux com dpkg-deb:
cd najascript-1.2.0-linux-structure
dpkg-deb --build . ../najascript_1.2.0_all.deb
sudo dpkg -i ../najascript_1.2.0_all.deb
```

### 🪟 Windows

#### Instalador Automático
1. **Compilar instalador** (requer Inno Setup):
   ```cmd
   ISCC.exe najascript_setup.iss
   ```

2. **Executar instalador**:
   - Executar `NajaScript_Setup_v1.2.0.exe` como Administrador
   - Seguir assistente de instalação
   - Marcar "Adicionar ao PATH do sistema"

3. **Verificar instalação**:
   ```cmd
   najascript --version
   naja_pkg list
   ```

## 🧪 Teste dos Instaladores

### Teste Básico
```bash
# Linux/Windows
najascript --version
echo 'println("Hello, NajaScript v1.2.0!");' > test.naja
najascript test.naja
```

### Teste da Biblioteca Math-Utils
```bash
echo 'import { pi, sqrt, factorial } from "math-utils"; println("Pi: " + pi()); println("√16: " + sqrt(16.0)); println("5! = " + factorial(5));' > math_test.naja
najascript math_test.naja
```

### Teste do Package Manager
```bash
naja_pkg list
naja_pkg search math
naja_pkg info
```

## 🔗 Links Úteis

- **Site**: https://najascript.github.io
- **Repositório**: https://github.com/NajaScript/Naja
- **Documentação**: https://najascript.github.io/documentation
- **Issues**: https://github.com/NajaScript/Naja/issues
- **Releases**: https://github.com/NajaScript/Naja/releases

## 📝 Checklist de Release

### Antes do Release:
- [ ] Testar instalador Linux em sistema limpo
- [ ] Compilar e testar instalador Windows
- [ ] Verificar todas as dependências
- [ ] Testar math-utils e package manager
- [ ] Validar documentação

### Durante o Release:
- [ ] Criar tag Git: `git tag v1.2.0`
- [ ] Push da tag: `git push origin v1.2.0`
- [ ] Criar GitHub Release
- [ ] Upload dos instaladores
- [ ] Atualizar site de documentação
- [ ] Anunciar nas redes sociais

### Após o Release:
- [ ] Monitorar issues e feedback
- [ ] Atualizar estatísticas de download
- [ ] Documentar problemas conhecidos

---

**Desenvolvido com ❤️ pela comunidade NajaScript**

Build: 20250707-1321
