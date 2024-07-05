/*
  --------------------------------------------------------------------------------------
  Função para obter a lista existente do servidor via requisição GET
  --------------------------------------------------------------------------------------
*/
const getList = async () => {
    let url = 'http://127.0.0.1:5000/nes';
    fetch(url, {
      method: 'get',
    })
      .then((response) => response.json())
      .then((data) => {
        data.nes.forEach(item => insertList(item.ug, item.nc, item.id, item.valor))
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  }
  
  /*
    --------------------------------------------------------------------------------------
    Chamada da função para carregamento inicial dos dados
    --------------------------------------------------------------------------------------
  */
  getList()
  
  /*
    --------------------------------------------------------------------------------------
    Função para colocar um item na lista do servidor via requisição POST
    --------------------------------------------------------------------------------------
  */
  const postItem = async (inputUG, inputNC, inputNE, inputValor) => {
    const formData = new FormData();
    formData.append('ug', inputUG);
    formData.append('nc', inputNC);
    formData.append('ne', inputNE);
    formData.append('valor', inputValor);
  
    let url = 'http://127.0.0.1:5000/ne';
    fetch(url, {
      method: 'post',
      body: formData
    })
      .then((response) => response.json())
      .catch((error) => {
        console.error('Error:', error);
      });
  }
  
  /*
    --------------------------------------------------------------------------------------
    Função para deletar um item da lista do servidor via requisição DELETE
    --------------------------------------------------------------------------------------
  */
  const deleteItem = (item) => {
    console.log(item)
    let url = 'http://127.0.0.1:5000/ne?id=' + item;
    fetch(url, {
      method: 'delete'
    })
      .then((response) => response.json())
      .catch((error) => {
        console.error('Error:', error);
      });
  }

  /*
  --------------------------------------------------------------------------------------
  Função para adicionar uma nova NE
  --------------------------------------------------------------------------------------
*/

const adicionarNE = () => {
    let inputUG = document.getElementById("numero_UG").value;
    let inputNC = document.getElementById("numero_NC").value;
    let inputNE = document.getElementById("numero_NE").value;
    let inputValor = document.getElementById("valor_NE").value;
  
    if ((inputUG === '')||(inputNC === '')||(inputNE === '')||(inputValor === '')) {
      alert("Dados da nota de empenho estão faltando!");
    } else if (isNaN(inputValor)) {
      alert("Valor precisa ser número!");
    } else {
      insertList(inputUG, inputNC, inputNE, inputValor)
      postItem(inputUG, inputNC, inputNE, inputValor)
      alert("Nota de Empenho adicionada!")
    }
  }

/*
  --------------------------------------------------------------------------------------
  Função para inserir items na lista apresentada
  --------------------------------------------------------------------------------------
*/
const insertList = (UG, NC, NE, valor) => {
    var item = [UG, NC, NE, valor]
    var table = document.getElementById('Tabela_de_NE');
    var row = table.insertRow();
  
    for (var i = 0; i < item.length; i++) {
      var cel = row.insertCell(i);
      cel.textContent = item[i];
      if (i==3) {
        cel.textContent=parseFloat(item[i]).toLocaleString('pt-br',{style: 'currency', currency: 'BRL'});
      }
    }
    insertButton(row.insertCell(-1))
    document.getElementById("numero_UG").value = "";
    document.getElementById("numero_NC").value = "";
    document.getElementById("numero_NE").value = "";
    document.getElementById("valor_NE").value = "";
  
    removeElement()
  }

/*
  --------------------------------------------------------------------------------------
  Função para criar um botão close para cada item da lista
  --------------------------------------------------------------------------------------
*/
const insertButton = (parent) => {
    let span = document.createElement("span");
    let txt = document.createTextNode("\u00D7");
    span.className = "close";
    span.appendChild(txt);
    parent.appendChild(span);
  }


/*
  --------------------------------------------------------------------------------------
  Função para remover um item da lista de acordo com o click no botão close
  --------------------------------------------------------------------------------------
*/
const removeElement = () => {
    let close = document.getElementsByClassName("close");
    // var table = document.getElementById('Tabela_de_NC');
    let i;
    for (i = 0; i < close.length; i++) {
      close[i].onclick = function () {
        let div = this.parentElement.parentElement;
        const nomeItem = div.getElementsByTagName('td')[2].innerHTML
        if (confirm("Você tem certeza?")) {
          div.remove()
          deleteItem(nomeItem)
          alert("Removido!")
        }
      }
    }
  }
  