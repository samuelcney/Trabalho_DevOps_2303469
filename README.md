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

## Estrutura do Projeto

- **Repositório Git**:
  - O repositório é versionado com todos os arquivos de configuração necessários, incluindo Dockerfiles, `docker-compose.yml`, Jenkinsfile, e configurações do Prometheus e Grafana.
  - Commits frequentes documentam o progresso do projeto.

- **Diretórios Principais**:
  - `app/`: Código-fonte da aplicação Flask.
  - `tests/`: Arquivo com testes unitários para validar a funcionalidade de cadastro de aluno.
  - `prometheus/`: Configurações para coleta de métricas no Prometheus.
  - `grafana/`: Configurações de datasources e dashboards para visualização das métricas no Grafana.

## Pipeline CI/CD

A pipeline do Jenkins é configurada para realizar as seguintes etapas:

1. **Download do Código**: Jenkins clona o repositório do projeto.
2. **Execução de Testes**: O teste unitário para o cadastro de aluno é executado para verificar a integridade da aplicação.
3. **Build e Deploy**: O Jenkins gera a imagem Docker da aplicação e realiza o deploy completo, garantindo que todos os serviços (aplicação Flask, MariaDB, Prometheus, Grafana) estejam funcionando corretamente.

## Monitoramento e Dashboard

- **Prometheus**:
  - Configurado para coletar métricas da aplicação Flask e do banco de dados MariaDB.
  - Monitora informações relevantes, como o número de requisições e as consultas realizadas no banco de dados.

- **Grafana**:
  - O dashboard exibe visualizações das métricas, facilitando o acompanhamento de dados em tempo real, como o número de acessos à aplicação e consultas ao banco de dados.
  - Os dashboards são configurados via arquivos de configuração, para facilitar a reprodução do ambiente.

## Instruções para Executar o Projeto

1. **Clone o Repositório**:
   ```bash
   git clone https://github.com/usuario/Trabalho_DevOps_[RA].git
   cd Trabalho_DevOps_[RA]

