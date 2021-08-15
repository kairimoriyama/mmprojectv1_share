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

  if (parseInt(localStorage.getItem('stylist_project_display_key'))==1) {
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
    localStorage.setItem('stylist_project_display_key', '1'); //1を設定
  }else{
    display_off();
    localStorage.setItem('stylist_project_display_key', '0'); //0を設定
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
  localStorage.removeItem('stylist_project_search_key');


  let projectProgress = document.getElementById('id_projectProgress').value;
  let client = document.getElementById('id_client').value;
  let projectCategory = document.getElementById('id_projectCategory').value;
  let projectName = document.getElementById('projectName').value;
  let description = document.getElementById('description').value;
  let projectDateFrom = document.getElementById('projectDateFrom').value;
  let projectDateTo = document.getElementById('projectDateTo').value;
  let invoiceDateFrom = document.getElementById('invoiceDateFrom').value;
  let invoiceDateTo = document.getElementById('invoiceDateTo').value;
  let salesAmountFrom = document.getElementById('salesAmountFrom').value;
  let salesAmountTo = document.getElementById('salesAmountTo').value;

  let dataset = ({
    "key1": projectProgress,
    "key2": client,
    "key3": projectCategory,
    "key4": projectName,
    "key5": description,
    "key6": projectDateFrom,
    "key7": projectDateTo,
    "key8": invoiceDateFrom,
    "key9": invoiceDateTo,
    "key10": salesAmountFrom,
    "key11": salesAmountTo,
  });
 
  let datasetJSON = JSON.stringify(dataset); // JSONに変換
  localStorage.setItem('stylist_project_search_key', datasetJSON); 

};


function count_key_clear(){
  localStorage.removeItem('stylistdivision_count_key'); //他のページへ遷移する場合にcount_key削除
};


function get_search_key() {

  let dataset = JSON.parse(localStorage.getItem('stylist_project_search_key'));

  if (dataset === null) {

  }else{

    // 検索条件をフォームに入力

    document.getElementById('id_projectProgress').value= dataset["key1"];
    document.getElementById('id_client').value= dataset["key2"];
    document.getElementById('id_projectCategory').value= dataset["key3"];
    document.getElementById('projectName').value= dataset["key4"];
    document.getElementById('description').value= dataset["key5"];
    document.getElementById('projectDateFrom').value= dataset["key6"];
    document.getElementById('projectDateTo').value= dataset["key7"];
    document.getElementById('invoiceDateFrom').value= dataset["key8"];
    document.getElementById('invoiceDateTo').value= dataset["key9"];
    document.getElementById('salesAmountFrom').value= dataset["key10"];
    document.getElementById('salesAmountTo').value= dataset["key11"];

    // 更新・他のページからの遷移の際に検索実施
    if (parseInt(localStorage.getItem('stylistdivision_count_key'))==1) { //カウント1であればそのまま実行

      localStorage.removeItem('stylistdivision_count_key'); 
      localStorage.removeItem('stylist_project_search_key');
      
    }else{
      localStorage.setItem('stylistdivision_count_key', '1'); //カウント1を設定

      //検索条件による抽出実行
      // document.getElementById('search_btn').click(); 
    };

  };
};

window.onload = get_search_key(); //読み込み時に遷移前の検索条件を入力


function clear_criteria(){

  localStorage.setItem('stylist_project_display_key', '1'); //1を設定

  document.getElementById('id_projectProgress').value= null;
  document.getElementById('id_client').value= null;
  document.getElementById('id_projectCategory').value= null;
  document.getElementById('projectName').value= null;
  document.getElementById('description').value= null;
  document.getElementById('projectDateFrom').value= null;
  document.getElementById('projectDateTo').value= null;
  document.getElementById('invoiceDateFrom').value= null;
  document.getElementById('invoiceDateTo').value= null;
  document.getElementById('salesAmountFrom').value= null;
  document.getElementById('salesAmountTo').value= null;

};
