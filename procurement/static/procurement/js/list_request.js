const filter_items = document.getElementById("filter_items");
const filter_bt_on = document.getElementById("filter_bt_on");
const filter_bt_off = document.getElementById("filter_bt_off");

function display_on(){
  
  filter_items.style.display ="flex";
  filter_bt_on.style.display ="block";
  filter_bt_off.style.display ="none";
  document.getElementById("display_button_color").style.background = "rgb(255, 255, 227)";

};

function display_off(){
  
  filter_items.style.display ="none";
    filter_bt_on.style.display ="none";
    filter_bt_off.style.display ="block";
    document.getElementById("display_button_color").style.background = "rgb(192, 222, 236)";

};

//表示・非表示の初期値
function display_criteria(){

  if (parseInt(localStorage.getItem('display_key_peocurement'))==1) {

    display_on();
    
  }else{

    display_off();

  };
};

window.onload = display_criteria();

function filter_item_bt(){

  if(filter_items.style.display=="none"){

    display_on();

    localStorage.setItem('display_key_peocurement', '1'); //1を設定
    
  }else{

    display_off();

    localStorage.setItem('display_key_peocurement', '0'); //0を設定
  }
};

function clear_criteria(){
  localStorage.setItem('display_key_peocurement', '1'); //0を設定
};


  //依頼日From To の初期値
  function submissionDateInit() {
    
    let p = JSON.parse(localStorage.getItem('search_key_peocurement'));

    if (p === null) {

      let today = new Date();
      today.setDate(today.getDate());
      let yyyy = today.getFullYear();
      let mm = ("0"+(today.getMonth()+1)).slice(-2);
      let mm2 = ("0"+(today.getMonth()+2)).slice(-2);
      let dd = ("0"+today.getDate()).slice(-2);

  
      document.getElementById("settlementDateFrom").value=yyyy+'-'+mm+'-'+dd;
      document.getElementById("settlementDateTo").value=yyyy+'-'+mm2+'-'+dd;

    }else{};
  };

  window.onload = submissionDateInit();


// 検索条件をローカルストレージへ保存（ボタン：検索、移動、詳細、戻る）
function set_search_key_peocurement(){

  localStorage.setItem('count_key_peocurement', '1'); //カウント1を設定
  localStorage.removeItem('search_key_peocurement');

  let staffdb = document.getElementById('staffdb').value;
  let division = document.getElementById('division').value;
  let word = document.getElementById('word').value;
  let submissionDateFrom = document.getElementById('submissionDateFrom').value;
  let submissionDateTo = document.getElementById('submissionDateTo').value;
  let settlementDateFrom = document.getElementById('settlementDateFrom').value;
  let settlementDateTo = document.getElementById('settlementDateTo').value;

  //ラジオボタンの値を確認
  let settlementCheck = document.getElementsByName('settlementCheck');
  let len = settlementCheck.length;
  let checkedValue = '';

  for (let i = 0; i < len ; i++){
    if (settlementCheck[i].checked){
      checkedValue = settlementCheck[i].value;
    }
  }


  let dataset = ({
    "key1": staffdb,
    "key2": division,
    "key3": word,
    "key4": submissionDateFrom,
    "key5": submissionDateTo,
    "key6": settlementDateFrom,
    "key7": settlementDateTo,
    "key8": checkedValue,  //ラジオボタンの値

  });
 
  let datasetJSON = JSON.stringify(dataset); // JSONに変換
  localStorage.setItem('search_key_peocurement', datasetJSON); 
};


function get_search_key() {

  let dataset = JSON.parse(localStorage.getItem('search_key_peocurement'));

  if (dataset === null) {

  }else{

    // 検索条件をフォームに入力
    document.getElementById('staffdb').value= dataset["key1"];
    document.getElementById('division').value = dataset["key2"];
    document.getElementById('word').value= dataset["key3"];
    document.getElementById('submissionDateFrom').value= dataset["key4"];
    document.getElementById('submissionDateTo').value= dataset["key5"];
    document.getElementById('settlementDateFrom').value= dataset["key6"];
    document.getElementById('settlementDateTo').value= dataset["key7"];

    //ラジオボタンの値設定
    let i = Number(dataset["key8"]);
    document.getElementsByName('settlementCheck')[i].checked = true;


    // 更新・他のページからの遷移の際に検索実施
    if (parseInt(localStorage.getItem('count_key_peocurement'))==1) { //カウント1であればそのまま実行

      localStorage.removeItem('count_key_peocurement'); 
      localStorage.removeItem('search_key_peocurement');
      
    }else{
      localStorage.setItem('count_key_peocurement', '1'); //カウント1を設定
      document.getElementById('search_btn').click(); //検索条件による抽出実行
    };
  };
};

window.onload = get_search_key(); //読み込み時に遷移前の検索条件を入力


function count_key_clear_peocurement(){
  localStorage.removeItem('count_key_peocurement'); //他のページへ遷移する場合にcount_key削除
};
