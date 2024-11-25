// URL do back-end Flask
const apiUrl = "http://127.0.0.1:5000/alunos";

// Função para buscar a lista de alunos
async function fetchAlunos() {
    try {
        const response = await fetch(apiUrl);
        const data = await response.json();
        const alunoList = document.getElementById('alunoList');

        alunoList.innerHTML = ''; // Limpa a lista

        data.forEach(aluno => {
            const li = document.createElement('li');
            li.textContent = `ID: ${aluno.id} - Nome: ${aluno.nome} - RA: ${aluno.ra}`;
            alunoList.appendChild(li);
        });
    } catch (error) {
        console.error("Erro ao buscar alunos:", error);
    }
}

// Função para cadastrar um novo aluno
async function cadastrarAluno(event) {
    event.preventDefault();

    const nome = document.getElementById('nome').value;
    const ra = document.getElementById('ra').value;

    try {
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ nome, ra })
        });

        if (response.ok) {
            document.getElementById('formMessage').textContent = 'Aluno cadastrado com sucesso!';
            document.getElementById('formMessage').style.color = 'green';
            fetchAlunos(); // Atualiza a lista de alunos
        } else {
            const errorData = await response.json();
            document.getElementById('formMessage').textContent = errorData.erro || 'Erro ao cadastrar aluno.';
        }
    } catch (error) {
        document.getElementById('formMessage').textContent = 'Erro de conexão.';
    }
}

// Adiciona evento ao formulário
document.getElementById('alunoForm').addEventListener('submit', cadastrarAluno);

// Carrega a lista de alunos ao iniciar
fetchAlunos();

