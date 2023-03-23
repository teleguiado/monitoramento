async function atualizaDados() {
  const resposta = await fetch('/ping/db_status');
  const dados = await resposta.json(); 
  return dados;
}

async function create_div_father(father_ID, acronym){
  const father = document.getElementById(father_ID);
  const newDiv = document.createElement('div');
  newDiv.id = acronym;

  father.appendChild(newDiv);
}

async function create_div_child(father_ID, nick, acronym){
  const father = document.getElementById(father_ID);
  const newItem = document.createElement('h7');
  newItem.textContent = nick;
  newItem.id = (acronym + '-h7');
  newItem.className ='status';
  
  father.appendChild(newItem);
}

async function create_button(acronym, status){
  const father = document.getElementById(acronym + 'h7');
  const newButton = document.createElement('button');
  newButton.textContent = status;
  newButton.id = (acronym + '-status');
  newButton.className = 'button-status';

  father.appendChild(newButton);
}

async function change_status(id_button, status){
  const button = document.getElementById(id_button);
  switch (status) {
    case "ONN":
      // fazer uma verificação para se caso aumente o numero de unidades 
      break;
  
    case "OFF":

      break;
  }

}

async function insert_data() {
  const api = await atualizaDados(); 

  for (let i = 0; i < api.length; i++) { 
  
    switch (api[i][2]) { 
      case 1:
        insert_data_aux("24H", api[i][4]); 
        break;
      case 2:
        insert_data_aux('CEO', api[i][4]);
        break;
      case 3:
        insert_data_aux('USF', api[i][4]);
        break;
      case 4:
        insert_data_aux('FISIO', api[i][4]);
        break;
      case 5:
        insert_data_aux('OUTRAS', api[i][4]);
        break;
    }
  }

}