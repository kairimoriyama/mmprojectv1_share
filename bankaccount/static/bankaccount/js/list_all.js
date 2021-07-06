
// 検索条件をローカルストレージへ保存（ボタン：検索、移動、詳細、戻る）
function set_search_key(){

  localStorage.setItem('bankaccount_count_key', '1'); //カウント1を設定
  localStorage.removeItem('bankaccount_search_key');

  let selected_bankAccount = document.getElementById('id_bankAccount').value;

  let dataset = ({
    "key1": selected_bankAccount,
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
    document.getElementById('id_bankAccount').value= dataset["key1"];



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

