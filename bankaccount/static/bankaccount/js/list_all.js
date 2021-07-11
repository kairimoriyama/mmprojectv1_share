const detail_form = document.getElementById("detail_form");
const filter_bt_on = document.getElementById("filter_bt_on");
const filter_bt_off = document.getElementById("filter_bt_off");

function display_off(){

  detail_form.style.display ="none";
  filter_bt_on.style.display ="flex";
  filter_bt_off.style.display ="none";
};


function display_on(){
  
  detail_form.style.display ="flex";
  filter_bt_on.style.display ="none";
  filter_bt_off.style.display ="flex";
};

//表示・非表示の初期値
function display_criteria(){

  if (parseInt(localStorage.getItem('bankaccount_display_key'))==1) {
    display_on();    
  }else{
    display_off();
  };
};
window.onload = display_criteria();

// ボタンで表示・非表示切り替え
function display_switch_bt(){

  if(detail_form.style.display=="none"){
    display_on();
    localStorage.setItem('bankaccount_display_key', '1'); //1を設定
  }else{
    display_off();
    localStorage.setItem('bankaccount_display_key', '0'); //0を設定
  }
};



// selected_bankAccount 自動入力
function selected_bankAccount(){

  let bankAccount = document.getElementById('id_bankAccount').value;
  console.log(bankAccount)

  document.getElementById("selected_bankAccount").value = bankAccount;
};

document.getElementById('id_bankAccount').addEventListener('focusout', () => {
  console.log("test");
  selected_bankAccount();
});


// selected_journalCategory 自動入力
function selected_journalCategory(){

  let journalCategory = document.getElementById('id_journalCategory').value;
  console.log(journalCategory)

  document.getElementById("selected_journalCategory").value = journalCategory;
};

document.getElementById('id_journalCategory').addEventListener('focusout', () => {
  console.log("test");
  selected_journalCategory();
});


// category 自動入力
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


// 検索条件をローカルストレージへ保存（ボタン：検索、移動、詳細、戻る）
function set_search_key(){

  localStorage.setItem('bankaccount_count_key', '1'); //カウント1を設定
  localStorage.removeItem('bankaccount_search_key');

  let selected_bankAccount = document.getElementById('selected_bankAccount').value;
  console.log('selected_bankAccount')
  console.log(selected_bankAccount)

  let bankAccount = document.getElementById('id_bankAccount').value;
  let journalCategory = document.getElementById('id_journalCategory').value;

  //ラジオボタンの値を確認
  let arOrAp = document.getElementsByName('arOrAp');
  let len = arOrAp.length;
  let checkedValue = '';

  for (let i = 0; i < len ; i++){
    if (arOrAp[i].checked){
      checkedValue = arOrAp[i].value;
    }
  }

  let progress = document.getElementById('progress').checked;
  let description1 = document.getElementById('description1').value;
  let description2 = document.getElementById('description2').value;
  let adminMemo = document.getElementById('adminMemo').value;
  let transactionDateFrom = document.getElementById('transactionDateFrom').value;
  let transactionDateTo = document.getElementById('transactionDateTo').value;
  let amountFrom = document.getElementById('accountAmountFrom').value;
  let amounTo = document.getElementById('accountAmountTo').value;

  let dataset = ({
    "key0": selected_bankAccount,
    "key1": bankAccount,
    "key2": journalCategory,
    "key3": checkedValue,
    "key4": progress,
    "key5": description1,
    "key6": description2,
    "key7": adminMemo,
    "key8": transactionDateFrom,
    "key9": transactionDateTo,
    "key10": amountFrom,
    "key11": amounTo,
  });
 
  let datasetJSON = JSON.stringify(dataset); // JSONに変換
  localStorage.setItem('bankaccount_search_key', datasetJSON); 

};


function count_key_clear(){
  localStorage.removeItem('bankaccount_count_key'); //他のページへ遷移する場合にcount_key削除
};


function get_search_key() {

  let dataset = JSON.parse(localStorage.getItem('bankaccount_search_key'));

  if (dataset === null) {

  }else{

    // 検索条件をフォームに入力
    document.getElementsByName('selected_bankAccount').value = dataset["key0"];

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

      //検索条件による抽出実行
      // document.getElementById('search_btn').click(); 
    };

    // selected_bankAccountの情報を更新
    selected_bankAccount();

    // selected_journalCategoryの情報を更新
    selected_journalCategory()

  };
};

window.onload = get_search_key(); //読み込み時に遷移前の検索条件を入力




function clear_criteria(){

  document.getElementById('selected_bankAccount').value= null;
  document.getElementById('selected_journalCategory').value= null;

  document.getElementById('id_bankAccount').value= null;
  document.getElementById('id_journalCategory').value= null;
  document.getElementsByName('arOrAp')[2].checked = true;
  document.getElementById('progress').checked = false;
  document.getElementById('description1').value= null;
  document.getElementById('description2').value= null;
  document.getElementById('adminMemo').value= null;
  document.getElementById('transactionDateFrom').value= null;
  document.getElementById('transactionDateTo').value= null;
  document.getElementById('accountAmountFrom').value= null;
  document.getElementById('accountAmountTo').value= null;

};
