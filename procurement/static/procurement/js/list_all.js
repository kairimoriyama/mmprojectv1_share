function accepance_menu_default(){
  $("#inspenction").hide(0);
  document.getElementById("acceptance_done").style.display ="none";
  document.getElementById("acceptance_none").style.display ="none";
  document.getElementById("acceptance_title").style.display ="none";
};
window.onload = accepance_menu_default();

// acceptance_start のクリックにより判定
function accepance_start(){
  if(document.getElementById("diff_amount").value != "" && document.getElementById("diff_amount").value == 0){
    $("#inspenction").show(150);
    $("#amount_check").hide(0);
    document.getElementById("create_request").style.display ="none";
    document.getElementById("acceptance_start").style.display ="none";
    document.getElementById("acceptance_done").style.display ="block";
    document.getElementById("acceptance_none").style.display ="block";
    document.getElementById("acceptance_title").style.display ="block";
  }else{
    alert('未検収の発注と対応する全ての依頼を選択してください')
  };
};

// 検収中止
function accepance_stop(){
  $("#inspenction").hide(150);
  $("#amount_check").show(0);
  document.getElementById("create_request").style.display ="block";
  document.getElementById("acceptance_start").style.display ="block";
  document.getElementById("acceptance_done").style.display ="none";
  document.getElementById("acceptance_none").style.display ="none";
  document.getElementById("acceptance_title").style.display ="none";
};

function checkAmount(){

// 発注依頼を選択する度にフォームに金額を入力
  let list_request = document.getElementsByName('selected_request');
  let len_list_request = list_request.length;
  let selected_request_num = 0;

  let list_request_amount = document.getElementsByName('selected_request_amount');

  for (let i = 0; i < len_list_request ; i++){
    if (list_request[i].checked){
      selected_request_num = selected_request_num + Number(list_request_amount[i].textContent.replace(/,/g, ''));
    }
  }
  document.getElementById("request_amount").value=String(selected_request_num).replace(/(\d)(?=(\d\d\d)+(?!\d))/g, '$1,');

// 発注情報を選択する度にフォームに金額を入力
  let list_order = document.getElementsByName('selected_order');
  let len_list_order = list_order.length;
  let selected_order_num = '';

  let list_order_amount = document.getElementsByName('selected_order_amount');

  for (let i = 0; i < len_list_order ; i++){
    if (list_order[i].checked){
      selected_order_num = Number(list_order_amount[i].textContent.replace(/,/g, ''));
    }
  }
  document.getElementById("order_amount").value=String(selected_order_num).replace(/(\d)(?=(\d\d\d)+(?!\d))/g, '$1,');

  // 差額を計算
  let str1 = document.getElementById('request_amount').value;
  let num1 = Number(str1.replace(/[^0-9]/g, ''));

  let str2 = document.getElementById('order_amount').value;
  let num2 = Number(str2.replace(/[^0-9]/g, ''));

  let diff = num2 - num1;
  let wnum = new String(diff).replace(/,/g, "");

  // 最上位桁まで下桁から３桁ごとにカンマ付加を繰り返す
  while(wnum != (wnum = wnum.replace(/^(-?\d+)(\d{3})/, "$1,$2")));
  document.getElementById("diff_amount").value=wnum;
};


// 依頼を選択すると自動で発注を選択
function correspondOrderNumber(){
  let list_request = document.getElementsByName('selected_request');
  let list_orderNumInRequest = document.getElementsByName('orderNumInRequest');
  let list_orderNumInOrder = document.getElementsByName('orderNumInOrder');
  let list_order = document.getElementsByName('selected_order');

  let len_list_request = list_request.length;
  let len_list_order = list_order.length;

  for (let i = 0; i < len_list_request ; i++){
    if (list_request[i].checked && Number(list_orderNumInRequest[i].textContent) > 0){
      
      orderNumInRequest = list_orderNumInRequest[i].textContent;

      // order のチェックを入れる
      for (let k = 0; k < len_list_order ; k++){

        console.log(list_orderNumInOrder[k].textContent);
        if (list_orderNumInOrder[k].textContent == orderNumInRequest){
          list_order[k].checked  = true;
        };
      };
    };
  };
  
};

function clickRequest() {
  correspondOrderNumber();
  checkAmount();
}

// 発注を選択すると自動で依頼を選択
function correspondRequest(){
  let list_request = document.getElementsByName('selected_request');
  let list_orderNumInRequest = document.getElementsByName('orderNumInRequest');
  let list_orderNumInOrder = document.getElementsByName('orderNumInOrder');
  let list_order = document.getElementsByName('selected_order');

  let len_list_request = list_request.length;
  let len_list_order = list_order.length;

  for (let i = 0; i < len_list_order ; i++){
    if (list_order[i].checked){

      orderNumInOrder = list_orderNumInOrder[i].textContent;

      // request に対応する発注番号の有無を調べる
      let orderNumCheck = 0;      
      for (let j = 0; j < len_list_request ; j++){
        if (list_orderNumInRequest[j].textContent == orderNumInOrder){
          orderNumCheck = orderNumCheck + 1; // 1以上なら対応する注文あり
        };
      };
      // request のチェックを入れる
      for (let k = 0; k < len_list_request ; k++){
        if (orderNumCheck>0){
          if (list_orderNumInRequest[k].textContent == orderNumInOrder){
            list_request[k].checked  = true;
          }else{
            list_request[k].checked  = false;
          };
        }else{
          if (Number(list_orderNumInRequest[k].textContent)>0){
            list_request[k].checked  = false;
          };
        };
      };

    };
  };
};

function clickOrder() {
  correspondRequest();
  checkAmount();
}