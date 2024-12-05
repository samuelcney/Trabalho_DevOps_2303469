# Projeto DevOps - Ambiente Monitorado com Pipeline CI/CD

Este projeto visa a criação de um ambiente DevOps completo, utilizando uma aplicação web simples, implementada em Flask, que conta com um banco de dados MariaDB e funcionalidades básicas. Para automatizar e monitorar o processo de desenvolvimento e deploy, configuramos uma pipeline CI/CD no Jenkins, e o ambiente é monitorado em tempo real com Prometheus e Grafana.

## Objetivo do Projeto
O objetivo deste projeto é desenvolver um fluxo completo de CI/CD, que possibilite a automação de testes, build e deploy, bem como a monitoração de métricas da aplicação e do banco de dados, visando garantir a confiabilidade e a observabilidade do ambiente.

## Arquitetura e Ferramentas Utilizadas

1. **Aplicação Web (Flask)**:
   - Uma aplicação web em Python com Flask, que possui uma funcionalidade de cadastro de alunos. 
   - Os dados são armazenados em um banco de dados MariaDB.
   - Implementação de testes unitários para validar o cadastro de aluno.

2. **Pipeline CI/CD (Jenkins)**:
   - Configuração de um **Jenkinsfile** para automatizar as etapas de download do código, execução dos testes, build da aplicação e deploy no ambiente.
   - A pipeline é estruturada em etapas de **Download do Código**, **Teste**, **Build** e **Deploy**, garantindo a integração e entrega contínuas.

3. **Monitoramento (Prometheus e Grafana)**:
   - **Prometheus**: Ferramenta de monitoramento utilizada para coletar métricas da aplicação Flask e do banco de dados MariaDB.
   - **Grafana**: Ferramenta de visualização das métricas. Um dashboard é configurado para exibir métricas como o número de acessos à aplicação e consultas ao banco de dados.
   - Configurações de datasources e dashboards no Grafana são feitas via arquivos de configuração, permitindo o provisionamento automatizado.

## **Estrutura do Projeto**

- **Repositório Git**:
  - O repositório é versionado com todos os arquivos de configuração necessários, incluindo Dockerfiles, `docker-compose.yml`, Jenkinsfile, e configurações do Prometheus e Grafana.
  - Commits frequentes documentam o progresso do projeto.

- **Diretórios Principais**:
  - `app/`: Código-fonte da aplicação Flask e arquivo com testes unitários para validar a funcionalidade de cadastro de aluno..
  - `prometheus/`: Configurações para coleta de métricas no Prometheus.
  - `grafana/`: Configurações de datasources e dashboards para visualização das métricas no Grafana.

## **Pipeline CI/CD**

A pipeline do Jenkins é configurada para realizar as seguintes etapas:

1. **Download do Código**: Jenkins clona o repositório do projeto.
2. **Execução de Testes**: O teste unitário para o cadastro de aluno é executado para verificar a integridade da aplicação.
3. **Build e Deploy**: O Jenkins gera a imagem Docker da aplicação e realiza o deploy completo, garantindo que todos os serviços (aplicação Flask, MariaDB, Prometheus, Grafana) estejam funcionando corretamente.

## **Monitoramento e Dashboard**

- **Prometheus**:
  - Configurado para coletar métricas da aplicação Flask e do banco de dados MariaDB.
  - Monitora informações relevantes, como o número de requisições e as consultas realizadas no banco de dados.

- **Grafana**:
  - O dashboard exibe visualizações das métricas, facilitando o acompanhamento de dados em tempo real, como o número de acessos à aplicação e consultas ao banco de dados.
  - Os dashboards são configurados via arquivos de configuração, para facilitar a reprodução do ambiente.
 
### **Estrutura de pastas do projeto**

```
├── Jenkinsfile                          # Define a pipeline de CI/CD do Jenkins
├── docker-compose.yml
├── grafana/
│   ├── provisioning/
│   │   ├── datasource.yml          # Configuração de fonte de dados para o Grafana
│   │   ├── dashboard.yml           # Configuração para provisionamento automático de dashboards
│   └── dashboards/
│       └── mariadb_dashboard.json  # JSON exportado da dashboard do Grafana para MariaDB
├── prometheus/
│   └── prometheus.yml              # Arquivo de configuração do Prometheus
├── mariadb/
│   └── Dockerfile_mariadb          # Dockerfile do MariaDB
├── flask/
│   ├── app.py                      # Código principal da aplicação Flask
│   ├── Dockerfile_flask            # Dockerfile do Flask
│   ├── requirements.txt            # Dependências da aplicação Flask
│   ├── test_app.py             # Arquivo de testes unitários da aplicação Flask
└── exporter/
    └── mysqld_exporter.env         # Arquivo de configuração/env do MySQL Exporter
```
## **Configurações dos Serviços**

### **1. Banco de Dados: MariaDB**
Criar Pasta: `mariadb`

Arquivo: `Dockerfile_mariadb`  
```dockerfile
# Dockerfile para MariaDB
# Salve este arquivo como Dockerfile_mariadb na raiz do projeto

# Dockerfile (MariaDB)
FROM mariadb:10.5

# Defina as variáveis de ambiente para o banco de dados
ENV MYSQL_ROOT_PASSWORD=root_password
ENV MYSQL_DATABASE=school_db
ENV MYSQL_USER=flask_user
ENV MYSQL_PASSWORD=flask_password

EXPOSE 3306
```

---

### **2. Backend: Aplicação Flask**
Pasta: `flask`

Arquivo: `app.py`  
```python
# Código principal do Flask (app.py)
import time
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_appbuilder import AppBuilder, SQLA
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView
from sqlalchemy.exc import OperationalError
from prometheus_flask_exporter import PrometheusMetrics
import logging

app = Flask(__name__)

metrics = PrometheusMetrics(app)
# Configuração da chave secreta para sessões
app.config['SECRET_KEY'] = 'minha_chave_secreta_super_secreta'  # Substitua por uma chave segura

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root_password@mariadb/school_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar o banco de dados e o AppBuilder
db = SQLAlchemy(app)
appbuilder = AppBuilder(app, db.session)

# Configuração do log
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Modelo de Aluno - Definição da tabela 'Aluno' no banco de dados
class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    sobrenome = db.Column(db.String(50), nullable=False)
    turma = db.Column(db.String(50), nullable=False)
    disciplinas = db.Column(db.String(200), nullable=False)
    ra = db.Column(db.String(200), nullable=False)


# Tentar conectar até o MariaDB estar pronto
attempts = 5
for i in range(attempts):
    try:
        with app.app_context():
            db.create_all()  # Inicializa o banco de dados
            # Criar um usuário administrador padrão
            if not appbuilder.sm.find_user(username='admin'):
                appbuilder.sm.add_user(
                    username='admin',
                    first_name='Admin',
                    last_name='User',
                    email='admin@admin.com',
                    role=appbuilder.sm.find_role(appbuilder.sm.auth_role_admin),
                    password='admin'
                )
        logger.info("Banco de dados inicializado com sucesso.")
        break
    except OperationalError:
        if i < attempts - 1:
            logger.warning("Tentativa de conexão com o banco de dados falhou. Tentando novamente em 5 segundos...")
            time.sleep(5)  # Aguarda 5 segundos antes de tentar novamente
        else:
            logger.error("Não foi possível conectar ao banco de dados após várias tentativas.")
            raise

# Visão do modelo Aluno para o painel administrativo
class AlunoModelView(ModelView):
    datamodel = SQLAInterface(Aluno)
    list_columns = ['id', 'nome', 'sobrenome', 'turma', 'disciplinas', 'ra']

# Adicionar a visão do modelo ao AppBuilder
appbuilder.add_view(
    AlunoModelView,
    "Lista de Alunos",
    icon="fa-folder-open-o",
    category="Alunos",
)

# Rota para listar todos os alunos - Método GET
@app.route('/alunos', methods=['GET'])
def listar_alunos():
    alunos = Aluno.query.all()
    output = [{'id': aluno.id, 'nome': aluno.nome, 'sobrenome': aluno.sobrenome, 'turma': aluno.turma, 'disciplinas': aluno.disciplinas, 'ra': aluno.ra} for aluno in alunos]
    return jsonify(output)

# Rota para adicionar um aluno - Método POST
@app.route('/alunos', methods=['POST'])
def adicionar_aluno():
    data = request.get_json()
    novo_aluno = Aluno(nome=data['nome'], sobrenome=data['sobrenome'], turma=data['turma'], disciplinas=data['disciplinas'], ra=data['ra'])
    db.session.add(novo_aluno)
    db.session.commit()
    logger.info(f"Aluno {data['nome']} {data['sobrenome']} adicionado com sucesso!")
    return jsonify({'message': 'Aluno adicionado com sucesso!'}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```
Pasta: `flask`

Arquivo: `requirements.txt`  
```plaintext
Flask==1.1.4  # Versão compatível com Flask-AppBuilder
Flask-SQLAlchemy==2.4.4  # Extensão do Flask para integração com SQLAlchemy
PyMySQL==0.9.3  # Biblioteca para conexão do Python com o banco de dados MariaDB
Flask-AppBuilder==3.3.0  # Versão compatível com Flask 1.x
Werkzeug==1.0.1  # Versão compatível do Werkzeug para evitar erros de importação
MarkupSafe==2.0.1  # Versão compatível com Jinja2 e Flask
WTForms==2.3.3  # Versão compatível com Flask-AppBuilder que contém o módulo 'compat'
prometheus-flask-exporter==0.18.3
pytest==6.2.5
pytest-flask==1.2.0
Flask-Testing==0.8.0
```
Pasta: `flask`

Arquivo: `Dockerfile_flask`  
```dockerfile
# Dockerfile (Flask AppBuilder)
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o arquivo app.py
COPY app.py /app/

# Copiar também o arquivo de teste test_app.py
COPY test_app.py /app/

CMD ["flask", "run", "--host=0.0.0.0"]
```
Pasta: `flask`

Arquivo: `test_app.py`

````
import pytest
from flask import Flask
from flask.testing import FlaskClient

# Importar a aplicação Flask
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_listar_alunos(client: FlaskClient):
    """Testa a rota GET /alunos"""
    response = client.get('/alunos')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_adicionar_aluno(client: FlaskClient):
    """Testa a rota POST /alunos"""
    new_aluno = {
        "nome": "Relampago",
        "sobrenome": "Marquinho",
        "turma": "1A",
        "disciplinas": "Copa pistão",
        "ra": "1010101"
    }
    response = client.post('/alunos', json=new_aluno)
    assert response.status_code == 201
    assert response.json['message'] == 'Aluno adicionado com sucesso!'
````
---

### **3. Monitoramento: Prometheus e Grafana**
Pasta: `prometheus`

Arquivo: `prometheus.yml`  
```yaml
global:
  scrape_interval: 15s  # Coleta de métricas a cada 15 segundos para todos os jobs

scrape_configs:
  - job_name: 'prometheus'  # Coleta de métricas do Prometheus
    static_configs:
      - targets: 
          - 'localhost:9090'  # Alvo é o próprio Prometheus

  - job_name: 'mysqld_exporter'  # Coleta de métricas do MySQL
    static_configs:
      - targets: 
          - '192.168.100.8:9104'  # Alvo é o MySQL Exporter
```
Pasta: `grafana/provisioning`

Arquivo: `datasource.yml`  
```yaml
apiVersion: 1 

datasources:
  - name: Prometheus 
    type: prometheus  
    access: proxy  
    url: http://prometheus:9090  
    isDefault: true  
    jsonData:
      timeInterval: 5s  
```
Pasta: `grafana/provisioning`

Arquivo: `dashboard.yml`  
```yaml
apiVersion: 1

providers:
  - name: 'MariaDB Dashboards'
    orgId: 1
    folder: ''
    type: file
    disableDeletion: false
    editable: true
    options:
      path: /var/lib/grafana/dashboards
```
Pasta: `grafana`

Arquivo: `Dockerfile_grafana`

````
FROM grafana/grafana:latest

USER root

# Certifique-se de que o diretório `provisioning/datasources` e `provisioning/dashboards` existem
RUN mkdir /var/lib/grafana/dashboards

# Copiar os arquivos para o diretório correto
COPY provisioning/datasource.yml /etc/grafana/provisioning/datasources/
COPY provisioning/dashboard.yml /etc/grafana/provisioning/dashboards/
COPY dashboards/mariadb_dashboard.json /var/lib/grafana/dashboards/

# Garantir permissões para o usuário grafana
RUN chown -R 472:472 /etc/grafana/provisioning

USER grafana
````
Pasta: `grafana/dashboards`

Arquivo: `mariadb_dashboard.json`

````
{
  "uid": "simple_dashboard",
  "title": "Desempenho HTTP - Métricas Padrão",
  "tags": ["HTTP", "Prometheus", "Desempenho"],
  "timezone": "browser",
  "schemaVersion": 16,
  "version": 1,
  "panels": [
    {
      "type": "graph",
      "title": "Taxa de Requisições HTTP",
      "datasource": "Prometheus",
      "gridPos": { "x": 0, "y": 0, "w": 12, "h": 6 },
      "targets": [
        {
          "expr": "rate(prometheus_http_requests_total[1m])",
          "legendFormat": "Requisições/s",
          "refId": "A"
        }
      ],
      "lines": true,
      "linewidth": 2,
      "fill": 1
    },
    {
      "type": "graph",
      "title": "Latência Média de Requisições",
      "datasource": "Prometheus",
      "gridPos": { "x": 12, "y": 0, "w": 12, "h": 6 },
      "targets": [
        {
          "expr": "rate(prometheus_http_request_duration_seconds_sum[1m]) / rate(prometheus_http_request_duration_seconds_count[1m])",
          "legendFormat": "Latência Média (s)",
          "refId": "B"
        }
      ],
      "lines": true,
      "linewidth": 2,
      "fill": 1
    },
    {
      "type": "graph",
      "title": "Requisições HTTP em Andamento",
      "datasource": "Prometheus",
      "gridPos": { "x": 0, "y": 6, "w": 12, "h": 6 },
      "targets": [
        {
          "expr": "promhttp_metric_handler_requests_in_flight",
          "legendFormat": "Em andamento",
          "refId": "C"
        }
      ],
      "lines": true,
      "linewidth": 2,
      "fill": 1
    },
    {
      "type": "graph",
      "title": "Requisições HTTP - Taxa de Erro",
      "datasource": "Prometheus",
      "gridPos": { "x": 12, "y": 6, "w": 12, "h": 6 },
      "targets": [
        {
          "expr": "rate(prometheus_http_requests_total{status!~'2..'}[1m])",
          "legendFormat": "Taxa de Erro",
          "refId": "D"
        }
      ],
      "lines": true,
      "linewidth": 2,
      "fill": 1
    }
  ],
  "refresh": "10s",
  "time": { "from": "now-1h", "to": "now" },
  "overwrite": true
}
````
---

## **Pipeline CI/CD: Jenkins**

Arquivo: `Jenkinsfile`
````
pipeline {
    agent any

    environment {
        REPOSITORY_URL = 'https://github.com/samuelcney/trabalho-devops-2303469.git'
        BRANCH_NAME = 'main'
        CONTAINERS = 'mariadb flask test mysqld_exporter prometheus grafana'
    }

    stages {
        stage('Cloning repository') {
            steps {
                git branch: "${BRANCH_NAME}", url: "${REPOSITORY_URL}"
            }
        }

        stage('Build containers') {
            steps {
                script {
                    echo 'Stopping existing containers...'
                    sh 'docker-compose down'

                    echo 'Building Docker images...'
                    sh 'docker-compose build'
                }
            }
        }

        stage('Start Containers') {
            steps {
                script {
                    echo 'Starting Docker containers...'
                    sh "docker-compose up -d ${CONTAINERS}"
                    sleep 25
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    try {
                        echo 'Running tests...'
                        sh 'docker-compose run --rm test'
                    } catch (Exception e) {
                        currentBuild.result = 'FAILURE'
                        error 'Pipeline process stopped because tests failed'
                    }
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline executed successfully'
        }
        failure {
            echo 'The pipeline fails to execute'
            sh 'docker-compose down'
        }
    }
}
````
---
## **Configuração Docker Compose**

Arquivo: `docker-compose.yml`
````
services:
  flask:
    build:
      context: ./flask
      dockerfile: Dockerfile_flask
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=development
    depends_on:
      - mariadb

  mariadb:
    build:
      context: ./mariadb
      dockerfile: Dockerfile_mariadb
    ports:
      - "3307:3306"
    environment:
      MYSQL_ROOT_PASSWORD: root_password
      MYSQL_DATABASE: school_db
      MYSQL_USER: flask_user
      MYSQL_PASSWORD: flask_password

  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"
    depends_on:
      - mysqld_exporter
    command:
      - "--config.file=/etc/prometheus/prometheus.yml"

  mysqld_exporter:
    image: prom/mysqld-exporter
    ports:
      - "9104:9104"
    environment:
      DATA_SOURCE_NAME: "user:password@(mariadb:3306)/"
    depends_on:
      - mariadb

  grafana:
    build:
      context: ./grafana
      dockerfile: Dockerfile_grafana
    ports:
      - "3000:3000"
    depends_on:
      - prometheus

  test:
    build:
      context: ./flask
      dockerfile: Dockerfile_flask
    command: ["pytest", "/app/test_app.py"]
    depends_on:
      - mariadb
      - flask
    environment:
      - DATABASE_URL=mysql+pymysql://flask_user:flask_password@mariadb:3306/school_db
    networks:
      - default
````
---
## **Passo a Passo de Execução e Resultados**
Abaixo estão as imagens que ilustram os resultados do projeto em execução:

- **Jenkins**  
Acesse a URL: `http://localhost:8080`.  

1. **Faça login no Jenkins** com suas credenciais.  

2. **Crie um Novo Projeto**:  
   - Clique em "Nova Tarefa".  
   - Insira um nome para o pipeline, como **"trabalho-devops"**.  
   - Escolha a opção **"Pipeline"** e clique em **"OK"**.  

![Imagem Jenkins](imagens/jenkins1.JPG)  

3. **Configurar o Pipeline**:  
   - Na página de configuração do pipeline, vá até a seção **"Build Triggers"**.  
   - Ative a opção **"Consultar periodicamente o SCM"**.  
   - Adicione o seguinte cronograma para que o Jenkins verifique o repositório regularmente: `H/5 * * * *`.  

4. **Definir o Script do Pipeline**:  
   - Role até a seção **"Pipeline"**.  
   - Selecione **"Pipeline Script from SCM"**.  

![Imagem Jenkins](imagens/jenkins2.JPG)  

5. **Configurar o Repositório Git**:  
   - No campo **SCM**, escolha **"Git"**.  
   - Informe o endereço do repositório do projeto:  
     `https://github.com/samuelcney/trabalho-devops-2303469`.
   - Informe a branch na qual irá acessar os dados. 

6. **Salvar as Alterações**:  
   - Clique em **Salvar** para finalizar a configuração.  

7. **Executar o Pipeline**  
   - Acesse a página inicial do Jenkins e localize o pipeline recém-criado.

   - Clique no pipeline e, em seguida, selecione a opção **"Construir Agora"** para dar início à execução.
         
   ![Imagem Jenkins](imagens/jenkins3.JPG)
   - Monitore os logs em tempo real para verificar o progresso.
   ![Imagem Jenkins](imagens/jenkins4.JPG)

- **Grafana**:
Acesse a URL: `http://localhost:3000`

Faça login no Grafana:

- Usuário: admin
- Senha: admin 

Verifique a dashboard provisionado automaticamente e visualize as métricas de requisições.

![Dashboard](imagens/grafana.JPG)

- **Flask**

Acesse a URL: ` http://localhost:5000 `
![Imagem da Aplicação Flask funcionando](imagens/flask1.JPG)

- Clique em Alunos, assim podendo visualizar os registros criados pelos testes
![Imagem da Aplicação Flask funcionando](imagens/flask2.JPG)

---


