document.addEventListener('DOMContentLoaded', function(){
  const btnNavi = document.getElementById("btn-gnavi");
  const navi = document.getElementById("navi");
  

  btnNavi.addEventListener("touchend",function() {

    if (navi.classList.contains("actives") == true) {
      // pullDownParentsにdisplay:block;が付与されている場合（つまり表示されている時）実行される
        // btnNavi.setAttribute("style", "display:flex");
        // navi.setAttribute("style", "display:block;");
        btnNavi.classList.remove("active");
        navi.classList.remove("actives");
      
    } else {
      // pullDownParentsにdisplay:block;が付与されていない場合（つまり非表示の時）実行される
        // btnNavi.removeAttribute("style", "display:flex");
        btnNavi.classList.add("active");
        navi.classList.add("actives");
        // navi.removeAttribute("style", "display:block;");
        // navi.setAttribute("style", "display:none;");

    }
})

})
