async function atualizaDados() {
  const resposta = await fetch('/ping/db_status');
  const dados = await resposta.json(); 
  return dados;
}
//cria primeira div 
async function create_div_father(father_ID, acronym){
  const father = document.getElementById(father_ID);
  const newDiv = document.createElement('div');
  newDiv.id = acronym;
  father.appendChild(newDiv);
}
//cria elemento do H7 
async function create_div_child(father_ID, nick, acronym){ // o ftaher_id tambem e o acronymo
  const father = document.getElementById(father_ID);
  const newItem = document.createElement('h7');
  newItem.textContent = nick;
  newItem.id = (acronym + '-h7');
  newItem.className ='status';
  father.appendChild(newItem);
}
// cria o botão
async function create_button(acronym, status){
  const father = document.getElementById(acronym + '-h7');
  const newButton = document.createElement('button');
  newButton.textContent = status;
  newButton.id = (acronym + '-status');
  newButton.className = 'button-status';
  father.appendChild(newButton);
}

async function insert_data() {
  const api = await atualizaDados(); 
  data_api = api;
  for (let i = 0; i < api.length; i++) { 
  
    switch (api[i][2]) { 
      case 1:
        create_div_father("24H", api[i][3]); 
        break;
      case 2:
        create_div_father('CEO', api[i][3]);
        break;
      case 3:
        create_div_father('USF', api[i][3]);
        break;
      case 4:
        create_div_father('FISIO', api[i][3]);
        break;
      case 5:
        create_div_father('OUTROS', api[i][3]);
        break;
    }
    await create_div_child(api[i][3], api[i][1], api[i][3]);

    await create_button(api[i][3], api[i][4]);
  }
  
  async function page_status (){
    if (data_api === api){
      const api = await atualizaDados();
      for (let i = 0; i < api.length; i++) {
        const id_div = document.getElementById(api[i][3] + '-status');
        if (id_div.style.backgroundColor != "" && id_div.textContent === api[i][4]) {
          continue;
        }
        else{
          switch (api[i][4]) {
            case "ONN":
              id_div.textContent = api[i][4];
              id_div.style.backgroundColor = 'green';
              break;
            case "OFF":
              id_div.textContent = api[i][4];
              id_div.style.backgroundColor = 'red';
              break;
          }
        }
      }
    }
    else{
      window.location.reload() // recarrega a pagina
    }
    setInterval(page_status, 80000); 
  }
  page_status();
}