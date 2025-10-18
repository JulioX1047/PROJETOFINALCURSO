async function getJSON(path){ const r=await fetch(path); return await r.json(); }
async function init(){
  const me = await getJSON('/api/me');
  const nav = document.getElementById('nav-user');
  if(me.user){
    nav.innerHTML = '<span>'+me.user.username+' ('+me.user.role+')</span> <a href="/logout">Sair</a>';
    loadStats();
    loadResources();
  } else {
    nav.innerHTML = '<a href="/login">Entrar</a>';
  }
  document.getElementById('btn-add').addEventListener('click', ()=> showForm());
  document.getElementById('form-resource').addEventListener('submit', onSubmitResource);
  document.getElementById('cancel-edit').addEventListener('click', ()=> hideForm());
}
async function loadStats(){
  const s = await getJSON('/api/stats');
  document.getElementById('stats-content').innerText = JSON.stringify(s, null, 2);
}
async function loadResources(){
  const list = await getJSON('/api/resources');
  const el = document.getElementById('resources-list');
  if(!list.length) el.innerText = 'Nenhum recurso cadastrado.';
  else {
    let html = '<table><tr><th>Nome</th><th>Tipo</th><th>Local</th><th>Status</th><th>Ações</th></tr>';
    list.forEach(r=>{
      html += `<tr><td>${r.name}</td><td>${r.type}</td><td>${r.location||''}</td><td>${r.status}</td><td>
        <button data-id="${r.id}" class="btn-edit">Editar</button>
        <button data-id="${r.id}" class="btn-delete">Excluir</button>
      </td></tr>`;
    });
    html += '</table>';
    el.innerHTML = html;
    document.querySelectorAll('.btn-edit').forEach(b=>b.addEventListener('click', onEdit));
    document.querySelectorAll('.btn-delete').forEach(b=>b.addEventListener('click', onDelete));
  }
}
function showForm(data){
  document.getElementById('resource-form').style.display='block';
  document.getElementById('form-resource').id && (()=>{})();
  const f = document.querySelector('#form-resource');
  if(data){
    f.id.value = data.id;
    f.name.value = data.name;
    f.type.value = data.type;
    f.location.value = data.location;
    f.status.value = data.status;
    f.notes.value = data.notes;
  } else {
    f.id.value=''; f.name.value=''; f.type.value=''; f.location.value=''; f.status.value='disponivel'; f.notes.value='';
  }
}
function hideForm(){ document.getElementById('resource-form').style.display='none'; }
async function onSubmitResource(e){
  e.preventDefault();
  const f = e.target;
  const data = { name: f.name.value, type: f.type.value, location: f.location.value, status: f.status.value, notes: f.notes.value };
  if(f.id.value){
    // update
    const res = await fetch('/api/resources/'+f.id.value, { method:'PUT', headers:{'Content-Type':'application/json'}, body: JSON.stringify(data) });
    if(res.ok){ hideForm(); loadResources(); }
    else alert('Erro ao atualizar');
  } else {
    const res = await fetch('/api/resources', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(data) });
    if(res.ok){ hideForm(); loadResources(); }
    else alert('Erro ao criar');
  }
}
async function onEdit(e){
  const id = e.target.dataset.id;
  const r = await getJSON('/api/resources/'+id);
  showForm(r);
}
async function onDelete(e){
  if(!confirm('Confirma exclusão?')) return;
  const id = e.target.dataset.id;
  const res = await fetch('/api/resources/'+id, { method:'DELETE' });
  if(res.ok) loadResources();
  else alert('Erro ao excluir (verifique permissões)');
}
window.addEventListener('DOMContentLoaded', init);
