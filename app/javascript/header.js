document.addEventListener('DOMContentLoaded', function(){
  const btnNavi = document.getElementById("btn-gnavi");
  const navi = document.getElementById("navi");
  

  btnNavi.addEventListener("touchend",function() {
    // btnNavi.setAttribute("style", "display:flex");
    // navi.setAttribute("style", "display:block;");
    // });

    if (navi.getAttribute("style") == "display:none;") {
      // pullDownParentsにdisplay:block;が付与されている場合（つまり表示されている時）実行される
        btnNavi.setAttribute("style", "display:flex");
        navi.setAttribute("style", "display:block;");
        btnNavi.classList.add("active");
    } else {
      // pullDownParentsにdisplay:block;が付与されていない場合（つまり非表示の時）実行される
        btnNavi.removeAttribute("style", "display:flex");
        btnNavi.classList.remove("active");
        navi.removeAttribute("style", "display:block;");
        navi.setAttribute("style", "display:none;");

    }
})

})
