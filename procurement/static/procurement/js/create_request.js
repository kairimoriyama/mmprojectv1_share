
  // 初期値として0を設定
  function input_zero(){
    document.getElementById('amount').children[0].value = 0;
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
  
 