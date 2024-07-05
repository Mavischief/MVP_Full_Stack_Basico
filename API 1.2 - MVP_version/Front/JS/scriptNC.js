/*
  --------------------------------------------------------------------------------------
  Função para obter a lista existente do servidor via requisição GET
  --------------------------------------------------------------------------------------
*/
const getList = async () => {
    let url = 'http://127.0.0.1:5000/ncs';
    fetch(url, {
      method: 'get',
    })
      .then((response) => response.json())
      .then((data) => {
        data.ncs.forEach(item => insertList(item.uasg, item.id, item.valor, item.nd, item.aplicacao, item.descricao))
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
  const postItem = async (inputUasg, inputNC, inputValor, inputND, inputAplicacao, inputDescricao) => {
    const formData = new FormData();
    formData.append('uasg', inputUasg);
    formData.append('id', inputNC);
    formData.append('valor', inputValor);
    formData.append('nd', inputND);
    formData.append('aplicacao', inputAplicacao);
    formData.append('descricao', inputDescricao);
  
    let url = 'http://127.0.0.1:5000/nc';
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
    let url = 'http://127.0.0.1:5000/nc?id=' + item;
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
  Função para adicionar uma nova NC
  --------------------------------------------------------------------------------------
*/

const adicionarNC = () => {
    let inputUasg = document.getElementById("novaUasg").value;
    let inputNC = document.getElementById("novaNC").value;
    let inputValor = document.getElementById("novoValor").value;
    let inputND = document.getElementById("novaND").value;
    let inputAplicacao = document.getElementById("novaAplicacao").value;
    let inputDescricao = document.getElementById("novaDescricao").value;
  
    if ((inputNC === '')||(inputValor === '')||(inputDescricao === '')) {
      alert("Dados da nota de crédito estão faltando!");
    } else if (isNaN(inputValor)) {
      alert("Valor precisa ser número!");
    } else {
      insertList(inputUasg, inputNC, inputValor, inputND, inputAplicacao, inputDescricao)
      postItem(inputUasg, inputNC, inputValor, inputND, inputAplicacao, inputDescricao)
      alert("Nota de Crédito adicionada!")
    }
  }

  const formCurrency = new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
})

/*
  --------------------------------------------------------------------------------------
  Função para inserir items na lista apresentada
  --------------------------------------------------------------------------------------
*/
const insertList = (Uasg, NC, valor, ND, aplicacao, descricao) => {
    var item = [Uasg, NC, valor, ND, aplicacao, descricao]
    var table = document.getElementById('Tabela_de_NC');
    var row = table.insertRow();
  
    for (var i = 0; i < item.length; i++) {
      var cel = row.insertCell(i);
      cel.textContent = item[i];
      
      if (i==2) {
        cel.textContent = parseFloat(item[i]).toLocaleString('pt-br',{style: 'currency', currency: 'BRL'});
      }
    
    }
    insertButton(row.insertCell(-1))
    document.getElementById("novaUasg").value = "";
    document.getElementById("novaNC").value = "";
    document.getElementById("novoValor").value = "";
    document.getElementById("novaND").value = "";
    document.getElementById("novaAplicacao").value = "";
    document.getElementById("novaDescricao").value = "";
  
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
        const nomeItem = div.getElementsByTagName('td')[0].innerHTML
        if (confirm("Você tem certeza?")) {
          div.remove()
          deleteItem(nomeItem)
          alert("Removido!")
        }
      }
    }
  }
  