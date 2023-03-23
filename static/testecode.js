async function atualizaDados() {
  const resposta = await fetch('/API/api');
  const dados = await resposta.json(); 
  return dados;
}

async function insert_status(div_pai, nick, id, status) { 
  const pai = document.getElementById(div_pai);
  const newDiv = document.createElement("h6");
  newDiv.textContent = nick;
  newDiv.className = 'status';
  const new_button = document.createElement('button');
  new_button.textContent = status;

  if (status === 'OFF') { // 
    new_button.style.backgroundColor = 'red';
  } else {
    new_button.style.backgroundColor = 'green';
  }

  pai.appendChild(newDiv);
  newDiv.appendChild(new_button);
}

async function insert_data() {
  const api = await atualizaDados(); 

  for (let i = 0; i < api.length; i++) { 
    switch (api[i][2]) { 
      case 1:
        insert_data_aux("24H", api[i][3], api[i][1]); 
        break;
      case 2:
        insert_data_aux('CEO', api[i][3], api[i][1]);
        break;
      case 3:
        insert_data_aux('USF', api[i][3], api[i][1]);
        break;
      case 4:
        insert_data_aux('FISIO', api[i][3], api[i][1]);
        break;
      case 5:
        insert_data_aux('OUTRAS', api[i][3], api[i][1]);
        break;
    }
  }

  async function load_page() { 
    const api = await atualizaDados(); 

    for (let i = 0; i < api.length; i++) { 
      const item_id = document.getElementById(api[i][3]); 
      await insert_status(item_id, api[i][1], api[i][0], api[i][4]); 
      if (item_id) {
        await insert_status(item_id, api[i][1], api[i][0], api[i][4]); 
      }
    }
  }

  setInterval(load_page, 60000); 
}

function insert_data_aux(div_pai, div_id, text_div) {
  const pai = document.getElementById(div_pai);
  const newdiv = document.createElement('div');
  newdiv.id = div_id;
  newdiv.textContent = text_div;
  pai.appendChild(newdiv);
}
insert_data();