#!/usr/bin/env python3
"""
Sistema de testes simplificado para Windows
"""

import subprocess
import sys
import os
from pathlib import Path

def run_safe_tests():
    """Executa apenas testes que NÃO consomem tokens da API"""
    print("🚀 Executando testes seguros para CI/CD")
    print("=" * 50)
    
    # Testa cada função individualmente para evitar problemas de sintaxe
    commands = [
        "pytest tests/testGenertion.py::test_root -v",
        "pytest tests/testGenertion.py::test_health_check -v", 
        "pytest tests/testGenertion.py::test_invalid_endpoints -v",
        "pytest tests/testGenertion.py::test_malformed_requests -v",
        "pytest tests/test_integration.py::TestPerformance -v"
    ]
    
    passed = 0
    failed = 0
    
    for cmd in commands:
        print(f"\n🔄 {cmd}")
        print("-" * 30)
        
        try:
            result = subprocess.run(cmd, shell=True, cwd=Path(__file__).parent.parent)
            if result.returncode == 0:
                print("✅ PASSOU")
                passed += 1
            else:
                print("❌ FALHOU") 
                failed += 1
        except Exception as e:
            print(f"❌ ERRO: {e}")
            failed += 1
    
    print(f"\n📊 RESULTADO FINAL:")
    print(f"✅ Passou: {passed}")
    print(f"❌ Falhou: {failed}")
    print(f"\n💡 Estes testes NÃO consumiram tokens da API!")
    
    return failed == 0

def run_all_tests():
    """Executa TODOS os testes - VAI CONSUMIR TOKENS"""
    print("⚠️  ATENÇÃO: Executando testes completos")
    
    confirm = input("Isso VAI CONSUMIR seus tokens do Gemini. Continuar? (y/N): ")
    if confirm.lower() != 'y':
        print("❌ Cancelado")
        return False
    
    print("🔥 Executando todos os testes...")
    result = subprocess.run("pytest -v", shell=True, cwd=Path(__file__).parent.parent)
    return result.returncode == 0

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "full":
        success = run_all_tests()
    else:
        success = run_safe_tests()
    
    sys.exit(0 if success else 1)