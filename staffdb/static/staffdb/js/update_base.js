
// 完了日削除
function clearCompletionDate() {
    let today = new Date();
    let yyyy = null;
    let mm = null;
    let dd = null;
    document.getElementById("completionDate").firstElementChild.value= yyyy+'-'+mm+'-'+dd;
};

// 完了日自動入力
function setCompletionDate() {
    let today = new Date();
    today.setDate(today.getDate());
    let yyyy = today.getFullYear();
    let mm = ("0"+(today.getMonth()+1)).slice(-2);
    let dd = ("0"+today.getDate()).slice(-2);
    document.getElementById("completionDate").firstElementChild.value=yyyy+'-'+mm+'-'+dd;
};

// 期日削除
function clearDueDate() {
    let today = new Date();
    let yyyy = null;
    let mm = null;
    let dd = null;
    document.getElementById("dueDate").firstElementChild.value= yyyy+'-'+mm+'-'+dd;
};

// 期日自動入力
function setDueDate() {
    let today = new Date();
    today.setDate(today.getDate());
    let yyyy = today.getFullYear();
    let mm = ("0"+(today.getMonth()+1)).slice(-2);
    let dd = ("0"+today.getDate()).slice(-2);
    document.getElementById("dueDate").firstElementChild.value=yyyy+'-'+mm+'-'+dd;
};

function changeBoxColor_blue(){
    document.getElementById('progress').firstElementChild.style.backgroundColor = "rgb(221, 237, 253)";
    document.getElementById('completionDate').firstElementChild.style.backgroundColor = "rgb(221, 237, 253)";
};

function changeBoxColor_white(){
    document.getElementById('progress').firstElementChild.style.backgroundColor = "white";
    document.getElementById('completionDate').firstElementChild.style.backgroundColor = "white";
};

function changeBoxColor_gray(){
document.getElementById('progress').firstElementChild.style.backgroundColor = "rgb(216, 214, 214)";
document.getElementById('completionDate').firstElementChild.style.backgroundColor = "rgb(216, 214, 214)";
};


//期日・完了日の表示切り替え条件
function due_complete_set(){
let s =document.getElementById("completionDate").firstElementChild.value;

console.log(s)

if(s == null || s =="" || s === undefined){
  document.getElementById("dueDate").style.display ="flex";
  document.getElementById("completionDate").style.display ="none";
  document.getElementById("due_complete_select").value="期日"
  changeBoxColor_white();
}else{
  document.getElementById("dueDate").style.display ="none";
  document.getElementById("completionDate").style.display ="flex";
  document.getElementById("due_complete_select").value="完了日"
  changeBoxColor_blue();
}
};  
// 画面開いた際に実行
window.onload = due_complete_set(); 


// 期日・完了日の切り替えに応じて表示変更
function due_complete_change(){
let p = document.getElementById("due_complete_select").value;


if(p == "期日"){
  document.getElementById("dueDate").style.display ="flex";
  document.getElementById("completionDate").style.display ="none";
  changeBoxColor_white();
  clearCompletionDate();
  document.getElementById("progress").firstElementChild.value=2;
  setDueDate();
  
}else{
  document.getElementById("dueDate").style.display ="none";
  document.getElementById("completionDate").style.display ="flex";
  changeBoxColor_blue();
  setCompletionDate();
  document.getElementById("progress").firstElementChild.value=4;
  clearDueDate();
}
};


//Progressの値に応じて completionDate の値を更新
function progressSelect() {

let select = document.getElementById('progress').firstElementChild.value;

// 完了
if (select==4){
  document.getElementById("due_complete_select").value="完了日"
  document.getElementById("dueDate").style.display ="none";
  document.getElementById("completionDate").style.display ="flex";
  changeBoxColor_blue();
  setCompletionDate();
  clearDueDate();

// 実施なし
}else if (select==3){
    document.getElementById("due_complete_select").value="期日"
    document.getElementById("dueDate").style.display ="none";
    document.getElementById("completionDate").style.display ="flex";
    changeBoxColor_gray();
    clearCompletionDate();
    clearDueDate();

// 新規・進行中
}else{
  document.getElementById("due_complete_select").value="期日"
  document.getElementById("dueDate").style.display ="flex";
  document.getElementById("completionDate").style.display ="none";
  changeBoxColor_white();
  clearCompletionDate();
  setDueDate();
};
};
