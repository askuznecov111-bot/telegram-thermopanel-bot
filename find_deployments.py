#!/usr/bin/env python3
"""
Поиск правильного deployment
"""
import os
from dotenv import load_dotenv
from abacusai import ApiClient

load_dotenv()

API_KEY = os.getenv('ABACUS_API_KEY', 's2_a337cfbf99eb400fa20558122b95d310')

print("="*60)
print("Поиск доступных deployments и проектов")
print("="*60)

try:
    client = ApiClient(API_KEY)
    print("✅ Клиент инициализирован")
    
    # Попробуем список проектов
    print("\n📋 Список проектов:")
    try:
        projects = client.list_projects()
        if projects:
            for project in projects[:10]:
                print(f"\n  Project ID: {project.project_id}")
                print(f"  Name: {project.name}")
                print(f"  Use Case: {project.use_case}")
                
                # Попробуем получить deployments для этого проекта
                try:
                    deployments = client.list_deployments(project_id=project.project_id)
                    if deployments:
                        print(f"  Deployments:")
                        for dep in deployments:
                            print(f"    - Deployment ID: {dep.deployment_id}")
                            print(f"      Name: {dep.name}")
                            print(f"      Status: {dep.status}")
                            
                            # Попробуем получить deployment token
                            try:
                                tokens = client.list_deployment_tokens(project_id=project.project_id)
                                if tokens:
                                    print(f"      Deployment Tokens:")
                                    for token in tokens:
                                        print(f"        - Token: {token.deployment_token}")
                            except Exception as e:
                                print(f"      ❌ Не удалось получить tokens: {str(e)[:100]}")
                except Exception as e:
                    print(f"  ❌ Не удалось получить deployments: {str(e)[:100]}")
        else:
            print("  Нет проектов")
    except Exception as e:
        print(f"❌ Ошибка при получении проектов: {str(e)[:500]}")
    
    # Попробуем список всех deployments
    print("\n\n📋 Прямой список всех deployments:")
    try:
        all_deployments = client.list_deployments()
        if all_deployments:
            for dep in all_deployments[:5]:
                print(f"\n  Deployment ID: {dep.deployment_id}")
                print(f"  Name: {dep.name}")
                print(f"  Status: {dep.status}")
        else:
            print("  Нет deployments")
    except Exception as e:
        print(f"❌ Ошибка: {str(e)[:500]}")

except Exception as e:
    print(f"❌ Критическая ошибка: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("Поиск завершен")
print("="*60)
