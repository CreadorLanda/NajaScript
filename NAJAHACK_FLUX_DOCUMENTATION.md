# NajaScript - Biblioteca NajaHack & Sistema Flux Reativo

## Introdução

Esta documentação cobre duas novas funcionalidades implementadas no NajaScript:

1. **Biblioteca NajaHack**: Ferramentas avançadas para hackers éticos e profissionais de segurança
2. **Sistema Flux Reativo**: Tipo de dados que se atualiza automaticamente quando suas dependências mudam

## Biblioteca NajaHack

A biblioteca `najahack` fornece uma coleção abrangente de ferramentas para testes de segurança, análise de vulnerabilidades e operações de hacking ético.

### Funcionalidades Principais

#### 1. Informações de Rede
```naja
dicionario info = najahack.networkInfo();
println("Hostname: " + info.get("hostname"));
println("IP Local: " + info.get("local_ip"));
println("Plataforma: " + info.get("platform"));
```

#### 2. Informações do Sistema
```naja
dicionario sysInfo = najahack.systemInfo();
println("Sistema: " + sysInfo.get("system"));
println("Usuário: " + sysInfo.get("user"));
println("Máquina: " + sysInfo.get("machine"));
```

#### 3. Escaneamento de Portas
```naja
lista portasAbertas = najahack.portScan("127.0.0.1", 80, 8080);
println("Portas abertas: " + portasAbertas.length());
```

#### 4. Quebra de Hash
```naja
string hash = md5("password123");
any resultado = najahack.hashCrack(hash);
if (resultado != null) {
    println("Senha: " + resultado.password);
    println("Tipo: " + resultado.type);
}
```

#### 5. Brute Force
```naja
string hashAlvo = md5("abc");
any resultado = najahack.bruteForce(hashAlvo, "abcdefghijklmnopqrstuvwxyz", 3);
if (resultado != null) {
    println("Senha encontrada: " + resultado.password);
}
```

#### 6. Teste de Injeção SQL
```naja
lista resultados = najahack.sqlInject("https://exemplo.com/login");
for (int i = 0; i < resultados.length(); i++) {
    dicionario resultado = resultados.get(i);
    println("Payload: " + resultado.get("payload"));
    println("Status: " + resultado.get("status"));
}
```

#### 7. Teste de XSS
```naja
lista resultados = najahack.xssTest("https://exemplo.com/search");
for (int i = 0; i < resultados.length(); i++) {
    dicionario resultado = resultados.get(i);
    println("Payload: " + resultado.get("payload"));
    println("Refletido: " + resultado.get("reflected"));
}
```

#### 8. Esteganografia
```naja
// Esconder mensagem
string resultado = najahack.steganography("hide", "imagem.png", "Mensagem secreta", "saida.png");
println(resultado);

// Extrair mensagem
string mensagem = najahack.steganography("extract", "saida.png");
println("Mensagem extraída: " + mensagem);
```

#### 9. Lookup Reverso de DNS
```naja
string hostname = najahack.reverseLookup("8.8.8.8");
println("Hostname: " + hostname);
```

#### 10. Consulta WHOIS
```naja
string whoisInfo = najahack.whois("google.com");
println(whoisInfo);
```

#### 11. Informações de Processos
```naja
lista processos = najahack.processInfo();
for (int i = 0; i < processos.length(); i++) {
    dicionario proc = processos.get(i);
    println("PID: " + proc.get("pid") + ", Nome: " + proc.get("name"));
}
```

### API Completa da Biblioteca NajaHack

| Método | Descrição | Parâmetros | Retorno |
|--------|-----------|------------|---------|
| `networkInfo()` | Obtém informações da rede | Nenhum | `dicionario` |
| `systemInfo()` | Obtém informações do sistema | Nenhum | `dicionario` |
| `portScan(host, start, end)` | Escaneia portas | `string`, `int`, `int` | `lista` |
| `hashCrack(hash, wordlist?)` | Quebra hash | `string`, `lista?` | `any` |
| `bruteForce(hash, charset, maxLen)` | Força bruta | `string`, `string`, `int` | `any` |
| `sqlInject(url, payloads?)` | Testa SQL injection | `string`, `lista?` | `lista` |
| `xssTest(url, payloads?)` | Testa XSS | `string`, `lista?` | `lista` |
| `steganography(action, image, msg?, out?)` | Esteganografia | `string`, `string`, `string?`, `string?` | `string` |
| `reverseLookup(ip)` | Lookup reverso DNS | `string` | `string` |
| `whois(domain)` | Consulta WHOIS | `string` | `string` |
| `processInfo()` | Lista processos | Nenhum | `lista` |

## Sistema Flux Reativo

O tipo `flux` é um tipo de dados reativo que se atualiza automaticamente quando as variáveis das quais depende são alteradas.

### Sintaxe Básica

```naja
int a = 10;
int b = 20;
flux soma = a + b;  // soma = 30

a = 50;  // soma automaticamente vira 70
```

### Características do Flux

1. **Reativo**: Atualiza automaticamente quando dependências mudam
2. **Transparente**: Funciona como uma variável normal
3. **Eficiente**: Só recalcula quando necessário
4. **Suporte a Tipos**: Funciona com todos os tipos de dados

### Exemplos de Uso

#### Exemplo 1: Matemática Básica
```naja
float x = 5.0;
float y = 3.0;
float z = 2.0;

flux area = x * y;           // 15.0
flux volume = x * y * z;     // 30.0
flux perimeter = 2 * (x + y); // 16.0

x = 10.0;
// Todos os flux são atualizados automaticamente:
// area = 30.0, volume = 60.0, perimeter = 26.0
```

#### Exemplo 2: Strings
```naja
string firstName = "John";
string lastName = "Doe";

flux fullName = firstName + " " + lastName;  // "John Doe"

firstName = "Jane";
// fullName automaticamente vira "Jane Doe"
```

#### Exemplo 3: Booleanos
```naja
int score = 85;
int minScore = 60;

flux passed = score >= minScore;  // true

score = 45;
// passed automaticamente vira false
```

#### Exemplo 4: Listas
```naja
lista numbers = [1, 2, 3, 4, 5];
int multiplier = 2;

flux total = numbers.length() * multiplier;  // 10

numbers.add(6);
// total automaticamente vira 12
```

#### Exemplo 5: Flux Aninhado
```naja
int base = 5;
int height = 8;

flux triangleArea = (base * height) / 2;        // 20
flux triangleAreaText = "Área: " + triangleArea; // "Área: 20"

base = 10;
// triangleArea vira 40
// triangleAreaText vira "Área: 40"
```

### Como Funciona

1. **Análise de Dependências**: O sistema analisa a expressão do flux para identificar variáveis dependentes
2. **Rastreamento**: Quando uma variável muda, o sistema identifica todos os flux que dependem dela
3. **Atualização Automática**: Os flux são recalculados automaticamente
4. **Cache**: Valores são armazenados em cache para eficiência

### Casos de Uso Práticos

#### Interface Reativa
```naja
int width = 100;
int height = 200;

flux area = width * height;
flux aspectRatio = width / height;
flux displayText = "Dimensões: " + width + "x" + height + " (área: " + area + ")";
```

#### Validação de Formulários
```naja
string email = "user@example.com";
string password = "123456";

flux emailValid = email.includes("@") && email.includes(".");
flux passwordValid = password.length() >= 8;
flux formValid = emailValid && passwordValid;
```

#### Cálculos Financeiros
```naja
float principal = 1000.0;
float rate = 0.05;
int years = 3;

flux interest = principal * rate * years;
flux total = principal + interest;
```

### Limitações Atuais

1. **Mutação de Objetos**: Mudanças internas em objetos podem não ser detectadas
2. **Funções Assíncronas**: Flux não funciona com operações assíncronas
3. **Referências Circulares**: Devem ser evitadas para prevenir loops infinitos

### Melhores Práticas

1. **Use para Cálculos**: Ideais para valores que dependem de outros
2. **Mantenha Simples**: Expressões complexas podem impactar performance
3. **Evite Efeitos Colaterais**: Expressões devem ser puras
4. **Teste Dependências**: Verifique se todas as dependências são capturadas

## Compatibilidade e Requisitos

### Biblioteca NajaHack

Algumas funcionalidades da biblioteca `najahack` podem requerer bibliotecas Python adicionais:

- **Port Scanning**: Nenhuma dependência extra
- **Hash Cracking**: `hashlib` (padrão)
- **Process Info**: `psutil` (opcional)
- **Network Tests**: `requests` (opcional)
- **Steganography**: `PIL/Pillow` (opcional)

### Sistema Flux

O sistema flux é nativo e não requer dependências externas.

## Segurança e Ética

⚠️ **IMPORTANTE**: As ferramentas da biblioteca `najahack` devem ser usadas apenas para:

1. **Testes de Segurança Autorizados**: Em sistemas próprios ou com permissão explícita
2. **Educação**: Para aprender sobre segurança e vulnerabilidades
3. **Hacking Ético**: Seguindo práticas éticas e legais

**NÃO USE** para:
- Acesso não autorizado a sistemas
- Atividades ilegais
- Danos maliciosos

## Exemplos de Arquivos

- `exemplos/teste_najahack.naja`: Demonstração completa da biblioteca najahack
- `exemplos/teste_flux_reativo.naja`: Demonstração do sistema flux reativo

## Conclusão

As novas funcionalidades expandem significativamente as capacidades do NajaScript:

- **NajaHack**: Torna o NajaScript uma ferramenta poderosa para profissionais de segurança
- **Flux Reativo**: Adiciona programação reativa moderna, similar a frameworks como SolidJS e Vue

Essas implementações mantêm a simplicidade e poder do NajaScript enquanto adicionam funcionalidades avançadas para casos de uso especializados. 