#!C:\Ruby22\bin\ruby.exe

require "cgi"
require "uri"
require "net/https"
require "rexml/document"


err_msg = nil
# FORMで送信した内容をこのCGIで受け取るために、このCGIの名前を設定します。
@my_self = ( $0.split("/") )[-1]

# 商品コード (商品毎に識別コードを指定してください。ここでは仮に固定の値を指定しています。)
item_code = "abc12345"

@goods = { "mouse" => "マウス:100",
           "keyboard" => "キーボード:2980",
           "disp" => "ディスプレイ:19800",
           "printer" => "プリンタ:34800",
           "camera" => "デジカメ:42000"
         }

# 課金区分
@mission_item = {
    "1" => "1回課金",
    "21" => "定期課金1",
    "22" => "定期課金2",
    "23" => "定期課金3",
    "24" => "定期課金4",
    "25" => "定期課金5",
    "26" => "定期課金6",
    "27" => "定期課金7",
    "28" => "定期課金8",
    "29" => "定期課金9",
    "30" => "定期課金10",
    "31" => "定期課金11",
    "32" => "定期課金12",
}

# 処理区分
@process_item = {
    "1" => "初回課金",
    "2" => "登録済み課金",
    "3" => "登録のみ",
    "4" => "登録内容変更",
    "7" => "退会取消",
    "9" => "退会",
}

# コンビニコード
@conveni_item = {
    "0"  => "-",
    "11" => "セブンイレブン",
    "21" => "ファミリーマート",
    "31" => "ローソン",
    "32" => "セイコーマート",
    "33" => "ミニストップ",
    "35" => "サークルK",
    "36" => "サンクス",
}

@pref_list = {
    "11" => '北海道',
    "12" => '青森県',
    "13" => '岩手県',
    "14" => '宮城県',
    "15" => '秋田県',
    "16" => '山形県',
    "17" => '福島県',
    "18" => '茨城県',
    "19" => '栃木県',
    "20" => '群馬県',
    "21" => '埼玉県',
    "22" => '千葉県',
    "23" => '東京都',
    "24" => '神奈川県',
    "25" => '新潟県',
    "26" => '富山県',
    "27" => '石川県',
    "28" => '福井県',
    "29" => '山梨県',
    "30" => '長野県',
    "31" => '岐阜県',
    "32" => '静岡県',
    "33" => '愛知県',
    "34" => '三重県',
    "35" => '滋賀県',
    "36" => '京都府',
    "37" => '大阪府',
    "38" => '兵庫県',
    "39" => '奈良県',
    "40" => '和歌山県',
    "41" => '鳥取県',
    "42" => '島根県',
    "43" => '岡山県',
    "44" => '広島県',
    "45" => '山口県',
    "46" => '徳島県',
    "47" => '香川県',
    "48" => '愛媛県',
    "49" => '高知県',
    "50" => '福岡県',
    "51" => '佐賀県',
    "52" => '長崎県',
    "53" => '熊本県',
    "54" => '大分県',
    "55" => '宮崎県',
    "56" => '鹿児島県',
    "57" => '沖縄県'
}

def order_form(err_msg = "", item = nil,user_id = nil,user_name = nil,user_mail_add = nil,user_name_kana = nil, user_tel = nil, process_code = "1", mission_code = "1", conveni_code = "0", st = nil,
               consignee_pref = nil, orderer_pref = nil, consignee_postal = nil, consignee_name = nil, consignee_address = nil, consignee_tel = nil, orderer_postal = nil,
               orderer_name = nil, orderer_address = nil, orderer_tel = nil
              )
    mission_code_item = ""
    process_code_item = ""
    conveni_code_item = ""
    consignee_pref_item = ""
    orderer_pref_item = ""
    # 区分の選択アイテムを作成(HTML埋め込み用)
    @mission_item.sort.each do |key, val|
        mission_code_item += sprintf("<option value=\"%s\" %s>%s</option>\r\n", key, ( key == mission_code ? "selected" : "" ), val )
    end
    # 処理区分の選択アイテムを作成(HTML埋め込み用)
    @process_item.sort.each do |key, val|
        process_code_item += sprintf("<option value=\"%s\" %s>%s</option>\r\n", key, ( key == process_code ? "selected" : "" ), val )
    end
    # コンビニコードの選択アイテムを作成(HTML埋め込み用)
    @conveni_item.sort.each do |key, val|
        conveni_code_item += sprintf("<option value=\"%s\" %s>%s</option>\r\n", key, ( key == conveni_code ? "selected" : "" ), val )
    end
    # 都道府県プルダウン作成
    @pref_list.sort.each do | key, val |
        consignee_pref_item += sprintf("<option value=\"%s\" %s>%s</option>\r\n", key, ( key == consignee_pref ? "selected" : "" ), val )
        orderer_pref_item += sprintf("<option value=\"%s\" %s>%s</option>\r\n", key, ( key == orderer_pref ? "selected" : "" ), val )
    end

    st_normal = ""
    st_conveni = ""
    st_card = ""
    st_atobarai = ""
    if  st == 'conveni' then
        st_conveni = "checked"
    elsif st == 'card' then
        st_card = "checked"
    elsif st == 'atobarai' then
        st_atobarai = "checked"
    else
        st_normal = "checked"
    end
    
    print <<-__HTML__ 
Content-Type: text/html

<html lang="ja"><head>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<title>商品購入サンプル画面</title>
<STYLE TYPE="text/css">
<!--
TABLE.S1 {font-size: 9pt; border-width: 0px; background-color: #E6ECFA; font-size: 9pt;}
TD.S1   {  border-width: 0px; background-color: #E6ECFA;color: #505050; font-size: 9pt;}
TH.S1   {  border-width: 0px; background-color: #7B8EB4;color: #E6ECFA; font-size: 9pt;}
TABLE {  border-style: solid;  border-width: 1px;  border-color: #7B8EB4; font-size: 8pt;}
TD   {  text-align: center; border-style: solid;  border-width: 2px; border-color: #FFFFFF #CCCCCC #CCCCCC #FFFFFF; color: #505050; font-size: 8pt;}
TH   {  background-color: #7B8EB4;border-style: solid;  border-width: 2px; border-color: #DDDDDD #AAAAAA #AAAAAA #DDDDDD; color: #E6ECFA; font-size: 8pt;}
-->
</STYLE>
<script>
function switching(flag,flag2,flag3) {
    document.getElementsByName('conveni_code')[0].disabled=flag
    document.getElementsByName('user_name_kana')[0].disabled=flag
    document.getElementsByName('user_tel')[0].disabled=flag
    document.getElementsByName('mission_code')[0].disabled=flag3
    document.getElementsByName('process_code')[0].disabled=flag3
    document.getElementsByName('consignee_postal')[0].disabled=flag2
    document.getElementsByName('consignee_name')[0].disabled=flag2
    document.getElementsByName('consignee_pref')[0].disabled=flag2
    document.getElementsByName('consignee_address')[0].disabled=flag2
    document.getElementsByName('consignee_tel')[0].disabled=flag2
    document.getElementsByName('orderer_postal')[0].disabled=flag2
    document.getElementsByName('orderer_name')[0].disabled=flag2
    document.getElementsByName('orderer_pref')[0].disabled=flag2
    document.getElementsByName('orderer_address')[0].disabled=flag2
    document.getElementsByName('orderer_tel')[0].disabled=flag2
}
function init(){
    var funcItem = {}
    funcItem["normal"] = function(){ switching(true,false,false) }
    funcItem["card"] = function(){ switching(true,true,false) }
    funcItem["conveni"] = function(){ switching(false,true,true) }
    funcItem["atobarai"] = function(){ switching(true,false,true) }
    var items = document.getElementsByName('st');
    for( var i = 0; i < items.length; i++ ){
        if( items[i].checked ){
            funcItem[items[i].value]();
            return;
        }
    }
}
</script>
</HEAD>
<BODY BGCOLOR="#E6ECFA" text="#505050" link="#555577" vlink="#555577" alink="#557755" onload="init()">
<BR>
<form action="#{@my_self}" method="post">
<table class=S1 width="400" border="0" cellpadding="0" cellspacing="0">
<tr class=S1><td class=S1>

<table class=S1 width="100%" cellpadding="6" align=center>
<tr class=S1><th class=S1 align=left><big>商品購入サンプル</big></th></tr>
</table>

<table class=S1 width="90%" align=center>
 <tr class=S1>
  <td class=S1>
    <br>購入する商品を選択してください。<br>
    <font color="#EE5555"> #{err_msg} </font>
__HTML__
puts "   <table cellspacing=4 cellpadding=4 align=\"left\">"
puts "     <tr><th>商品名</th><th>価格</th></tr>"
	# 商品リストの表示
	@goods.sort.each do |key, val|
	  name, price = val.split(":")
	  checked = (item == key) ? "checked" : ""
	  print "<tr><td><input type=\"radio\" name=\"item\" value=\"%s\" %s>%s</td><td>%s円</td></tr>\n"%[key, checked, name, price]
	end
puts "</table><br><br>"
    print <<-__HTML2__;
  </td>
 </tr>
 <tr class=S1>
  <td class=S1>
    <br>以下の項目を入力してください<br>
   <table cellspacing=4 cellpadding=4 align="left">
    <tr>
     <td>ユーザーID</td>
     <td><input type="text" name="user_id" value="#{user_id}"></td>
    </tr>
    <tr>
     <td>氏名</td>
     <td><input type="text" name="user_name" value="#{user_name}"></td>
    </tr>
    <tr>
     <td>メールアドレス</td>
     <td><input type="text" name="user_mail_add" value="#{user_mail_add}"></td>
    </tr>
    <tr>
        <td>決済区分</td>
        <td><label><input type="radio" name="st" value="normal" onclick="switching(true,false,false)" #{st_normal}>指定無し</label>
        　　<label><input type="radio" name="st" value="card" onclick="switching(true,true,false)" #{st_card}>カード決済</label>
        　　<label><input type="radio" name="st" value="conveni" onclick="switching(false,true,true)" #{st_conveni}>コンビニ決済</label>
        　　<label><input type="radio" name="st" value="atobarai" onclick="switching(true,false,true)" #{st_atobarai}>GMO後払い</label>
        </td>
    </tr>
    <tr>
        <td>コンビニコード</td>
        <td><select name="conveni_code">
                #{conveni_code_item}
            </select>
        </td>
    </tr>
    <tr>
        <td>ユーザ名(カナ)</td>
        <td><input type="text" name="user_name_kana" value="#{user_name_kana}"></td>
    </tr>
    <tr>
        <td>ユーザ電話番号</td>
        <td><input type="text" name="user_tel" value="#{user_tel}"></td>
    </tr>
    <tr>
        <td>送り先郵便番号</td>
        <td><input type="text" name="consignee_postal" value="#{consignee_postal}"></td>
    </tr>
    <tr>
        <td>送り先住所</td>
        <td><select name="consignee_pref">#{consignee_pref_item}</select>
        <input type="text" name="consignee_address" value="#{consignee_address}"></td>
    </tr>
    <tr>
        <td>送り先名</td>
        <td><input type="text" name="consignee_name" value="#{consignee_name}"></td>
    </tr>
    <tr>
        <td>送り先電話番号</td>
        <td><input type="text" name="consignee_tel" value="#{consignee_tel}"></td>
    </tr>
    <tr>
        <td>注文主郵便番号</td>
        <td><input type="text" name="orderer_postal" value="#{orderer_postal}"></td>
    </tr>
    <tr>
        <td>注文主住所</td>
        <td><select name="orderer_pref">#{orderer_pref_item}</select>
        <input type="text" name="orderer_address" value="#{orderer_address}"></td>
    </tr>
    <tr>
        <td>注文主名</td>
        <td><input type="text" name="orderer_name" value="#{orderer_name}"></td>
    </tr>
    <tr>
        <td>注文主電話番号</td>
        <td><input type="text" name="orderer_tel" value="#{orderer_tel}"></td>
    </tr>
    <tr>
        <td>課金区分</td>
        <td><select name="mission_code">
            #{mission_code_item}
            </select>
        </td>
    </tr>
    <tr>
        <td>処理区分</td>
        <td><select name="process_code">
            #{process_code_item}
        </select>
        </td>
    </tr>
   </table>
  </td>
 </tr>
 <tr class=S1>
  <td class=S1>
    <br>
    <input type="hidden" name="come_from" value="here">
    <input type="submit" name="go" value="送信">
  </td>
 </tr>
</table>
  </td>
 </tr>
</table>
</form>
</BODY>
</HTML>
    __HTML2__
  1;
end

def kakunin( item = nil,user_id = nil,user_name = nil,user_mail_add = nil,user_name_kana = nil, user_tel = nil, process_code = "1", mission_code = "1", conveni_code = "0", st = nil,
             consignee_pref = "", orderer_pref = "", consignee_postal = "", consignee_name = "", consignee_address = "", consignee_tel = "", orderer_postal = "",
             orderer_name = "", orderer_address = "", orderer_tel = ""
) 
    confirm_text = ""
    # 確認内容
    # 通常の場合には課金区分
    if st == 'conveni' then
        # 商品名、価格
        confirm_text += "商品名: %s<br>\n価格: %s円<br>\n"%[@item_name, @item_price]
        # コンビニ指定決済の場合、1回課金のみ
        confirm_text += "課金区分: %s<br>\n"%[@mission_item['1']]
        # コンビニ指定決済の場合、初回課金のみ
        confirm_text += "処理区分: %s<br>\n"%[@process_item['1']]
        # 指定がない場合は入力画面のURLがEPSILON側から返されます。
        confirm_text += "ユーザ名(カナ): %s 様<br>\nユーザ電話番号: %s<br>\n"%[user_name_kana, user_tel]
        # 2、コンビニ決済のみなので明示
        confirm_text += "決済方法：コンビニ決済<br>\n"
		if conveni_code != 0 then
	        confirm_text += "コンビニコード: %s<br>\n"%[@conveni_item[conveni_code]]
		end
 	elsif st == 'atobarai' then
        # 商品名、価格
        confirm_text += "商品名: %s<br>\n価格: %s円<br>\n"%[@item_name, @item_price]
        # 後払い指定決済の場合、1回課金のみ
        confirm_text += "課金区分: %s<br>\n"%[@mission_item['1']]
        # 後払い指定決済の場合、初回課金のみ
        confirm_text += "処理区分: %s<br>\n"%[@process_item['1']]
        confirm_text += "決済方法：GMO後払い<br>\n"

        # いずれかが入力されている場合必須入力でチェックを行っているので
        # 郵便番号が入力されていた場合は画面に入力パラメータを表示する
        # ここで指定がない場合はEPSILON側で入力画面が出力される
        if !consignee_postal.empty? then
            confirm_text += "%s: %s<br>\n"%["送り先郵便番号",consignee_postal]
            confirm_text += "%s: %s<br>\n"%["送り先名",consignee_name]
            confirm_text += "%s: %s%s<br>\n"%["送り先住所", @pref_list[consignee_pref], consignee_address]
            confirm_text += "%s: %s<br>\n"%["送り先電話番号",consignee_tel]
            confirm_text += "%s: %s<br>\n"%["注文主郵便番号",orderer_postal]
            confirm_text += "%s: %s<br>\n"%["注文主名",orderer_name]
            confirm_text += "%s: %s%s<br>\n"%["注文主住所", @pref_list[orderer_pref], orderer_address]
            confirm_text += "%s: %s<br>\n"%["注文主電話番号",orderer_tel]
        end
    else
        if process_code == "1" || process_code == "2" then
            confirm_text += "商品名: %s<br>\n価格: %s円<br>\n"%[@item_name, @item_price]
            confirm_text += "課金区分: %s<br>\n"%[@mission_item[mission_code]]
            confirm_text += "処理区分: %s<br>\n"%[@process_item[process_code]]
            confirm_text += "ユーザID: %s<br>\n"%[user_id]
        else
            # 処理区分3からは何がしかの処理
            confirm_text += "処理区分: %s<br>\n"%[@process_item[process_code]]
            confirm_text += "ユーザID: %s<br>\n"%[user_id]
        end
    end
  print <<__HTML__
Content-Type: text/html charset=UTF-8

<html lang="ja"><head>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<title>商品購入サンプル画面</title>
<STYLE TYPE="text/css">
<!--
TABLE.S1 {font-size: 9pt border-width: 0px background-color: #E6ECFA font-size: 9pt}
TD.S1   {  border-width: 0px background-color: #E6ECFAcolor: #505050 font-size: 9pt}
TH.S1   {  border-width: 0px background-color: #7B8EB4color: #E6ECFA font-size: 9pt}
TABLE {  border-style: solid  border-width: 1px  border-color: #7B8EB4 font-size: 8pt}
TD   {  text-align: center border-style: solid  border-width: 2px border-color: #FFFFFF #CCCCCC #CCCCCC #FFFFFF color: #505050 font-size: 8pt}
TH   {  background-color: #7B8EB4border-style: solid  border-width: 2px border-color: #DDDDDD #AAAAAA #AAAAAA #DDDDDD color: #E6ECFA font-size: 8pt}
-->
</STYLE>
</HEAD>
<BODY BGCOLOR="#E6ECFA" text="#505050" link="#555577" vlink="#555577" alink="#557755">
<BR>
<table class=S1 width="400" border="0" cellpadding="0" cellspacing="0">
<tr class=S1><td class=S1>

<table class=S1 width="100%" cellpadding="6" align=center>
<tr class=S1><th class=S1 align=left><big>商品購入サンプル</big></th></tr>
</table>

<table class=S1 width="90%" align=center>
 <tr class=S1>
  <td class=S1>
    <br>以下の商品を注文します。<br>
    よろしければ[確認]ボタンを押してください。<br><br>
    #{confirm_text}
    <br>
    <table class=S1 align=center width="50%">
     <tr class=S1>
      <td class=S1>
       <form action="#{@my_self}" method="post">
        <input type="hidden" name="item" value="#{item}">
        <input type="hidden" name="item_name" value="#{@item_name}">
        <input type="hidden" name="item_price" value="#{@item_price}">
        <input type="hidden" name="user_name" value="#{user_name}">
        <input type="hidden" name="user_id" value="#{user_id}">
        <input type="hidden" name="user_mail_add" value="#{user_mail_add}">
        <input type="hidden" name="conveni_code" value="#{conveni_code}">
        <input type="hidden" name="st" value="#{st}">
        <input type="hidden" name="user_name_kana" value="#{user_name_kana}">
        <input type="hidden" name="user_tel" value="#{user_tel}">
        <input type="hidden" name="mission_code" value="#{mission_code}">
        <input type="hidden" name="process_code" value="#{process_code}">
        <input type="hidden" name="consignee_postal" value="#{consignee_postal}">
        <input type="hidden" name="consignee_name" value="#{consignee_name}">
        <input type="hidden" name="consignee_pref" value="#{consignee_pref}">
        <input type="hidden" name="consignee_address" value="#{consignee_address}">
        <input type="hidden" name="consignee_tel" value="#{consignee_tel}">
        <input type="hidden" name="orderer_postal" value="#{orderer_postal}">
        <input type="hidden" name="orderer_name" value="#{orderer_name}">
        <input type="hidden" name="orderer_pref" value="#{orderer_pref}">
        <input type="hidden" name="orderer_address" value="#{orderer_address}">
        <input type="hidden" name="orderer_tel" value="#{orderer_tel}">
        <input type="submit" name="go" value="戻る">
       </form>
      </td>
      <td class=S1>
       <form action="#{@my_self}" method="post">
        <input type="hidden" name="item" value="#{item}">
        <input type="hidden" name="item_name" value="#{@item_name}">
        <input type="hidden" name="item_price" value="#{@item_price}">
        <input type="hidden" name="user_name" value="#{user_name}">
        <input type="hidden" name="user_id" value="#{user_id}">
        <input type="hidden" name="user_mail_add" value="#{user_mail_add}">
        <input type="hidden" name="conveni_code" value="#{conveni_code}">
        <input type="hidden" name="st" value="#{st}">
        <input type="hidden" name="user_name_kana" value="#{user_name_kana}">
        <input type="hidden" name="user_tel" value="#{user_tel}">
        <input type="hidden" name="mission_code" value="#{mission_code}">
        <input type="hidden" name="process_code" value="#{process_code}">
        <input type="hidden" name="consignee_postal" value="#{consignee_postal}">
        <input type="hidden" name="consignee_name" value="#{consignee_name}">
        <input type="hidden" name="consignee_pref" value="#{consignee_pref}">
        <input type="hidden" name="consignee_address" value="#{consignee_address}">
        <input type="hidden" name="consignee_tel" value="#{consignee_tel}">
        <input type="hidden" name="orderer_postal" value="#{orderer_postal}">
        <input type="hidden" name="orderer_name" value="#{orderer_name}">
        <input type="hidden" name="orderer_pref" value="#{orderer_pref}">
        <input type="hidden" name="orderer_address" value="#{orderer_address}">
        <input type="hidden" name="orderer_tel" value="#{orderer_tel}">
        <input type="hidden" name="come_from" value="kakunin">
        <input type="submit" name="go" value="確認">
       </form>
      </td>
     </tr>
    
  </td>
 </tr>
</table>
  </td>
 </tr>
</table>
</form>
</BODY>
</HTML>
__HTML__
  1
end

def result_page(result) 
    result = result.to_i == 1 ? "正常終了<br>" : "異常終了<br>"
print <<__HTML__;
  Content-Type: text/html; charset=UTF-8

  <html lang="ja"><head>
  <META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
  <title>商品購入サンプル画面</title>
  <STYLE TYPE="text/css">
  <!--
  TABLE.S1 {font-size: 9pt; border-width: 0px; background-color: #E6ECFA; font-size: 9pt;}
  TD.S1   {  border-width: 0px; background-color: #E6ECFA;color: #505050; font-size: 9pt;}
  TH.S1   {  border-width: 0px; background-color: #7B8EB4;color: #E6ECFA; font-size: 9pt;}
  TABLE {  border-style: solid;  border-width: 1px;  border-color: #7B8EB4; font-size: 8pt;}
  TD   {  text-align: center; border-style: solid;  border-width: 2px; border-color: #FFFFFF #CCCCCC #CCCCCC #FFFFFF; color: #505050; font-size: 8pt;}
  TH   {  background-color: #7B8EB4;border-style: solid;  border-width: 2px; border-color: #DDDDDD #AAAAAA #AAAAAA #DDDDDD; color: #E6ECFA; font-size: 8pt;}
  -->
  </STYLE>
  </HEAD>
  <BODY BGCOLOR="#E6ECFA" text="#505050" link="#555577" vlink="#555577" alink="#557755">
  <BR>
  <table class=S1 width="400" border="0" cellpadding="0" cellspacing="0">
  <tr class=S1><td class=S1>

  <table class=S1 width="100%" cellpadding="6" align=center>
  <tr class=S1><th class=S1 align=left><big>商品購入サンプル</big></th></tr>
  </table>

  <table class=S1 width="90%" align=center>
    <tr class=S1><td class=S1>
       #{result}
    </td>
    </tr>
  </table>
</table>
</form>
</BODY>
</HTML>
__HTML__
end


# オーダー情報送信先URL(試験用)
# 本番環境でご利用の場合は契約時に弊社からお送りするURLに変更してください。
order_url = URI.parse("https://beta.epsilon.jp/cgi-bin/order/receive_order3.cgi")


# 注文結果取得CGI(試験用)
# 展開環境に応じて適宜変更してください。
confirm_url = "./c_cgi2.cgi"

# 以下の各項目についてご利用環境に沿った設定に変更してください

# 契約番号(8桁) オンライン登録時に発行された契約番号を入力してください。
contract_code = "********"


# 注文番号(注文毎にユニークな番号を割り当てます。ここでは仮に乱数を使用しています。)
order_number = rand(100000000)

# 決済区分 (使用したい決済方法を指定してください。登録時に申し込まれていない決済方法は指定できません。)
# 指定方法はCGI設定マニュアルの「決済区分について」を参照してください。
st_code = {
    "card"    => "10000-0000-00000-00000-00000-00000-00000 ",
    "normal"  => "10100-0000-00000-00010-00000-00000-00000 ",
    "conveni" => "00100-0000-00000-00000-00000-00000-00000 ",
    "atobarai" => "00000-0000-00000-00010-00000-00000-00000 ",
}


# 追加情報 1,2  (入力は必須ではありません)
memo1 = "試験用オーダー情報"
memo2 = ""


# オーダー情報を送信した結果を格納する連想配列
response = Hash.new


# CGIオブジェクトの生成
cgi = CGI.new( :accept_charset => 'UTF-8' )
param = cgi.params
# 商品指定
item = param["item"][0]
# 商品名、価格
@item_name = nil
@item_price = nil
if @goods.key?(item) then
	# 商品リストサンプルの連想配列から、商品名と価格を取り出しています。
	@item_name,@item_price = @goods[item].to_s.split(":")
end

# 課金区分 (1:一回のみ 21～32:定期課金)
# 定期課金について契約がない場合は利用できません。また、定期課金を設定した場合決済区分はクレジットカード決済のみとなります。
mission_code = param["mission_code"][0] || "1"

# 処理区分 (1:初回課金 2:登録済み課金 3:登録のみ 4:登録変更 )
# 各処理区分のご利用に関してはCGI設定マニュアルの「処理区分について」を参照してください。
process_code = param["process_code"][0] || "1"

st = param["st"][0] || "normal"

# ユーザー固有情報
# ここでは仮にフォームに入力してもらっていますが、ユーザーID等の値はクライアント様側で
# 管理されている値を使用してください。
user_id = param["user_id"][0] || ""                # ユーザーID
user_name = param["user_name"][0] || ""            # ユーザー氏名
user_mail_add = param["user_mail_add"][0] || ""    # メールアドレス
come_from = param["come_from"][0]

# コンビニコード直接決済
conveni_code = param["conveni_code"][0] || ""
user_tel = param["user_tel"][0] || ""
user_name_kana = param["user_name_kana"][0] || ""

# 後払い用パラメータ
consignee_postal = param["consignee_postal"][0] || ""
consignee_name = param["consignee_name"][0] || ""
consignee_pref = param["consignee_pref"][0] || ""
consignee_address = param["consignee_address"][0] || ""
consignee_tel = param["consignee_tel"][0] || ""
orderer_postal = param["orderer_postal"][0] || ""
orderer_name = param["orderer_name"][0] || ""
orderer_pref = param["orderer_pref"][0] || ""
orderer_address = param["orderer_address"][0] || ""
orderer_tel = param["orderer_tel"][0] || ""
atobarai_para = consignee_postal.length + consignee_name.length + consignee_address.length + consignee_tel.length + orderer_postal.length + orderer_name.length + orderer_address.length + orderer_tel.length
if come_from == "here" then

    if process_code == "1" || process_code == "2" then
    	if @item_name.nil? || @item_name.empty? then
    		err_msg = "購入する商品を選択してください。"
    	elsif user_id.empty? then
    		err_msg = "ユーザーIDを入力してください。"
    	elsif user_name.empty? then
    		err_msg = "氏名を入力してください。"
    	elsif user_mail_add.empty? then
    		err_msg = "メールアドレスを入力してください。"
    	end
        # コンビニ決済時のみかつコンビニコード指定があるときだけ追加チェック
        if st == "conveni" then
			process_code = "1"
			mission_code = "1"
			# コンビニコードが指定されているときだけ処理
			if conveni_code != "0" then
	            if user_tel.empty? then
	                err_msg = "ユーザ電話番号が未指定です。"
	            elsif user_name_kana.empty? then
	                err_msg = "ユーザ名が未指定です。"
	            end
			end
        elsif ( st == "atobarai" || st == "normal" )  &&  atobarai_para > 0  then
            # 入力チェック
            if !/\A\d+\Z/.match( consignee_postal.to_s ) then
                err_msg = "送り先郵便番号の入力が異常です"
            end
            if consignee_name.empty? then
                err_msg = "送り先名が未入力です"
            end
            if !@pref_list.key?(consignee_pref.to_s) then
                err_msg = "送り先住所(都道府県)が異常です"
            end
            if consignee_address.empty? then
                err_msg = "送り先住所が未入力です"
            end
            if !/\A\d+\Z/.match( consignee_tel.to_s ) then
                err_msg = "送り先電話番号が異常です"
            end
            if !/\A\d+\Z/.match( orderer_postal.to_s ) then
                err_msg = "注文主郵便番号の入力が異常です"
            end
            if orderer_name.empty? then
                err_msg = "注文主名が未入力です"
            end
            if !@pref_list.key?(orderer_pref.to_s) then
                err_msg = "注文主住所(都道府県)が異常です"
            end
            if orderer_address.empty? then
                err_msg = "注文主住所が未入力です"
            end
            if  !/\A\d+\Z/.match( orderer_tel.to_s ) then
#                err_msg = "注文主電話番号が異常です"
            end
        end

    	unless  err_msg.nil? then
       		# パラメータに異常がある場合は、もう一度入力画面を表示します。
			order_form(err_msg, item, user_id, user_name, user_mail_add, user_name_kana, user_tel, process_code, mission_code, conveni_code, st,
					   consignee_pref, orderer_pref,
					   consignee_postal, consignee_name, consignee_address, consignee_tel, orderer_postal, orderer_name, orderer_address, orderer_tel
			 )

            exit 1
    	else
            # パラメータを正常に受け取れた場合は、購入確認画面を表示します。
			kakunin(item, user_id, user_name, user_mail_add, user_name_kana, user_tel, process_code, mission_code, conveni_code, st,
		       	    consignee_pref, orderer_pref,
					consignee_postal, consignee_name, consignee_address, consignee_tel, orderer_postal, orderer_name, orderer_address, orderer_tel
			 )
            exit 0
    	end
    else
        if process_code == "3" || process_code == "4" then
            # ユーザ登録 || ユーザ変更
            
            # ユーザIDチェック
            if user_id.empty? then
    		    err_msg = "ユーザーIDを入力してください。"
            elsif !/\A[a-zA-Z0-9\.\-\+\/\@]+\Z/.match(user_id) then 
                err_msg = "ユーザIDにご利用できない文字が含まれています。"
            # ユーザ名が入っていない
            elsif  user_name.empty? then
                err_msg = "氏名を入力してください。"
            # ユーザメールアドレスチェック
    	   elsif user_mail_add.empty? then
    		   err_msg = "メールアドレスを入力してください。"
            elsif  !/\A[a-zA-Z0-9\.\-\_\@]+\Z/.match(user_mail_add) then
                err_msg = "ユーザメールアドレスにご利用できない文字が含まれています。"
            end
        elsif process_code == "7" || process_code == "9" then
            if user_id.empty? then
    		    err_msg = "ユーザーIDを入力してください。"
            elsif !/\A[a-zA-Z0-9\.\-\+\/\@]+\Z/.match(user_id) then 
                err_msg = "ユーザIDにご利用できない文字が含まれています。"
            end
        else
            # process_codeの指定が処理対象外の場合
            process_code = "1"
            err_msg = "処理区分の指定が異常です。"
        end

        # エラーが有る場合は終了
        unless err_msg.nil? then
			order_form(err_msg, item, user_id, user_name, user_mail_add, user_name_kana, user_tel, process_code, mission_code, conveni_code, st )
            exit 1
        else
            # パラメータを正常に受け取れた場合は、購入確認画面を表示します。
			kakunin(item, user_id, user_name, user_mail_add, user_name_kana, user_tel, process_code, mission_code, conveni_code, st )
            exit 0
        end
    end
elsif come_from == "kakunin" then  # 購入確認画面で[確認]ボタンを押した場合
	# EPSILONに情報送信を行います。
	post_data = Net::HTTP::Post.new( order_url.request_uri )
	data = Hash.new
	if process_code == "1" || process_code == "2" then
		data = { 	
		   "version" => "2",
           "contract_code" => contract_code,
           "user_id" => user_id,           
           "user_name" => user_name,  
           "user_mail_add" => user_mail_add,
           "item_code" => item_code,       
           "item_name" => @item_name,
           "order_number" => order_number, 
           "st_code" => st_code[st],
           "mission_code" => mission_code, 
           "item_price" => @item_price,     
           "process_code" => process_code, 
           "memo1" => memo1,               
           "memo2" => memo2,
           "xml" => "1",
           "character_code" => "UTF8"
        }
        if st == 'conveni' && conveni_code != '0' then
           data["conveni_code"] = conveni_code
           data["user_tel"] = user_tel
           data["user_name_kana"] = user_name_kana
        elsif ( st ==  'normal' || st == 'atobarai' ) && consignee_postal.length > 0 then
            # 後払い決済用パラメータが入力されている場合は送信パラメータに含めておく
            # その場合delivery_codeは99固定
            data["delivery_code"] = 99
            data["consignee_postal"] = consignee_postal
            data["consignee_name"] = consignee_name
            data["consignee_address"] = "%s%s"%[@pref_list[consignee_pref], consignee_address]
            data["consignee_tel"] = consignee_tel
            data["orderer_postal"] = orderer_postal
            data["orderer_name"] = orderer_name
            data["orderer_address"] ="%s%s"%[@pref_list[orderer_pref], orderer_address]
            data["orderer_tel"] = orderer_tel         
        end
	elsif process_code == '3' || process_code == '4' then
		data = { "version" => "2",
                 "contract_code" => contract_code,
                 "user_id" => user_id,
                 "user_name" => user_name,
                 "user_mail_add" => user_mail_add,
                 "st_code" => "10000-0000-00000-00000-00000-00000-00000",
                 "process_code" => process_code,
                 "memo1" => memo1,
                 "memo2" => memo2,
                 "xml" => "1",
                 "charset" => "UTF8" }
    elsif process_code == '7' || process_code == '9' then
        data = {
            "version" => 2,
            "contract_code" => contract_code,
            "user_id"       => user_id,
            "process_code" => process_code,
            "memo1"        => memo1,
            "memo2"        => memo2,
            "xml"          => 1,
        }
	end
    post_data.set_form_data( data )
    http = Net::HTTP.new(order_url.host,order_url.port)
    http.use_ssl = true # SSLを有効にします


    http.open_timeout = 20 # セッション接続までのタイムアウト時間
    http.read_timeout = 20 # 応答を待つまでのタイムアウト時間
    # EPSILONに接続して送信
    result = http.start do
        http.request( post_data )
    end   
    # 結果の確認
    if result.code == "200" then
        ##xml = REXML::Document.new(result.body)
        xml = REXML::Document.new(( result.body.gsub("x-sjis-cp932","Shift_JIS"))) # 文字コードをSJISとして読み込む(CP932はSJISの拡張なので基本はOK)
        xml.elements.each("Epsilon_result/result") do |element|
            element.attributes.each do |name, value|
                response[name] = CGI.unescape(value)
            end
        end
    else
        # イプシロンに対して接続に失敗
        err_msg =  "データの送信に失敗しました %s:%s<br><br>"%[result.code,result.message]
		order_form(err_msg, item, user_id, user_name, user_mail_add) 
        exit 1
    end
    # result = 1 の場合、送信に成功
    if response["result"] == "1" then
        # recdirectがある場合
        if response.key?("redirect") then
            print cgi.header({"status" => "REDIRECT", "Location" => response["redirect"]})
            exit
        elsif response.key?("trans_code") then 
            
            print cgi.header({"status" => "REDIRECT", "Location" => confirm_url+("?trans_code=%d"%[response["trans_code"]] )})
            exit
        else
            # リダイレクトの指定なし、trans_codeがない場合は会員情報変更等
            result_page( response['result'] );
            exit
        end
    else
        # データ送信結果が失敗だった場合、オーダー入力画面に戻し、エラーメッセージを表示します。
        err_msg = "%s:%s"%[response["err_code"],response["err_detail"]]
		order_form(err_msg, item, user_id, user_name, user_mail_add) 
        exit 1
    end
end

order_form(err_msg, item, user_id, user_name, user_mail_add, user_name_kana, user_tel, process_code, mission_code, conveni_code, st,
		   consignee_pref, orderer_pref,
		   consignee_postal, consignee_name, consignee_address, consignee_tel, orderer_postal, orderer_name, orderer_address, orderer_tel
)

