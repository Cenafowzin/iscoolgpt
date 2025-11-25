#!/usr/bin/env python3
"""
Script de testes para GitHub Actions
Executa apenas testes que não precisam de API key real
"""

import subprocess
import sys
import os

def run_tests():
    """Executa testes seguros para CI/CD"""
    print("🚀 Executando testes seguros no GitHub Actions")
    print("=" * 50)
    
    # Configurar ambiente para pular validação de API
    os.environ['CI'] = 'true'
    os.environ['SKIP_API_VALIDATION'] = 'true'
    
    # Lista de testes individuais que não consomem API
    test_commands = [
        "pytest tests/test_genertion.py::test_root -v",
        "pytest tests/test_genertion.py::test_health_check -v", 
        "pytest tests/test_genertion.py::test_invalid_endpoints -v",
        "pytest tests/test_genertion.py::test_malformed_requests -v",
        "pytest tests/test_integration.py::TestPerformance::test_response_time_basic_endpoints -v",
        "pytest tests/test_integration.py::TestPerformance::test_health_check_performance -v"
    ]
    
    failed = 0
    passed = 0
    
    for cmd in test_commands:
        print(f"\n🔄 {cmd}")
        print("-" * 30)
        
        try:
            result = subprocess.run(
                cmd, 
                shell=True, 
                check=False,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print("✅ PASSOU")
                passed += 1
            else:
                print("❌ FALHOU")
                print("STDOUT:", result.stdout)
                print("STDERR:", result.stderr)
                failed += 1
                
        except Exception as e:
            print(f"❌ ERRO: {e}")
            failed += 1
    
    print(f"\n📊 RESULTADO:")
    print(f"✅ Passou: {passed}")
    print(f"❌ Falhou: {failed}")
    
    # Test application import
    print(f"\n🔄 Testando importação da aplicação...")
    try:
        from app.main import app
        print("✅ Aplicação importada com sucesso")
        passed += 1
    except Exception as e:
        print(f"❌ Erro ao importar aplicação: {e}")
        failed += 1
    
    return failed == 0

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)