#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
from urllib.parse import urljoin

class HTTPResponse:
    """Representa uma resposta HTTP formatada para NajaScript (similar à Response do JavaScript)"""
    def __init__(self, response):
        # Propriedades públicas
        self.status = response.status_code
        self.ok = 200 <= response.status_code < 300
        self.headers = dict(response.headers)
        self.statusText = response.reason
        self.url = response.url
        
        # Propriedades privadas
        self._raw = response
        self._text = response.text
        self._json_data = None
        self._json_parsed = False
    
    def __str__(self):
        return f"Response(status={self.status}, ok={self.ok})"
    
    def text(self):
        """Retorna o corpo da resposta como texto (equivalente ao .text() do JavaScript)"""
        return self._text
    
    def json(self):
        """Retorna o corpo da resposta como JSON (equivalente ao .json() do JavaScript)"""
        if not self._json_parsed:
            try:
                self._json_data = json.loads(self._text)
                self._json_parsed = True
            except Exception as e:
                raise RuntimeError(f"A resposta não é um JSON válido: {str(e)}")
        return self._json_data
    
    def blob(self):
        """Similar ao .blob() do JavaScript - retorna os dados brutos"""
        return self._raw.content

class Dict:
    """Implementação de dicionário para NajaScript"""
    def __init__(self, initial_data=None):
        self._data = {} if initial_data is None else dict(initial_data)
    
    def get(self, key):
        """Obtém um valor pelo nome da chave"""
        if key in self._data:
            return self._data[key]
        return None
    
    def set(self, key, value):
        """Define um valor para uma chave"""
        self._data[key] = value
        return value
    
    def has(self, key):
        """Verifica se uma chave existe"""
        return key in self._data
    
    def keys(self):
        """Retorna uma lista de chaves"""
        return list(self._data.keys())
    
    def values(self):
        """Retorna uma lista de valores"""
        return list(self._data.values())
    
    def items(self):
        """Retorna uma lista de tuplas (chave, valor)"""
        return list(self._data.items())
    
    def __repr__(self):
        items = []
        for k, v in self._data.items():
            items.append(f"{k}: {repr(v)}")
        return "{" + ", ".join(items) + "}"

def create_http_module():
    """Cria e configura o módulo HTTP para NajaScript"""
    module = {}
    
    # Configuração global
    default_headers = {
        "User-Agent": "NajaScript/1.0",
        "Content-Type": "application/json"
    }
    
    # Implementação do fetch similar ao JavaScript
    def fetch(url, options=None):
        """
        Realiza uma requisição HTTP no estilo Fetch API
        
        Parâmetros:
        url (string): A URL para a requisição
        options (Dict, opcional): Opções da requisição
        
        Opções disponíveis:
        - method: 'GET', 'POST', 'PUT', 'DELETE', 'PATCH'
        - headers: dicionário com cabeçalhos
        - body: corpo da requisição (String ou Dict)
        - params: parâmetros de URL (Dict)
        
        Retorna:
        Response: Um objeto Response com os métodos .text(), .json()
        """
        if options is None:
            options = {}
        
        # Extrai as opções
        method = "GET"
        if options and hasattr(options, "get"):
            method = options.get("method") or "GET"
            if isinstance(method, str):
                method = method.upper()
        
        # Prepara headers
        headers = dict(default_headers)
        if options and hasattr(options, "get"):
            options_headers = options.get("headers")
            if options_headers and hasattr(options_headers, "items"):
                for k, v in options_headers.items():
                    headers[k] = v
        
        # Extrai parâmetros e corpo
        params = None
        body = None
        
        if options and hasattr(options, "get"):
            params = options.get("params")
            body = options.get("body")
        
        try:
            if method == "GET":
                response = requests.get(url, params=params, headers=headers)
            elif method == "POST":
                # Se body for um objeto Dict ou similar, tenta converter para JSON
                if body and hasattr(body, "items"):
                    response = requests.post(url, json=dict(body.items()) if hasattr(body, "items") else body, headers=headers)
                else:
                    response = requests.post(url, data=body, headers=headers)
            elif method == "PUT":
                if body and hasattr(body, "items"):
                    response = requests.put(url, json=dict(body.items()) if hasattr(body, "items") else body, headers=headers)
                else:
                    response = requests.put(url, data=body, headers=headers)
            elif method == "DELETE":
                response = requests.delete(url, headers=headers)
            elif method == "PATCH":
                if body and hasattr(body, "items"):
                    response = requests.patch(url, json=dict(body.items()) if hasattr(body, "items") else body, headers=headers)
                else:
                    response = requests.patch(url, data=body, headers=headers)
            else:
                raise RuntimeError(f"Método HTTP não suportado: {method}")
                
            return HTTPResponse(response)
        except Exception as e:
            raise RuntimeError(f"Erro na requisição HTTP: {str(e)}")
    
    # Atalho para GET
    def get(url, params=None, headers=None):
        """
        Realiza uma requisição HTTP GET
        
        Parâmetros:
        url (string): A URL para a requisição
        params (Dict, opcional): Parâmetros de consulta
        headers (Dict, opcional): Cabeçalhos HTTP adicionais
        
        Retorna:
        Response: Um objeto Response
        """
        options = {}
        options["method"] = "GET"
        if params:
            options["params"] = params
        if headers:
            options["headers"] = headers
        
        return fetch(url, options)
    
    # Atalho para POST
    def post(url, data=None, json_data=None, headers=None):
        """
        Realiza uma requisição HTTP POST
        
        Parâmetros:
        url (string): A URL para a requisição
        data (string, opcional): Dados a serem enviados como formulário
        json_data (Dict, opcional): Dados a serem enviados como JSON
        headers (Dict, opcional): Cabeçalhos HTTP adicionais
        
        Retorna:
        Response: Um objeto Response
        """
        options = {}
        options["method"] = "POST"
        
        if json_data:
            options["body"] = json_data
        elif data:
            options["body"] = data
            
        if headers:
            options["headers"] = headers
            
        return fetch(url, options)
    
    # Atalho para PUT
    def put(url, data=None, json_data=None, headers=None):
        """
        Realiza uma requisição HTTP PUT
        
        Parâmetros:
        url (string): A URL para a requisição
        data (string, opcional): Dados a serem enviados como formulário
        json_data (Dict, opcional): Dados a serem enviados como JSON
        headers (Dict, opcional): Cabeçalhos HTTP adicionais
        
        Retorna:
        Response: Um objeto Response
        """
        options = {}
        options["method"] = "PUT"
        
        if json_data:
            options["body"] = json_data
        elif data:
            options["body"] = data
            
        if headers:
            options["headers"] = headers
            
        return fetch(url, options)
    
    # Atalho para DELETE
    def delete(url, headers=None):
        """
        Realiza uma requisição HTTP DELETE
        
        Parâmetros:
        url (string): A URL para a requisição
        headers (Dict, opcional): Cabeçalhos HTTP adicionais
        
        Retorna:
        Response: Um objeto Response
        """
        options = {}
        options["method"] = "DELETE"
        
        if headers:
            options["headers"] = headers
            
        return fetch(url, options)
    
    # Atalho para PATCH
    def patch(url, data=None, json_data=None, headers=None):
        """
        Realiza uma requisição HTTP PATCH
        
        Parâmetros:
        url (string): A URL para a requisição
        data (string, opcional): Dados a serem enviados como formulário
        json_data (Dict, opcional): Dados a serem enviados como JSON
        headers (Dict, opcional): Cabeçalhos HTTP adicionais
        
        Retorna:
        Response: Um objeto Response
        """
        options = {}
        options["method"] = "PATCH"
        
        if json_data:
            options["body"] = json_data
        elif data:
            options["body"] = data
            
        if headers:
            options["headers"] = headers
            
        return fetch(url, options)
    
    # Função para construir URL
    def buildUrl(base_url, path):
        """
        Constrói uma URL completa a partir de uma URL base e um caminho
        
        Parâmetros:
        base_url (string): A URL base
        path (string): O caminho a ser anexado
        
        Retorna:
        string: A URL completa
        """
        return urljoin(base_url, path)
    
    # Funções para manipular JSON
    def jsonStringify(obj):
        """
        Converte um objeto para string JSON
        
        Parâmetros:
        obj (any): O objeto a ser convertido
        
        Retorna:
        string: A representação JSON do objeto
        """
        try:
            # Se for um Dict do NajaScript, converte para dict Python
            if hasattr(obj, "_data"):
                obj = obj._data
            return json.dumps(obj)
        except Exception as e:
            raise RuntimeError(f"Erro ao converter para JSON: {str(e)}")
    
    def jsonParse(json_str):
        """
        Converte uma string JSON para objeto
        
        Parâmetros:
        json_str (string): A string JSON a ser analisada
        
        Retorna:
        Dict: O objeto JSON convertido para Dict
        """
        try:
            parsed = json.loads(json_str)
            # Se for um dicionário, converte para Dict do NajaScript
            if isinstance(parsed, dict):
                return Dict(parsed)
            return parsed
        except Exception as e:
            raise RuntimeError(f"Erro ao analisar JSON: {str(e)}")
    
    # Criador de Dict
    def createDict(initial_data=None):
        """
        Cria um novo objeto Dict
        
        Parâmetros:
        initial_data (Dict, opcional): Dados iniciais
        
        Retorna:
        Dict: Um novo objeto Dict
        """
        return Dict(initial_data)
    
    # Exporta as funções
    module["fetch"] = fetch
    module["get"] = get
    module["post"] = post
    module["put"] = put
    module["delete"] = delete
    module["patch"] = patch
    module["buildUrl"] = buildUrl
    module["jsonStringify"] = jsonStringify
    module["jsonParse"] = jsonParse
    module["createDict"] = createDict
    
    # Marca todas as funções como exportadas
    for name, func in module.items():
        if hasattr(func, '__call__'):
            func.exported = True
    
    return module 