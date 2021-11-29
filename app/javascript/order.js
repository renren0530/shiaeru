document.addEventListener('DOMContentLoaded', function(){
  const Button = document.getElementById("quantity");
  Button.addEventListener("change",(e) =>{
  const quantityButton = document.getElementById("quantity-button");
  quantityButton.setAttribute("value", Button.value);

  })
});