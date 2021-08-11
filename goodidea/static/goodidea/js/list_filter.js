const filter_items = document.getElementById("filter_items");


function display_on(){
  
  filter_items.style.display ="flex";
  document.getElementById('display_button').checked = false;

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
    document.getElementById('display_button').checked = true;
    document.getElementById("completionDateFilter").style.display ="none";

};

//表示・非表示の初期値
function display_criteria(){

  if (parseInt(localStorage.getItem('goodidea_displayKey'))==1) {

    display_on();
    document.getElementById('display_button').checked = false;
    
  }else{

    display_off();
    document.getElementById('display_button').checked = true;
  };
};

window.onload = display_criteria();

function filter_item_bt(){

  if(filter_items.style.display=="none"){

    display_on();

    localStorage.setItem('goodidea_displayKey', '1'); //1を設定
    
  }else{

    display_off();

    localStorage.setItem('goodidea_displayKey', '0'); //0を設定
  }
};

function clear_criteria(){
  localStorage.setItem('goodidea_displayKey', '1'); //0を設定

  document.getElementById('display_button').checked = false; // 表示モードに設定

  let display_button = document.getElementById('display_button').checked;
  
  let dataset = JSON.parse(localStorage.getItem('search_key'));

  if (dataset === null) {
    
  dataset = ({
    "goodidea_displayButton": display_button //チェックの状態
  });

  }else{
    dataset["goodidea_displayButton"] = false;
  };

  let datasetJSON = JSON.stringify(dataset); // JSONに変換
  localStorage.setItem('search_key', datasetJSON); 

};


  //Progressの値に応じて completionDate の表示を更新
  function progressSelect() {
  
  let dataset = JSON.parse(localStorage.getItem('search_key'));

    if (dataset === null) {

      let select = document.getElementById('progress').value;

      if (select=="4"){
   
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

  let display_button = document.getElementById('display_button').checked;

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
    "key12": purchase,  //チェックの状態
    "key13": system,  //チェックの状態
    "key14": internalDiscussion,  //チェックの状態
    "key15": consideration,  //チェックの状態

    "goodidea_displayButton": display_button //チェックの状態

  });
 
  let datasetJSON = JSON.stringify(dataset); // JSONに変換
  localStorage.setItem('search_key', datasetJSON); 
};


function count_key_clear(){
  localStorage.removeItem('count_key'); //他のページへ遷移する場合にcount_key削除
};


function get_search_key() {

  let dataset = JSON.parse(localStorage.getItem('search_key'));

  if (dataset === null) {

    let params = (new URL(document.location)).searchParams;
    if (params.get('staffdb') != null){
      document.getElementById('staffdb').value = params.get('staffdb');
    }
    if (params.get('division')!= null){
      document.getElementById('division').value = params.get('division');
    }
    if (params.get('inchargeStaff')!= null){
      document.getElementById('inchargeStaff').value = params.get('inchargeStaff');
    }
    if (params.get('inchargeDivision')!= null){
      document.getElementById('inchargeDivision').value = params.get('inchargeDivision');
    }
    if (params.get('progress')!= null){
      document.getElementById('progress').value = params.get('progress');
    }
    if (params.get('word')!= null){
      document.getElementById('word').value = params.get('word');
    }
    if (params.get('submissionDateFrom')!= null){
      document.getElementById('submissionDateFrom').value = params.get('submissionDateFrom');
    }
    if (params.get('submissionDateTo')!= null){
      document.getElementById('submissionDateTo').value = params.get('submissionDateTo');
    }
    if (params.get('completionDateFrom')!= null){
      document.getElementById('completionDateFrom').value = params.get('completionDateFrom');
    }
    if (params.get('completionDateTo')!= null){
      document.getElementById('completionDateTo').value = params.get('completionDateTo');
    }
    if (params.get('ideaOrAction')!= null && params.get('ideaOrAction')<2){
      document.getElementsByName('ideaOrAction')[params.get('ideaOrAction')].checked = true;
    }

    if (params.get('purchase')!= null && params.get('purchase') == 1) {
      document.getElementById('purchase').checked = true;
    }else{
      document.getElementById('purchase').checked = false;
    };

    if (params.get('purchase')!= null && params.get('purchase') == 1) {
      document.getElementById('purchase').checked = true;
    }else{
      document.getElementById('purchase').checked = false;
    };

    if (params.get('system')!= null && params.get('system') == 1) {
      document.getElementById('system').checked = true;
    }else{
      document.getElementById('system').checked = false;
    };

    if (params.get('internalDiscussion')!= null && params.get('internalDiscussion') == 1) {
      document.getElementById('internalDiscussion').checked = true;
    }else{
      document.getElementById('internalDiscussion').checked = false;
    };

    if (params.get('consideration')!= null && params.get('consideration') == 1) {
      document.getElementById('consideration').checked = true;
    }else{
      document.getElementById('consideration').checked = false;
    };


    if (params.get('goodidea_displayButton')!= null && params.get('goodidea_displayButton') == 1) {
      document.getElementById('display_button').checked = false;
    }else{
      document.getElementById('display_button').checked = true;
    };


    // 完了日の表示・非表示切り替え
    if (params.get('progress')!= null  && params.get('progress')==4) {
      document.getElementById("completionDateFilter").style.display ="block";
    }else{
      document.getElementById("completionDateFilter").style.display ="none";
    };

  }else{


    if (dataset["goodidea_displayButton"] == true) {
      document.getElementById('display_button').checked = true;
    }else{
      document.getElementById('display_button').checked = false;
    };

    // 検索条件をフォームに入力
    if (dataset["key1"] != null){
    document.getElementById('staffdb').value= dataset["key1"];
    };
    if (dataset["key2"] != null){
    document.getElementById('division').value= dataset["key2"];
    };
    if (dataset["key3"] != null){
      document.getElementById('inchargeStaff').value= dataset["key3"];
    };
    if (dataset["key4"] != null){
      document.getElementById('inchargeDivision').value= dataset["key4"];
    };
    if (dataset["key5"] != null){
      document.getElementById('progress').value= dataset["key5"];
    };
    if (dataset["key6"] != null){
      document.getElementById('word').value= dataset["key6"];
    };

    if (dataset["key7"] != null){
      document.getElementById('submissionDateFrom').value= dataset["key7"];
    };
    if (dataset["key8"] != null){
      document.getElementById('submissionDateTo').value= dataset["key8"];
    };
    if (dataset["key9"] != null){
      document.getElementById('completionDateFrom').value= dataset["key9"];
    };
    if (dataset["key10"] != null){
      document.getElementById('completionDateTo').value= dataset["key10"];
    };


    //ラジオボタンの値設定
    if (dataset["key11"] != null){
    let i = Number(dataset["key11"]);
    document.getElementsByName('ideaOrAction')[i].checked = true;
    };

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
