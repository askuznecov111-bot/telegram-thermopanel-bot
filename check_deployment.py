#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from abacusai import ApiClient

load_dotenv()

API_KEY = os.getenv('ABACUS_API_KEY', 's2_a337cfbf99eb400fa20558122b95d310')
DEPLOYMENT_ID = '7c388e8dc'

client = ApiClient(API_KEY)
deployment = client.describe_deployment(DEPLOYMENT_ID)
print(f"Deployment Status: {deployment.status}")

if deployment.status != 'ACTIVE':
    print(f"⚠️ Deployment не активен! Запускаю...")
    client.start_deployment(DEPLOYMENT_ID)
    print("✅ Deployment запущен, ожидайте активации (30-60 сек)")
else:
    print("✅ Deployment уже активен!")
