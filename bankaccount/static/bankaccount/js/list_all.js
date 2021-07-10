// const filter_items = document.getElementById("detail_form");
// const filter_bt_on = document.getElementById("filter_bt_on");
// const filter_bt_off = document.getElementById("filter_bt_off");

// function display_off(){
  
//   filter_items.style.display ="none";
//   filter_bt_on.style.display ="flex";
//   filter_bt_off.style.display ="none";

//   document.getElementsByName('arOrAp')[2].checked = true;
//   document.getElementById('progress').checked = false;
//   document.getElementById('description1').value= null;
//   document.getElementById('description2').value= null;
//   document.getElementById('adminMemo').value= null;
//   document.getElementById('transactionDateFrom').value= null;
//   document.getElementById('transactionDateTo').value= null;
//   document.getElementById('accountAmountFrom').value= null;
//   document.getElementById('accountAmountTo').value= null;

// };
// // window.onload = display_off();

// function display_on(){
  
//   filter_items.style.display ="flex";
//   filter_bt_on.style.display ="none";
//   filter_bt_off.style.display ="flex";

// };

// function detail_change(){

//   if(filter_items.style.display=="none"){

//     display_on();

//     localStorage.setItem('bankaccount_display', '1'); //1を設定
    
//   }else{

//     display_off();

//     localStorage.setItem('bankaccount_display', '0'); //0を設定
//   }
// };


// 検索条件をローカルストレージへ保存（ボタン：検索、移動、詳細、戻る）
function set_search_key(){

  localStorage.setItem('bankaccount_count_key', '1'); //カウント1を設定
  localStorage.removeItem('bankaccount_search_key');

  let selected_bankAccount = document.getElementById('id_bankAccount').value;
  let selected_journalCategory = document.getElementById('id_journalCategory').value;

  //ラジオボタンの値を確認
  let selected_arOrAp = document.getElementsByName('arOrAp');
  let len = selected_arOrAp.length;
  let checkedValue = '';

  for (let i = 0; i < len ; i++){
    if (selected_arOrAp[i].checked){
      checkedValue = selected_arOrAp[i].value;
    }
  }

  let selected_progress = document.getElementById('progress').checked;
  let selected_description1 = document.getElementById('description1').value;
  let selected_description2 = document.getElementById('description2').value;
  let selected_adminMemo = document.getElementById('adminMemo').value;
  let selected_transactionDateFrom = document.getElementById('transactionDateFrom').value;
  let selected_transactionDateTo = document.getElementById('transactionDateTo').value;
  let selected_amountFrom = document.getElementById('accountAmountFrom').value;
  let selected_amounTo = document.getElementById('accountAmountTo').value;

  let dataset = ({
    "key1": selected_bankAccount,
    "key2": selected_journalCategory,
    "key3": checkedValue,
    "key4": selected_progress,
    "key5": selected_description1,
    "key6": selected_description2,
    "key7": selected_adminMemo,
    "key8": selected_transactionDateFrom,
    "key9": selected_transactionDateTo,
    "key10": selected_amountFrom,
    "key11": selected_amounTo,
  });
 
  let datasetJSON = JSON.stringify(dataset); // JSONに変換
  localStorage.setItem('bankaccount_search_key', datasetJSON); 


//   let dataset_display = JSON.parse(localStorage.getItem('bankaccount_display'));

//   if (dataset_display == "1") {

//     display_on();

//     localStorage.setItem('bankaccount_display', '1'); //1を設定
    
//   }else{

//     display_off();

//     localStorage.setItem('bankaccount_display', '0'); //0を設定
//   };

};


function count_key_clear(){
  localStorage.removeItem('bankaccount_count_key'); //他のページへ遷移する場合にcount_key削除
};


function get_search_key() {

  let dataset = JSON.parse(localStorage.getItem('bankaccount_search_key'));

  if (dataset === null) {

  }else{

    // 検索条件をフォームに入力
    document.getElementById('id_bankAccount').value= dataset["key1"];
    document.getElementById('id_journalCategory').value= dataset["key2"];

    let i = Number(dataset["key3"]);
    console.log(i)
    document.getElementsByName('arOrAp')[i].checked = true;

    if (dataset["key4"] == true) {
      document.getElementById('progress').checked = true;
    }else{
      document.getElementById('progress').checked = false;
    };

    document.getElementById('description1').value= dataset["key5"];
    document.getElementById('description2').value= dataset["key6"];
    document.getElementById('adminMemo').value= dataset["key7"];
    document.getElementById('transactionDateFrom').value= dataset["key8"];
    document.getElementById('transactionDateTo').value= dataset["key9"];
    document.getElementById('accountAmountFrom').value= dataset["key10"];
    document.getElementById('accountAmountTo').value= dataset["key11"];

    // 更新・他のページからの遷移の際に検索実施
    if (parseInt(localStorage.getItem('bankaccount_count_key'))==1) { //カウント1であればそのまま実行

      localStorage.removeItem('bankaccount_count_key'); 
      localStorage.removeItem('bankaccount_search_key');
      
    }else{
      localStorage.setItem('bankaccount_count_key', '1'); //カウント1を設定
      document.getElementById('search_btn').click(); //検索条件による抽出実行
    };
  };
};

window.onload = get_search_key(); //読み込み時に遷移前の検索条件を入力


// category 
function selected_record(){

  let selected_record = document.getElementsByName('selected_record');
  let len_selected_record = selected_record.length;
  let selected_record_id = []
  

  for (let k = 0; k < len_selected_record ; k++){
    if (selected_record[k].checked){
      selected_record_id.push(Number(selected_record[k].value));
    }
  }
  document.getElementById("selected_record_list").value = selected_record_id;
};

