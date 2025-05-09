// NajaScript Runtime para navegador
// Este arquivo integra o interpretador NajaScript compilado para WebAssembly

const NajaRuntime = (() => {
    // Estado interno
    let _interpreter = null;
    let _initialized = false;
    let _domModule = null;
    
    // Exportações para o NajaScript
    const exports = {};
    
    // Inicializa o módulo DOM para NajaScript
    function initDOMModule() {
        _domModule = {
            document: {
                getElementById: (id) => document.getElementById(id),
                createElement: (tag) => document.createElement(tag),
                querySelector: (selector) => document.querySelector(selector),
                querySelectorAll: (selector) => Array.from(document.querySelectorAll(selector))
            },
            window: {
                addEventListener: (event, callback) => {
                    window.addEventListener(event, (...args) => {
                        // Converte a callback NajaScript para JS
                        _interpreter.callFunction(callback, args);
                    });
                },
                setInterval: (callback, ms) => {
                    return window.setInterval(() => {
                        _interpreter.callFunction(callback, []);
                    }, ms);
                },
                setTimeout: (callback, ms) => {
                    return window.setTimeout(() => {
                        _interpreter.callFunction(callback, []);
                    }, ms);
                },
                console: {
                    log: (...args) => console.log(...args),
                    error: (...args) => console.error(...args)
                }
            },
            fetch: async (url, options) => {
                try {
                    const response = await fetch(url, options);
                    return {
                        status: response.status,
                        ok: response.ok,
                        headers: Object.fromEntries(response.headers.entries()),
                        text: () => response.text(),
                        json: () => response.json()
                    };
                } catch (error) {
                    console.error("Erro na requisição fetch:", error);
                    throw error;
                }
            }
        };
        
        return _domModule;
    }
    
    // Interface pública
    return {
        // Inicializa o runtime NajaScript
        init: async function() {
            console.log("Inicializando NajaScript Runtime...");
            
            try {
                // Carrega o módulo WebAssembly do interpretador NajaScript
                const najaModule = await import('./naja_wasm.js');
                
                // Inicializa o interpretador
                await najaModule.init();
                _interpreter = najaModule.createInterpreter();
                
                // Registra módulos nativos
                _interpreter.registerModule("dom", initDOMModule());
                
                _initialized = true;
                console.log("NajaScript Runtime inicializado com sucesso!");
                
                return true;
            } catch (error) {
                console.error("Falha ao inicializar NajaScript Runtime:", error);
                return false;
            }
        },
        
        // Carrega e executa um script NajaScript
        loadScript: async function(scriptPath) {
            if (!_initialized) {
                throw new Error("NajaScript Runtime não inicializado. Chame init() primeiro.");
            }
            
            try {
                // Carrega o código fonte do script
                const response = await fetch(scriptPath);
                if (!response.ok) {
                    throw new Error(`Falha ao carregar script ${scriptPath}: ${response.status} ${response.statusText}`);
                }
                
                const sourceCode = await response.text();
                
                // Executa o código NajaScript
                const result = _interpreter.execute(sourceCode, scriptPath);
                
                // Exporta funções globais definidas no script
                if (result.exports) {
                    for (const [name, func] of Object.entries(result.exports)) {
                        exports[name] = (...args) => _interpreter.callFunction(func, args);
                        window[name] = exports[name]; // Para acesso global
                    }
                }
                
                return result;
            } catch (error) {
                console.error(`Erro ao executar script ${scriptPath}:`, error);
                throw error;
            }
        },
        
        // Executa código NajaScript diretamente
        execute: function(code) {
            if (!_initialized) {
                throw new Error("NajaScript Runtime não inicializado. Chame init() primeiro.");
            }
            
            return _interpreter.execute(code, "inline");
        },
        
        // Retorna as exportações de scripts carregados
        getExports: function() {
            return exports;
        }
    };
})();

// Para uso como módulo ES
export default NajaRuntime; 