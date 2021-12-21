document.addEventListener('DOMContentLoaded', function(){

var imgList =[
  "assets/items/top_image4.jpg",
  "assets/items/top_image3.jpg",
  "assets/items/top_image2.jpg",
  "assets/items/top_image.jpg",
]   


// 画像とナビの要素を自動で追加
for(var i = 0; i < imgList.length; i++) {
	// li要素を取得
	var slide = document.createElement("li");
	// li要素の中に画像タグを埋め込む
	slide.innerHTML = "<img src='" + imgList[i] + "'>";

	// li要素をクラス名「slider-inner」の子要素として追加
	document.getElementsByClassName("slider-inner")[0].appendChild(slide);


}

// スライドの数を取得(処理のために-1する)
var length = imgList.length - 1;

// クラス名「imageSlide」に画像の1枚の要素を格納
var imageSlide = document.getElementsByClassName("slider-inner")[0].getElementsByTagName("li");

// 「現在○○枚目のスライドを表示している」というインデックス番号を格納する変数
var nowIndex = 0;
// 現在表示されている画像とドットナビにクラス名を付ける
imageSlide[nowIndex].classList.add("show");

// スライドがアニメーション中か判断するフラグ
var isChanging = false;
// スライドのsetTimeoutを管理するタイマー
var slideTimer;
// スライド切り替え時に呼び出す関数
function sliderSlide(val) {
	if (isChanging === true) {
		return false;
	}
	isChanging = true;
	// 現在表示している画像とナビからクラス名を削除
	imageSlide[nowIndex].classList.remove("show");
	nowIndex = val;
	// 次に表示するスライドとナビにカレントクラスを設定
	imageSlide[nowIndex].classList.add("show");
	// アニメーションが終わるタイミングでisChangingのステータスをfalseに
	slideTimer = setTimeout(function(){
		isChanging = false;
	}, 600);
}

// 左矢印のナビをクリックした時のイベント
document.getElementById("arrow-prev").addEventListener("click", function(){
	var index = nowIndex - 1;
	if(index < 0){
	  index = length;
	}
	sliderSlide(index);
}, false);

// 右矢印のナビをクリックした時のイベント
document.getElementById("arrow-next").addEventListener("click", function(){
	var index = nowIndex + 1;
	if(index > length){
	  index = 0;
	}
  sliderSlide(index);
}, false);

})
