//登録日の初期値
function submissionDateInit() {
    let now = new Date();
    let year = now.getFullYear();
    let mon = ("0"+ (now.getMonth()+1)).slice(-2);
    let day = ("0"+ (now.getDate())).slice(-2);
    let today =year+'/'+mon+'/'+day;
    document.getElementById("submissionDateInit").innerHTML= today;
    }
  window.onload = submissionDateInit();