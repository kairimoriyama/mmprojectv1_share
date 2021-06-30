
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


  
$(function() {
  $('input[type="number"]')
    .focusout(function(){

      // 合計金額を自動入力
      let amount1 = Number(document.getElementById('amount_t10').children[1].value.replace(/[^0-9,-]/g, ''));
      let amount2 = Number(document.getElementById('amount_t8').children[1].value.replace(/[^0-9,-]/g, ''));
      let amount3 = Number(document.getElementById('amount_t0').children[1].value.replace(/[^0-9,-]/g, ''));
      let amount4 = amount1 + amount2 + amount3;

      // フォームへ自動入力
      document.getElementById('amount_total').children[1].value = amount4;
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

document.getElementById("id_registeredSupplier").addEventListener('change', (e) => {
  change_registeredSupplier(e)
});

// 個別発注先の変更  標準発注先 or 個別発注先
function change_irregularSupplier(){
  select_supplier();
};

document.getElementById("id_irregularSupplier").addEventListener('change', (e) => {
  change_irregularSupplier(e)
});



// 費用負担1 自動入力 1件目
function input_costCenter1_1(){
let division_pk = document.getElementById("id_orderRequest_orderInfo-0-requestStaffDivision").value;
document.getElementById("id_orderRequest_orderInfo-0-costCenter1").value = division_pk;

console.log(division_pk)
};
document.getElementById("id_orderRequest_orderInfo-0-requestStaffDivision").addEventListener('focusout', (e) => {
  input_costCenter1_1(e)
});

// 費用負担1 自動入力 2件目
function input_costCenter1_2(){
  let division_pk = document.getElementById("id_orderRequest_orderInfo-0-requestStaffDivision").value;
  document.getElementById("id_orderRequest_orderInfo-1-costCenter1").value = division_pk;
  
  console.log(division_pk)
  };
  document.getElementById("id_orderRequest_orderInfo-1-requestStaffDivision").addEventListener('focusout', (e) => {
    input_costCenter1_2(e)
  });
  
