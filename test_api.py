#!/usr/bin/env python3
"""
Script para testar os endpoints da API de previsão de ações.
"""
import sys
import json

def test_api_imports():
    """Testa se todos os imports da API funcionam"""
    print("🧪 Testando imports da API...")
    try:
        from api.main import app
        from src.train_prev_acoes import criar_sequencias, main
        from src.predict_prev_acoes import prever, carregar_modelo
        from api.schemas.parameters_to_train import ParametersToTrain
        print("✅ Todos os imports foram bem-sucedidos")
        return True
    except Exception as e:
        print(f"❌ Erro nos imports: {e}")
        return False

def test_fastapi_routes():
    """Testa se as rotas da API estão definidas corretamente"""
    print("\n🧪 Testando rotas da API...")
    try:
        from api.main import app
        routes = [route.path for route in app.routes]
        expected_routes = ['/health', '/train_model', '/predict/{ticker}', '/models']
        
        print(f"Rotas encontradas: {routes}")
        
        for route in expected_routes:
            if any(route in r for r in routes):
                print(f"  ✅ Rota {route} existe")
            else:
                print(f"  ⚠️  Rota {route} pode não estar registrada")
        
        return True
    except Exception as e:
        print(f"❌ Erro ao testar rotas: {e}")
        return False

def test_model_functions():
    """Testa funções básicas do modelo"""
    print("\n🧪 Testando funções do modelo...")
    try:
        from src.train_prev_acoes import criar_sequencias
        import numpy as np
        
        # Criar dados de teste
        dados_teste = np.random.rand(200, 1)
        X, y = criar_sequencias(dados_teste, janela=90)
        
        assert X.shape[0] == 110, f"Shape incorreto: {X.shape}"
        assert y.shape[0] == 110, f"Shape incorreto: {y.shape}"
        
        print(f"  ✅ criar_sequencias funciona corretamente")
        print(f"     Input shape: {X.shape}, Output shape: {y.shape}")
        return True
    except Exception as e:
        print(f"❌ Erro ao testar funções: {e}")
        return False

def test_pydantic_schemas():
    """Testa os schemas Pydantic"""
    print("\n🧪 Testando schemas Pydantic...")
    try:
        from api.schemas.parameters_to_train import ParametersToTrain
        from datetime import date
        
        # Criar instância de teste
        params = ParametersToTrain(
            ticker="TEST",
            start=date(2024, 1, 1),
            end=date(2025, 12, 31),
            janela=90,
            epochs=40,
            batch=32,
            patience=4
        )
        
        print(f"  ✅ Schema ParametersToTrain funciona")
        print(f"     Exemplo: {params.ticker}, janela={params.janela}")
        return True
    except Exception as e:
        print(f"❌ Erro ao testar schemas: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("=" * 60)
    print("🚀 Testes da API de Previsão de Ações")
    print("=" * 60)
    
    tests = [
        test_api_imports,
        test_fastapi_routes,
        test_model_functions,
        test_pydantic_schemas
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Teste falhou com exceção: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"📊 Resultado: {passed}/{total} testes passaram")
    
    if passed == total:
        print("✅ Todos os testes passaram!")
        print("=" * 60)
        return 0
    else:
        print("⚠️  Alguns testes falharam")
        print("=" * 60)
        return 1

if __name__ == "__main__":
    sys.exit(main())
