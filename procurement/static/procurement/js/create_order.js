
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



// 個別・標準発注先の選定
function select_supplier(){
  let irregularSupplier = document.getElementById('irregularSupplier')
  let registeredSupplier = document.getElementById('registeredSupplier')
  if (irregularSupplier.children[0].value=="" || irregularSupplier.children[0].value==null){
    irregularSupplier.children[0].style.background = "rgb(192, 222, 236)";
    registeredSupplier.children[0].style.background = "rgb(255, 255, 227)";
  }else{
    irregularSupplier.children[0].style.background = "rgb(255, 255, 227)";
    registeredSupplier.children[0].style.background = "rgb(192, 222, 236)";
    registeredSupplier.children[0].value = "";
  };
};


// 初期値として0を設定
function input_zero(){
    document.getElementById('amount_t10').children[1].value = 0;
    document.getElementById('amount_t10').children[2].value = 0;
    document.getElementById('amount_t8').children[1].value = 0;
    document.getElementById('amount_t8').children[2].value = 0;
    document.getElementById('amount_t0').children[1].value = 0;
    document.getElementById('amount_t0').children[2].value = 0;
    document.getElementById('amount_total').children[1].value = 0;
    document.getElementById('amount_total').children[2].value = 0;
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
        let amount1 = Number(document.getElementById('amount_t10').children[1].value.replace(/[^0-9]/g, ''));
        let amount2 = Number(document.getElementById('amount_t8').children[1].value.replace(/[^0-9]/g, ''));
        let amount3 = Number(document.getElementById('amount_t0').children[1].value.replace(/[^0-9]/g, ''));
        let amount4 = amount1 + amount2 + amount3;
        document.getElementById('amount_total').children[1].value = String(amount4).replace(/(\d)(?=(\d\d\d)+(?!\d))/g, '$1,');
  
        // フォームへ自動入力
        document.getElementById('amount_t10').children[2].value = amount1;
        document.getElementById('amount_t8').children[2].value = amount2;
        document.getElementById('amount_t0').children[2].value = amount3;
        document.getElementById('amount_total').children[2].value = amount4;
      });
  });


// 標準発注先の変更  標準発注先 or 個別発注先
function change_registeredSupplier(){
  let registeredSupplier = document.getElementById("id_registeredSupplier").value;

  if (registeredSupplier != "" || registeredSupplier != null){
    document.getElementById("id_registeredSupplier").style.background = "rgb(255, 255, 227)";
    document.getElementById("id_irregularSupplier").style.background = "rgb(192, 222, 236)";
    document.getElementById("id_irregularSupplier").value = ""
  };
};

document.getElementById("id_registeredSupplier").addEventListener('focusout', (e) => {
  change_registeredSupplier(e)
});

// 個別発注先の変更  標準発注先 or 個別発注先
function change_irregularSupplier(){
  select_supplier();
};

document.getElementById("id_irregularSupplier").addEventListener('focusout', (e) => {
  change_irregularSupplier(e)
});

