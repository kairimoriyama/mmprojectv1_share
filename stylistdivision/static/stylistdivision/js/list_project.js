const detail_form = document.getElementById("detail_form");


function display_off(){

  detail_form.style.display ="none";
  document.getElementById('display_button').checked = true;

};


function display_on(){
  
  detail_form.style.display ="flex";
  document.getElementById('display_button').checked = false;

};

//表示・非表示の初期値
function display_criteria(){

  if (parseInt(localStorage.getItem('stylistdivision_display_key'))==1) {
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
    localStorage.setItem('stylistdivision_display_key', '1'); //1を設定
  }else{
    display_off();
    localStorage.setItem('stylistdivision_display_key', '0'); //0を設定
  }
};


// record 自動入力
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

  localStorage.setItem('stylistdivision_count_key', '1'); //カウント1を設定
  localStorage.removeItem('stylistdivision_search_key');


  let arCheck = document.getElementById('id_projectProgress').value;
  let description2 = document.getElementById('description2').value;
  let memo = document.getElementById('memo').value;
  let transactionDateFrom = document.getElementById('transactionDateFrom').value;
  let transactionDateTo = document.getElementById('transactionDateTo').value;
  let amountFrom = document.getElementById('amountFrom').value;
  let amountTo = document.getElementById('amountTo').value;

  let dataset = ({
    // "key1": arCheck,
    "key2": description2,
    "key3": memo,
    "key4": transactionDateFrom,
    "key5": transactionDateTo,
    "key6": amountFrom,
    "key7": amountTo,
  });
 
  let datasetJSON = JSON.stringify(dataset); // JSONに変換
  localStorage.setItem('stylistdivision_search_key', datasetJSON); 

};


function count_key_clear(){
  localStorage.removeItem('stylistdivision_count_key'); //他のページへ遷移する場合にcount_key削除
};


function get_search_key() {

  let dataset = JSON.parse(localStorage.getItem('stylistdivision_search_key'));

  if (dataset === null) {

  }else{

    // 検索条件をフォームに入力

    document.getElementById('id_projectProgress').value= dataset["key1"];
    document.getElementById('description2').value= dataset["key2"];
    document.getElementById('memo').value= dataset["key3"];
    document.getElementById('transactionDateFrom').value= dataset["key4"];
    document.getElementById('transactionDateTo').value= dataset["key5"];
    document.getElementById('amountFrom').value= dataset["key6"];
    document.getElementById('amountTo').value= dataset["key7"];

    // 更新・他のページからの遷移の際に検索実施
    if (parseInt(localStorage.getItem('stylistdivision_count_key'))==1) { //カウント1であればそのまま実行

      localStorage.removeItem('stylistdivision_count_key'); 
      localStorage.removeItem('stylistdivision_search_key');
      
    }else{
      localStorage.setItem('stylistdivision_count_key', '1'); //カウント1を設定

      //検索条件による抽出実行
      // document.getElementById('search_btn').click(); 
    };

  };
};

window.onload = get_search_key(); //読み込み時に遷移前の検索条件を入力


function clear_criteria(){

  localStorage.setItem('stylistdivision_display_key', '1'); //1を設定

  document.getElementById('id_projectProgress').value= null;
  document.getElementById('description2').value= null;
  document.getElementById('memo').value= null;
  document.getElementById('transactionDateFrom').value= null;
  document.getElementById('transactionDateTo').value= null;
  document.getElementById('amountFrom').value= null;
  document.getElementById('amountTo').value= null;

};
