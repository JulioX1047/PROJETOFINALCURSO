# Projeto Final - Indústrias Wayne (DEV FULL STACK)

Aplicação: **Sistema de Gerenciamento de Segurança**
Tecnologias: Python (Flask), SQLite, HTML, CSS, JavaScript (Fetch API).

Funcionalidades:
- Autenticação (usuário/senha) com sessões.
- Diferentes perfis: funcionário, gerente, administrador.
- Gestão de recursos (equipamentos, veículos, dispositivos) com CRUD via API.
- Dashboard simples mostrando estatísticas.
- Frontend responsivo com páginas de login, dashboard e gestão.

Como rodar:
1. Crie um ambiente virtual (recomendado) e instale dependências:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/macOS
   venv\Scripts\activate    # Windows
   pip install -r requirements.txt
   ```

2. Inicialize o banco e crie usuários:
   ```bash
   python seed.py
   ```

3. Rode o servidor:
   ```bash
   flask run
   # ou
   python app.py
   ```

A API roda por padrão em http://127.0.0.1:5000

Documentação das rotas e exemplos de uso estão neste repositório (arquivo `docs.md`).
