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



// 初期値を設定
function input_zero(){
    document.getElementById('amount').children[0].value = document.getElementById('amount').children[1].value.replace(/(\d)(?=(\d\d\d)+(?!\d))/g, '$1,');
  };
  window.onload = input_zero();

  $(function() {
    $('input[type="tel"]')
      .focusout(function(){
  
        // 金額の入力の場合にカンマを自動入力
        let h = $(this).val().replace(/[^0-9]/g, '');   // 入力値から数字（0～9）以外の文字を削除
        let i = h.replace(/(\d)(?=(\d\d\d)+(?!\d))/g, '$1,'); // カンマ区切りの3桁に変換する
        $(this).val(i);  // テキストボックス内の値を上書き
  
        // 合計金額を自動入力
        let amount = Number(document.getElementById('amount').children[0].value.replace(/[^0-9]/g, ''));
  
        // フォームへ自動入力
        document.getElementById('amount').children[1].value = amount;
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