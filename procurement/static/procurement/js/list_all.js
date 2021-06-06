function menu_default(){

  // 依頼作成
  document.getElementById("create_request").style.display ="block";

  // 検収メニュー
  $("#acceptance_wrapper").hide(0);
  document.getElementById("acceptance_start").style.display ="block";
  document.getElementById("acceptance_done").style.display ="none";
  document.getElementById("acceptance_none").style.display ="none";
  document.getElementById("acceptance_title").style.display ="none";
  
  // 検収メニュー 案件番号
  document.getElementById("selected_order_pk_acceptance").value = "";
  document.getElementById("selected_request_pk_acceptance").value =[];

  // 検討メニュー
  document.getElementById("selected_request_pk_selectSupplier").value =[];
  $("#selectSupplier_wrapper").hide(0);
  document.getElementById("selectSupplier_start").style.display ="block";
  document.getElementById("selectSupplier_done").style.display ="none";
  document.getElementById("selectSupplier_stop").style.display ="none";
  document.getElementById("selectSupplier_title").style.display ="none";

  // 検討メニュー 案件番号
  document.getElementById("selected_order_pk_orderReport").value ="";
  document.getElementById("selected_request_pk_orderReport").value =[];

  // 依頼・発注 金額突合
  document.getElementById('request_amount_int').value = "";
  document.getElementById('order_amount_int').value = "";
  document.getElementById('diff_amount_int').value = "";
};
window.onload = menu_default();


// 依頼と発注の差額を計算
function checkAmount(){

// 発注依頼を選択する度に金額を入力
  let list_request = document.getElementsByName('selected_request');

  // 依頼の件数を確認
  let len_list_request = list_request.length;

  // 依頼の金額を集計するため
  let selected_request_num = 0;
  
  // 各依頼の金額
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
  document.getElementById('request_amount_int').value = num1;

  let str2 = document.getElementById('order_amount').value;
  let num2 = Number(str2.replace(/[^0-9]/g, ''));
  document.getElementById('order_amount_int').value = num2;

  let diff = num2 - num1;
  let wnum = new String(diff).replace(/,/g, "");
  document.getElementById('diff_amount_int').value = wnum;

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

        if (list_orderNumInOrder[k].textContent == orderNumInRequest){
          list_order[k].checked  = true;
        };
      };
    };
  }; 
};

// 発注報告について番号自動入力
function reportOrder_number(){
  //発注番号の自動入力
  let list_order = document.getElementsByName('selected_order');
  let len_list_order = list_order.length;
  let selected_order_pk = ''

  for (let i = 0; i < len_list_order ; i++){
    if (list_order[i].checked){
      selected_order_pk = list_order[i].value;
    }
  }
  document.getElementById("selected_order_pk_orderReport").value = selected_order_pk;

//依頼番号の自動入力
  let list_request = document.getElementsByName('selected_request');
  let len_list_request = list_request.length;
  let selected_request_pk = []

  for (let i = 0; i < len_list_request ; i++){
    if (list_request[i].checked){
      selected_request_pk.push(Number(list_request[i].value));
    }
  }
  document.getElementById("selected_request_pk_orderReport").value = selected_request_pk;

};


// 発注報告
function reportOrder(){

  reportOrder_number();

};


// 依頼番号選択 → 自動入力
function clickRequest() {
  correspondOrderNumber();
  checkAmount();
  reportOrder_number();
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

// 発注番号選択 → 自動入力
function clickOrder() {
  correspondRequest();
  checkAmount();
  reportOrder_number();
}


// 発注準備の実施 
function selectSupplier_start(){

  let list_request = document.getElementsByName('selected_request');
  let len_list_request = list_request.length;
  let selected_request_pk = []

  for (let i = 0; i < len_list_request ; i++){
    if (list_request[i].checked){
      selected_request_pk.push(Number(list_request[i].value));
    }
  }

  if(!selected_request_pk.length){
    alert('対象の依頼を選択してください')
  }else{
    
    $("#selectSupplier_wrapper").show(150);
    $("#amount_check").hide(0);
    document.getElementById("create_request").style.display ="none";
    document.getElementById("acceptance_start").style.display ="none";
    document.getElementById("selectSupplier_start").style.display ="none";
    document.getElementById("selectSupplier_done").style.display ="block";
    document.getElementById("selectSupplier_stop").style.display ="block";
    document.getElementById("selectSupplier_title").style.display ="block";
    
    document.getElementById("create_order").style.display ="none";
    document.getElementById("report_order").style.display ="none";

    document.getElementById("selected_request_pk_selectSupplier").value = selected_request_pk;
  };
};

// 発注準備中止
function selectSupplier_stop(){
  $("#selectSupplier_wrapper").hide(150);
  $("#amount_check").show(0);
  document.getElementById("create_request").style.display ="block";
  document.getElementById("acceptance_start").style.display ="block";
  document.getElementById("selectSupplier_start").style.display ="block";
  document.getElementById("selectSupplier_done").style.display ="none";
  document.getElementById("selectSupplier_stop").style.display ="none";
  document.getElementById("selectSupplier_title").style.display ="none";

  document.getElementById("create_order").style.display ="block";
  document.getElementById("report_order").style.display ="block";
};

// acceptance_start のクリックにより判定
function accepance_start(){
  if(document.getElementById("diff_amount").value != "" && document.getElementById("diff_amount").value == 0){
    $("#acceptance_wrapper").show(150);
    $("#amount_check").hide(0);
    document.getElementById("create_request").style.display ="none";
    document.getElementById("selectSupplier_start").style.display ="none";
    document.getElementById("acceptance_start").style.display ="none";
    document.getElementById("acceptance_done").style.display ="block";
    document.getElementById("acceptance_none").style.display ="block";
    document.getElementById("acceptance_title").style.display ="block";
    
  //発注番号の自動入力
    let list_order = document.getElementsByName('selected_order');
    let len_list_order = list_order.length;
    let selected_order_pk = ''

    for (let i = 0; i < len_list_order ; i++){
      if (list_order[i].checked){
        selected_order_pk = list_order[i].value;
      }
    }
    document.getElementById("selected_order_pk_acceptance").value = selected_order_pk;

  //依頼番号の自動入力
    let list_request = document.getElementsByName('selected_request');
    let len_list_request = list_request.length;
    let selected_request_pk = []

    for (let i = 0; i < len_list_request ; i++){
      if (list_request[i].checked){
        selected_request_pk.push(Number(list_request[i].value));
      }
    }
    document.getElementById("selected_request_pk_acceptance").value = selected_request_pk;


    //検収日の自動入力
    let now = new Date();
    let year = now.getFullYear();
    let mon = ("0"+ (now.getMonth()+1)).slice(-2);
    let day = ("0"+ (now.getDate())).slice(-2);
    let today =year+'-'+mon+'-'+day;
    document.getElementById("acceptanceDate_acceptance").value = today;

  }else{
    alert('未検収の発注と対応する全ての依頼を選択してください')
  };
};

// 検収中止
function accepance_stop(){
  $("#acceptance_wrapper").hide(150);
  $("#amount_check").show(0);
  document.getElementById("create_request").style.display ="block";
  document.getElementById("selectSupplier_start").style.display ="block";
  document.getElementById("acceptance_start").style.display ="block";
  document.getElementById("acceptance_done").style.display ="none";
  document.getElementById("acceptance_none").style.display ="none";
  document.getElementById("acceptance_title").style.display ="none";
};