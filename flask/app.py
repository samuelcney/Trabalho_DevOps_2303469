import time
import logging
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
from prometheus_flask_exporter import PrometheusMetrics

#Configuração template front-end
@app.route('/')
def index():
    return render_template('index.html')

# Configuração do Flask
app = Flask(__name__)
metrics = PrometheusMetrics(app)

# Configuração da chave secreta
app.config['SECRET_KEY'] = 'minha_chave_secreta_super_secreta'

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:password@localhost/flask_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar SQLAlchemy
db = SQLAlchemy(app)

# Configuração do log
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Tentar conectar ao banco de dados com tentativas limitadas
attempts = 5
for i in range(attempts):
    try:
        with app.app_context():
            db.create_all()  # Cria as tabelas
        logger.info("Banco de dados inicializado com sucesso.")
        break
    except OperationalError:
        if i < attempts - 1:
            logger.warning("Tentativa de conexão com o banco de dados falhou. Tentando novamente em 5 segundos...")
            time.sleep(5)  # Aguardar 5 segundos antes de tentar novamente
        else:
            logger.error("Não foi possível conectar ao banco de dados após várias tentativas.")
            raise

# Modelo de Aluno
class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    ra = db.Column(db.String(50), unique=True, nullable=False)

    def to_dict(self):
        return {"id": self.id, "nome": self.nome, "ra": self.ra}

# Rotas para manipular os alunos
@app.route('/alunos', methods=['POST'])
def cadastrar_aluno():
    data = request.get_json()

    # Validação de entrada
    if not data.get('nome') or not data.get('ra'):
        logger.warning("Tentativa de cadastro com dados incompletos.")
        return jsonify({"erro": "Nome e RA são obrigatórios"}), 400

    novo_aluno = Aluno(nome=data['nome'], ra=data['ra'])
    try:
        db.session.add(novo_aluno)
        db.session.commit()
        logger.info(f"Aluno {data['nome']} adicionado com sucesso.")
        return jsonify(novo_aluno.to_dict()), 201
    except OperationalError as e:
        db.session.rollback()
        logger.error(f"Erro ao salvar aluno: {e}")
        return jsonify({"erro": "Erro ao salvar o aluno"}), 500
    except Exception as e:
        db.session.rollback()
        logger.error(f"Erro desconhecido: {e}")
        return jsonify({"erro": "Erro desconhecido"}), 500

@app.route('/alunos', methods=['GET'])
def listar_alunos():
    alunos = Aluno.query.all()
    logger.info("Listagem de alunos realizada com sucesso.")
    return jsonify([aluno.to_dict() for aluno in alunos]), 200

# Inicializar a aplicação
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

