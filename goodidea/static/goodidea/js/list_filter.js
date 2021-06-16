const filter_items = document.getElementById("filter_items");
const filter_bt_on = document.getElementById("filter_bt_on");
const filter_bt_off = document.getElementById("filter_bt_off");

function display_on(){
  
  filter_items.style.display ="flex";
  filter_bt_on.style.display ="block";
  filter_bt_off.style.display ="none";
  document.getElementById("display_button_color").style.background = "rgb(255, 255, 227)";

  let dataset = JSON.parse(localStorage.getItem('search_key'));

  if (dataset === null) {
    document.getElementById("completionDateFilter").style.display ="none";

    let select = document.getElementById('progress').value;
    if (select=="4"){
        document.getElementById("completionDateFilter").style.display ="block";
      }else{
        document.getElementById("completionDateFilter").style.display ="none";
      };
  };
};

function display_off(){
  
  filter_items.style.display ="none";
    filter_bt_on.style.display ="none";
    filter_bt_off.style.display ="block";
    document.getElementById("display_button_color").style.background = "rgb(192, 222, 236)";
    document.getElementById("completionDateFilter").style.display ="none";

};

//表示・非表示の初期値
function display_criteria(){

  if (parseInt(localStorage.getItem('display_key'))==1) {

    display_on();
    
  }else{

    display_off();

  };
};

window.onload = display_criteria();

function filter_item_bt(){

  if(filter_items.style.display=="none"){

    display_on();

    localStorage.setItem('display_key', '1'); //1を設定
    
  }else{

    display_off();

    localStorage.setItem('display_key', '0'); //0を設定
  }
};

function clear_criteria(){
  localStorage.setItem('display_key', '1'); //0を設定
};


  //登録日From To の初期値
  function submissionDateInit() {
    
    let p = JSON.parse(localStorage.getItem('search_key'));

    if (p === null) {

      let today = new Date();
      today.setDate(today.getDate());
      let yyyy1 = today.getFullYear()-1;
      let yyyy2 = today.getFullYear();
      let mm = ("0"+(today.getMonth()+1)).slice(-2);
      let dd = ("0"+today.getDate()).slice(-2);
      document.getElementById("submissionDateFrom").value=yyyy1+'-'+mm+'-'+dd;
      document.getElementById("submissionDateTo").value=yyyy2+'-'+mm+'-'+dd;

    }else{};

  };

  window.onload = submissionDateInit();


  //Progressの値に応じて completionDate の値を更新
  function progressSelect() {
  
  let dataset = JSON.parse(localStorage.getItem('search_key'));

    if (dataset === null) {

      let select = document.getElementById('progress').value;

      if (select=="4"){
        (function updateCompletionDate() {
          let today = new Date();
          today.setDate(today.getDate());
          let yyyy1 = today.getFullYear()-1;
          let yyyy2 = today.getFullYear();
          let mm = ("0"+(today.getMonth()+1)).slice(-2);
          let dd = ("0"+today.getDate()).slice(-2);
          document.getElementById("completionDateFrom").value=yyyy1+'-'+mm+'-'+dd;
          document.getElementById("completionDateTo").value=yyyy2+'-'+mm+'-'+dd;
        }());
        
        //completionDateFilter の表示

        (function completionDateOn(){
          document.getElementById("completionDateFilter").style.display ="block";
        }());

        console.log('test1')
            
      }else{
        (function completionDateOff(){
          document.getElementById("completionDateFilter").style.display ="none";
        }());

        console.log('test2')
      };

    }else{};
  };


// 検索条件をローカルストレージへ保存（ボタン：検索、移動、詳細、戻る）
function set_search_key(){

  localStorage.setItem('count_key', '1'); //カウント1を設定
  localStorage.removeItem('search_key');

  let staffdb = document.getElementById('staffdb').value;
  let division = document.getElementById('division').value;
  let inchargeStaff = document.getElementById('inchargeStaff').value;
  let inchargeDivision = document.getElementById('inchargeDivision').value;
  let progress = document.getElementById('progress').value;
  let word = document.getElementById('word').value;
  let submissionDateFrom = document.getElementById('submissionDateFrom').value;
  let submissionDateTo = document.getElementById('submissionDateTo').value;
  let completionDateFrom = document.getElementById('completionDateFrom').value;
  let completionDateTo = document.getElementById('completionDateTo').value;


  //ラジオボタンの値を確認
  let ideaOrAction = document.getElementsByName('ideaOrAction');
  let len = ideaOrAction.length;
  let checkedValue = '';

  for (let i = 0; i < len ; i++){
    if (ideaOrAction[i].checked){
      checkedValue = ideaOrAction[i].value;
    }
  }

  let purchase = document.getElementById('purchase').checked;
  let system = document.getElementById('system').checked;
  let internalDiscussion = document.getElementById('internalDiscussion').checked;
  let consideration = document.getElementById('consideration').checked;

  let dataset = ({
    "key1": staffdb,
    "key2": division,
    "key3": inchargeStaff,
    "key4":inchargeDivision,
    "key5": progress,
    "key6": word,
    "key7": submissionDateFrom,
    "key8": submissionDateTo,
    "key9": completionDateFrom,
    "key10": completionDateTo,
    "key11": checkedValue,  //ラジオボタンの値
    "key12": purchase,  //チェックリストの状態
    "key13": system,  //チェックリストの状態
    "key14": internalDiscussion,  //チェックリストの状態
    "key15": consideration  //チェックリストの状態

  });
 
  let datasetJSON = JSON.stringify(dataset); // JSONに変換
  localStorage.setItem('search_key', datasetJSON); 
};


// function count_key_clear(){
//   localStorage.removeItem('count_key'); //他のページへ遷移する場合にcount_key削除
// };


function get_search_key() {

  let dataset = JSON.parse(localStorage.getItem('search_key'));

  if (dataset === null) {

  }else{

    // 検索条件をフォームに入力
    document.getElementById('staffdb').value= dataset["key1"];
    document.getElementById('division').value = dataset["key2"];
    document.getElementById('inchargeStaff').value= dataset["key3"];
    document.getElementById('inchargeDivision').value= dataset["key4"];
    document.getElementById('progress').value= dataset["key5"];
    document.getElementById('word').value= dataset["key6"];
    document.getElementById('submissionDateFrom').value= dataset["key7"];
    document.getElementById('submissionDateTo').value= dataset["key8"];
    document.getElementById('completionDateFrom').value= dataset["key9"];
    document.getElementById('completionDateTo').value= dataset["key10"];

    //ラジオボタンの値設定
    let i = Number(dataset["key11"]);
    document.getElementsByName('ideaOrAction')[i].checked = true;

    if (dataset["key12"] == true) {
      document.getElementById('purchase').checked = true;
    }else{
      document.getElementById('purchase').checked = false;
    };

    if (dataset["key13"] == true) {
      document.getElementById('system').checked = true;
    }else{
      document.getElementById('system').checked = false;
    };

    if (dataset["key14"] == true) {
      document.getElementById('internalDiscussion').checked = true;
    }else{
      document.getElementById('internalDiscussion').checked = false;
    };

    if (dataset["key15"] == true) {
      document.getElementById('consideration').checked = true;
    }else{
      document.getElementById('consideration').checked = false;
    };


    // 完了日の表示・非表示切り替え
    if (dataset["key5"]==4) {
      document.getElementById("completionDateFilter").style.display ="block";
    }else{
      document.getElementById("completionDateFilter").style.display ="none";
    };


    // 更新・他のページからの遷移の際に検索実施
    if (parseInt(localStorage.getItem('count_key'))==1) { //カウント1であればそのまま実行

      localStorage.removeItem('count_key'); 
      localStorage.removeItem('search_key');
      
    }else{
      localStorage.setItem('count_key', '1'); //カウント1を設定
      document.getElementById('search_btn').click(); //検索条件による抽出実行
    };
  };
};

window.onload = get_search_key(); //読み込み時に遷移前の検索条件を入力
