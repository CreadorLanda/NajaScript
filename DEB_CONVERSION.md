# Conversão para .deb no Linux

## Método 1: Usando dpkg-deb (Recomendado)

```bash
# No sistema Linux com dpkg:
cd najascript-1.2.0-updated/linux/
dpkg-deb --build najascript-1.2.0-linux-structure najascript_1.2.0_all.deb

# Verificar pacote criado
dpkg-deb --info najascript_1.2.0_all.deb
dpkg-deb --contents najascript_1.2.0_all.deb
```

## Método 2: Instalação Manual

```bash
# Usar o script de instalação
chmod +x install_najascript.sh
sudo ./install_najascript.sh

# Para desinstalar
chmod +x uninstall_najascript.sh
sudo ./uninstall_najascript.sh
```

## Método 3: Usando o Tarball

```bash
# Extrair e instalar manualmente
tar -xzf najascript_1.2.0_all.tar.gz
sudo cp -r najascript_1.2.0_all/usr/* /usr/
sudo chmod +x /usr/bin/najascript /usr/bin/naja /usr/bin/naja_pkg
sudo update-mime-database /usr/share/mime
sudo update-desktop-database /usr/share/applications
```

## Teste da Instalação

```bash
# Verificar instalação
najascript --version

# Testar package manager
naja_pkg list

# Testar math-utils
echo 'import { pi } from "math-utils"; println("Pi: " + pi());' > test.naja
najascript test.naja
```

## Estrutura do Pacote

- **Package**: najascript
- **Version**: 1.2.0
- **Architecture**: all
- **Depends**: python3 (>= 3.6), python3-pip
- **Maintainer**: NajaScript Team
- **Size**: ~4 MB

## Upload para Repositório

```bash
# Após criar o .deb:
# 1. Testar instalação em sistema limpo
# 2. Verificar dependências
# 3. Upload para GitHub Releases
# 4. Atualizar documentação
```
