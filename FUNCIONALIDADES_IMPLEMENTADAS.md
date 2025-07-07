# Funcionalidades Implementadas no NajaScript

## Resumo das Melhorias

O NajaScript agora possui funcionalidades modernas padrão incluindo:

### ✅ 1. Sistema de Eventos Completo
- Sistema de eventos global
- EventEmitter personalizado
- Suporte a listeners únicos (once)
- Múltiplos aliases para compatibilidade

### ✅ 2. Suporte JSON Nativo  
- JSON.stringify() e JSON.parse()
- Conversão automática entre tipos NajaScript e JSON
- Funciona sem necessidade de imports

### ✅ 3. Fetch API para Requisições HTTP
- fetch() nativo similar ao JavaScript
- Suporte a GET, POST, PUT, DELETE, PATCH
- Response object com métodos text(), json(), blob()
- Funções auxiliares get() e post()

## Documentação Detalhada

### Sistema de Eventos

```javascript
// Adicionar listener para evento
addEventListener("evento", funcao);

// Listener que executa apenas uma vez
once("evento", funcao);

// Disparar evento
dispatchEvent("evento", dados...);

// Remover listener
removeEventListener("evento", funcao);

// Aliases disponíveis
on("evento", funcao);      // = addEventListener
off("evento", funcao);     // = removeEventListener  
emit("evento", dados);     // = dispatchEvent
trigger("evento", dados);  // = dispatchEvent

// EventEmitter personalizado
emitter = createEventEmitter();
emitter.on("evento", funcao);
emitter.emit("evento", dados);
```

### JSON

```javascript
// Serializar objeto para JSON
dicionario dados = {};
dados.add("nome", "João");
dados.add("idade", 30);

// JSON está disponível globalmente
println(JSON.stringify); // função disponível
println(JSON.parse);     // função disponível

// Nota: Sintaxe JSON.stringify(dados) tem limitação no parser atual
// Use: stringify_func = JSON.stringify; resultado = stringify_func(dados);
```

### Fetch API

```javascript  
// Fetch básico
response = fetch("https://api.exemplo.com/dados");

// Fetch com opções
dicionario opcoes = {};
opcoes.add("method", "POST");
opcoes.add("body", dados);
response = fetch("https://api.exemplo.com/enviar", opcoes);

// Funções auxiliares
response = get("https://api.exemplo.com/dados");
response = post("https://api.exemplo.com/enviar", dados);

// Response object
println(response.status);  // código HTTP
println(response.ok);      // boolean para sucesso
texto = response.text();   // corpo como texto
dados = response.json();   // corpo como objeto
```

## Exemplos Práticos

### Sistema de Notificações

```javascript
funcao processarNotificacao(titulo, mensagem) {
    println("📢 " + titulo + ": " + mensagem)
}

addEventListener("notificacao", processarNotificacao);
dispatchEvent("notificacao", "Nova Mensagem", "Você tem uma nova mensagem!");
```

### Chat Simulado

```javascript
funcao onMensagem(usuario, texto) {
    println("[" + usuario + "] " + texto)
}

funcao onUsuarioEntrou(nome) {
    println("👤 " + nome + " entrou no chat")
}

addEventListener("mensagem", onMensagem);
addEventListener("usuario_entrou", onUsuarioEntrou);

dispatchEvent("usuario_entrou", "João");
dispatchEvent("mensagem", "João", "Olá pessoal!");
```

### Sistema de Estados

```javascript
// EventEmitter para gerenciar estados
estado = createEventEmitter();

funcao onMudancaEstado(novoEstado) {
    println("Estado alterado para: " + novoEstado)
}

estado.on("mudanca", onMudancaEstado);
estado.emit("mudanca", "logado");
estado.emit("mudanca", "carregando");
```

## Características Técnicas

### Sistema de Eventos
- **Classe EventEmitter**: Implementação completa similar ao Node.js
- **Listeners únicos**: Suporte a `once()` que remove automaticamente
- **Múltiplos argumentos**: Eventos podem carregar múltiplos dados
- **Tratamento de erros**: Erros em listeners não quebram o sistema
- **Limite de listeners**: Proteção contra vazamentos de memória

### JSON
- **Conversão automática**: NajaDict ↔ JSON object, NajaList ↔ JSON array
- **Tipos suportados**: string, int, float, bool, dict, list
- **Tratamento de erros**: Mensagens claras para JSON inválido
- **Fallback**: Funciona mesmo se módulo requests não estiver disponível

### Fetch
- **Métodos HTTP**: GET, POST, PUT, DELETE, PATCH
- **Headers automáticos**: User-Agent e Content-Type padrão
- **Conversão JSON**: Body automático para objetos NajaScript
- **Response padronizado**: Interface similar ao JavaScript Fetch API
- **Tratamento de erros**: Exceptions claras para problemas de rede

## Compatibilidade

- ✅ **Sem imports**: Todas as funcionalidades são padrão
- ✅ **Backward compatible**: Não quebra código existente  
- ✅ **Cross-platform**: Funciona em Windows, Linux, macOS
- ✅ **Dependencies mínimas**: JSON funciona sem bibliotecas externas
- ⚠️ **Fetch requer requests**: pip install requests para funcionalidade HTTP

## Limitações Conhecidas

1. **Parser JSON**: `JSON.stringify(obj)` requer sintaxe alternativa atualmente
2. **Fetch offline**: Requisições HTTP precisam de conexão de rede
3. **EventEmitter methods**: Alguns métodos avançados ainda não implementados

## Próximos Passos Sugeridos

1. Corrigir parser para suportar `JSON.stringify(obj)` diretamente
2. Adicionar suporte a WebSockets
3. Implementar sistema de Promises/async-await
4. Adicionar localStorage/sessionStorage
5. Sistema de roteamento para aplicações web

---

**Status**: ✅ IMPLEMENTADO E FUNCIONANDO
**Versão**: NajaScript 1.0 com funcionalidades modernas
**Data**: Janeiro 2024 