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
  let len_list_order = list_request.length;
  console.log(list_orderNumInRequest[1].textContent,1);

  for (let i = 0; i < len_list_request ; i++){
    if (list_request[i].checked && Number(list_orderNumInRequest[i]) > 0){
      orderNumInRequest = list_orderNumInRequest[i].textContent;
      console.log(orderNumInRequest,2);
      for (let j = 0; j < len_list_order ; j++){
        if (list_orderNumInOrder[j].textContent == orderNumInRequest){
          list_order[j].checked  = true;
          console.log(list_order[j]);
        };
      };
    };
  };
};

function clickRequest() {
  correspondOrderNumber();
  checkAmount();
}
