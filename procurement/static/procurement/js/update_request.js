// クリックでの送信禁止
$(function () {
  $("input").keydown(function (e) {
      if ((e.which && e.which === 13) || (e.keyCode && e.keyCode === 13)) {
          return false;
      } else {
          return true;
      }
  });
});




// 費用負担1 自動入力
function input_costCenter1(){
  let division_pk = document.getElementById("id_requestStaffDivision").value;
  document.getElementById("id_costCenter1").value = division_pk;

  console.log(division_pk)
};
document.getElementById("id_requestStaffDivision").addEventListener('focusout', (e) => {
  input_costCenter1(e)
});