import pytest
import requests

BASE_URL = "http://localhost:5000"

def test_cadastro_aluno():
    payload = {"nome": "Teste Aluno", "ra": "123456"}
    response = requests.post(f"{BASE_URL}/alunos", json=payload)
    assert response.status_code == 201
    assert response.json()["message"] == "Aluno cadastrado com sucesso"

