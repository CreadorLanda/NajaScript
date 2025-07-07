# NajaScript Modern Features Documentation

## Overview
NajaScript agora possui todas as funcionalidades modernas similares ao JavaScript, tornando-se uma linguagem robusta e atual para desenvolvimento.

## 🚀 Funcionalidades Implementadas

### 1. Console Avançado
```naja
console.log("Standard message");
console.warn("Warning message");
console.error("Error message");
console.info("Info message");
console.debug("Debug message");
console.table(data);  // Tabela formatada
console.clear();      // Limpar console
console.time("label");    // Iniciar timer
console.timeEnd("label"); // Finalizar timer
```

### 2. Crypto & Hash
```naja
// Hash functions
string hash_md5 = crypto.md5("text");
string hash_sha1 = crypto.sha1("text");
string hash_sha256 = crypto.sha256("text");

// Random generation
string uuid = crypto.randomUUID();
string randomData = crypto.randomBytes(16);

// Base64 encoding/decoding
string encoded = crypto.base64Encode("text");
string decoded = crypto.base64Decode(encoded);
```

### 3. DateTime Avançado
```naja
// Criar instâncias
any now = DateTime.now();
any specific = DateTime(2024, 12, 25, 10, 30, 0);
any fromTimestamp = DateTime.fromTimestamp(1640995200);

// Formatação
string formatted = now.format("%Y-%m-%d %H:%M:%S");

// Getters
int year = now.getYear();
int month = now.getMonth();
int day = now.getDay();
int hour = now.getHour();
int minute = now.getMinute();
int second = now.getSecond();
int timestamp = now.getTimestamp();

// Operações
any future = now.addDays(7);
any laterToday = now.addHours(3);
```

### 4. Regex (Expressões Regulares)
```naja
// Criar regex
any regex = Regex("\\d+", "g");

// Métodos
bool matches = regex.test("text 123");
string firstMatch = regex.match("text 123");
list allMatches = regex.matchAll("text 123 and 456");
string replaced = regex.replace("text 123", "NUMBER");
list parts = regex.split("word1 word2 word3");

// Funções globais
list matches = match("text 123", "\\d+");
string newText = replace("text 123", "\\d+", "NUMBER");
```

### 5. Timers
```naja
// Timeout (executa uma vez)
fun callback() {
    println("Executed after delay!");
}
int timeoutId = setTimeout(callback, 1000);  // 1 segundo
clearTimeout(timeoutId);

// Interval (executa repetidamente)
int intervalId = setInterval(callback, 2000);  // A cada 2 segundos
clearInterval(intervalId);
```

### 6. Storage (Armazenamento Local)
```naja
// localStorage (persistente)
localStorage.setItem("key", "value");
string value = localStorage.getItem("key");
localStorage.removeItem("key");
localStorage.clear();
int length = localStorage.length();
string keyAt = localStorage.key(0);

// sessionStorage (temporário)
sessionStorage.setItem("sessionKey", "sessionValue");
string sessionValue = sessionStorage.getItem("sessionKey");
// Mesmos métodos do localStorage
```

### 7. Array/List Funcionais
```naja
list numbers = [1, 2, 3, 4, 5];

// Map - transforma elementos
fun doubleFunction(item, index, array) {
    return item * 2;
}
list doubled = numbers.map(doubleFunction);

// Filter - filtra elementos
fun evenFunction(item, index, array) {
    return item % 2 == 0;
}
list evens = numbers.filter(evenFunction);

// Reduce - reduz a um valor
fun sumFunction(acc, item, index, array) {
    return acc + item;
}
int sum = numbers.reduce(sumFunction, 0);

// Outros métodos
numbers.forEach(callback);
any found = numbers.find(callback);
bool hasAny = numbers.some(callback);
bool hasAll = numbers.every(callback);
bool contains = numbers.includes(value);
int index = numbers.indexOf(value);
string joined = numbers.join(", ");
list reversed = numbers.reverse();
list sliced = numbers.slice(1, 3);
```

### 8. File System
```naja
// Operações com arquivos
string content = fs.readFile("path/file.txt");
bool success = fs.writeFile("path/file.txt", "content");
bool appended = fs.appendFile("path/file.txt", "more content");
bool deleted = fs.deleteFile("path/file.txt");

// Verificações
bool exists = fs.exists("path/file.txt");
bool isFile = fs.isFile("path/file.txt");
bool isDir = fs.isDir("path/");
int size = fs.getSize("path/file.txt");

// Diretórios
bool created = fs.mkdir("path/new-dir");
list files = fs.listDir("path/");
```

### 9. WebSocket
```naja
// Criar WebSocket
any ws = WebSocket("ws://localhost:8080");

// Event handlers
fun onOpen() {
    println("Connected!");
}

fun onMessage(data) {
    println("Received: " + data);
}

fun onClose() {
    println("Disconnected!");
}

fun onError(error) {
    println("Error: " + error);
}

// Registrar eventos
ws.on("open", onOpen);
ws.on("message", onMessage);
ws.on("close", onClose);
ws.on("error", onError);

// Operações
ws.connect();
ws.send("Hello Server!");
ws.close();
```

### 10. Promise & Async/Await
```naja
// Criar Promise
fun executor(resolve, reject) {
    // Async operation
    sleep(1000);
    resolve("Success!");
    // ou reject("Error!");
}

any promise = Promise(executor);

// Handlers
fun onSuccess(value) {
    println("Success: " + value);
}

fun onError(error) {
    println("Error: " + error);
}

// Usar Promise
promise.then(onSuccess, onError);
promise.catch(onError);

// Métodos estáticos
any resolved = PromiseResolve("value");
any rejected = PromiseReject("error");
any all = PromiseAll([promise1, promise2]);

// Sleep para operações assíncronas
sleep(1000);  // 1 segundo
```

### 11. JSON & Fetch (Já implementados)
```naja
// JSON
any stringify_func = JSON.get("stringify");
string jsonStr = stringify_func(object);

any parse_func = JSON.get("parse");
any parsed = parse_func(jsonStr);

// Fetch
any response = fetch("https://api.example.com/data");
println("Status: " + response.status);
println("OK: " + response.ok);
string text = response.text();
any json = response.json();

// HTTP methods
any getResponse = get("https://api.example.com/data");
any postResponse = post("https://api.example.com/data", data);
```

### 12. Sistema de Eventos (Já implementado)
```naja
// Eventos globais
fun handler(data) {
    println("Event: " + data);
}

addEventListener("custom-event", handler);
dispatchEvent("custom-event", "Hello!");
removeEventListener("custom-event", handler);
once("one-time-event", handler);

// EventEmitter personalizado
any emitter = createEventEmitter();
emitter.on("event", handler);
emitter.emit("event", "data");
emitter.off("event", handler);
```

## 🎯 Sintaxe Importante
- Use `fun` em vez de `function`
- Todas as funcionalidades são **nativas** (sem imports necessários)
- Tipos: `string`, `int`, `float`, `bool`, `any`, `list`, `dict`
- Sintaxe em inglês para todas as funcionalidades modernas

## 🚀 Exemplo Completo
```naja
println("=== NajaScript Modern Demo ===");

// Console e DateTime
console.log("Starting application...");
any now = DateTime.now();
console.info("Current time: " + now.format("%H:%M:%S"));

// Crypto
string hash = crypto.sha256("my-secret-data");
console.log("Data hash: " + hash);

// Storage
localStorage.setItem("user", "developer");
console.log("Stored user: " + localStorage.getItem("user"));

// Arrays funcionais
list data = [1, 2, 3, 4, 5];
list doubled = data.map(fun(x) { return x * 2; });
console.log("Doubled: " + doubled.join(", "));

// File system
fs.writeFile("demo.txt", "Hello NajaScript!");
string content = fs.readFile("demo.txt");
console.log("File content: " + content);
fs.deleteFile("demo.txt");

// Events
addEventListener("demo", fun(msg) {
    console.log("Event received: " + msg);
});
dispatchEvent("demo", "Application ready!");

console.log("=== Demo complete! ===");
```

## 📋 Status das Funcionalidades
- ✅ Console Avançado - Funcionando
- ✅ Crypto & Hash - Funcionando  
- ✅ DateTime - Funcionando
- ✅ Regex - Funcionando
- ✅ Timers - Funcionando
- ✅ Storage - Funcionando
- ✅ Functional Arrays - Funcionando
- ✅ File System - Funcionando
- ✅ WebSocket - Funcionando
- ✅ Promise & Async/Await - Funcionando
- ✅ JSON & Fetch - Funcionando
- ✅ Event System - Funcionando

## 🎉 Conclusão
NajaScript agora possui todas as funcionalidades modernas necessárias para desenvolvimento atual, tornando-se uma linguagem completa e robusta similar ao JavaScript/TypeScript moderno! 