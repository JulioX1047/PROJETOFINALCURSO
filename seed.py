from app import db, User, Resource
from werkzeug.security import generate_password_hash

def seed():
    db.create_all()
    if User.query.filter_by(username='admin').first():
        print('Already seeded')
        return
    users = [
        ('admin','admin123','admin'),
        ('gerente','gerente123','gerente'),
        ('func','func123','funcionario'),
    ]
    for u,p,role in users:
        user = User(username=u, password_hash=generate_password_hash(p), role=role)
        db.session.add(user)
    # Sample resources
    res = [
        ('Câmera Externa','Câmera','Telhado','disponivel','Câmera principal na cobertura'),
        ('Veículo de Segurança 1','Veículo','Garagem','em_uso','Patrulha noturna'),
        ('Sensor de Porta A','Sensor','Entrada A','manutencao','Falha detectada'),
    ]
    for name, typ, loc, status, notes in res:
        r = Resource(name=name, type=typ, location=loc, status=status, notes=notes)
        db.session.add(r)
    db.session.commit()
    print('Seed concluído. Usuários: admin/admin123, gerente/gerente123, func/func123')

if __name__ == '__main__':
    seed()
