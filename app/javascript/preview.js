document.addEventListener('DOMContentLoaded', function() {
  if ( document.getElementById('item-image')){
    const ImageList = document.getElementById('image-list')

    // 選択した画像を表示する関数
    const createImageHTML = (blob) => {

    // 画像が表示されている場合のみ、すでに存在している画像を削除する
    const imageContent = document.querySelector('img');
    if (imageContent){
      imageContent.remove();
    }

      // 画像を表示するためのdiv要素を生成
      const imageElement = document.createElement('div')
      imageElement.setAttribute('class', "image-element")
      let imageElementNum = document.querySelectorAll('.image-element').length

      // 表示する画像を生成
      const blobImage = document.createElement('img')
      blobImage.setAttribute('src', blob)
      
      //画像の高さを100pxにする
      blobImage.height = 100

      // ファイル選択ボタンを生成
      // const inputHTML = document.createElement('input')
      // inputHTML.setAttribute('id', `item-image-${imageElementNum}`)
      // inputHTML.setAttribute('name', 'return[images][]')
      // inputHTML.setAttribute('type', 'file')

      // 生成したHTMLの要素をブラウザに表示させる
      imageElement.appendChild(blobImage)
      // imageElement.appendChild(inputHTML)
      ImageList.appendChild(imageElement);
 
      

      // inputHTML.addEventListener('change', (e) => {
      //   file = e.target.files[0];
      //   blob = window.URL.createObjectURL(file);

      //   createImageHTML(blob)
      // })
    }

    document.getElementById('item-image').addEventListener('change', (e) => {
      let file = e.target.files[0];
      let blob = window.URL.createObjectURL(file);

      createImageHTML(blob)

    });
  }
});