# Documentação - API e Funcionalidades

## Autenticação
- Rota frontend: `/login` (POST com form)
- Sessões Flask utilizadas; cookie de sessão é criado após login.

## Endpoints principais (API)
- `GET /api/me` -> retorna usuário atual (id, username, role).
- `GET /api/resources` -> lista todos recursos (requer login).
- `POST /api/resources` -> cria recurso (requer role: gerente|admin).
- `GET /api/resources/<id>` -> detalhes do recurso.
- `PUT /api/resources/<id>` -> atualiza recurso (role: gerente|admin).
- `DELETE /api/resources/<id>` -> exclui recurso (role: admin).
- `GET /api/stats` -> estatísticas simples.

## Roles
- `funcionario` — acesso de leitura ao dashboard e lista de recursos.
- `gerente` — leitura + criação e edição de recursos.
- `admin` — todos os privilégios, inclusive exclusão.

## Observações de segurança (para avaliação)
- Em produção, troque `SECRET_KEY` por valor forte e use HTTPS.
- Valide e sanitize entradas no backend para evitar injeção.
- Para sessão mais segura, considere Flask-Login e proteção CSRF.
