// Enterによる送信禁止
$(function () {
    $("input").keydown(function (e) {
        if ((e.which && e.which === 13) || (e.keyCode && e.keyCode === 13)) {
            return false;
        } else {
            return true;
        }
    });
  });

    
  $(function() {
    $('input[type="number"]')
      .focusout(function(){
  
        // 合計金額を自動入力
        let sales1 = Number(document.getElementById('id_salesAmount1_inctax').value );
        let sales2 = Number(document.getElementById('id_salesAmount2_inctax').value );
        let sales3 = Number(document.getElementById('id_salesAmount3_inctax').value );
        let sales4 = Number(document.getElementById('id_salesAmount2_notax').value );
        let sales5 = Number(document.getElementById('id_salesAmount3_notax').value );

        let totalSales = sales1 + sales2 + sales3 + sales4 + sales5 ;

          // フォームへ自動入力
        document.getElementById('id_salesTotal').value = totalSales;


        // 合計金額を自動入力
        let cost1 = Number(document.getElementById('id_costAmount1_inctax').value );
        let cost2 = Number(document.getElementById('id_costAmount2_inctax').value );
        let cost3 = Number(document.getElementById('id_costAmount3_inctax').value );
        let cost4 = Number(document.getElementById('id_costAmount2_notax').value );
        let cost5 = Number(document.getElementById('id_costAmount3_notax').value );

        let totalCost = cost1 + cost2 + cost3 +cost4 + cost5 ;

  
        // フォームへ自動入力
        document.getElementById('id_costTotal').value = totalCost;


      });
  });