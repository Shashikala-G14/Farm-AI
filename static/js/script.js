const wrapper = document.querySelector(".sliderWrapper");
const menuItems = document.querySelectorAll(".menuItem");

menuItems.forEach((item, index) => {
  item.addEventListener("click", () => {
    console.log("you clicked!" + index);
  });
});

// const item=document.getElementsByClassName("buyButton")
// item.addEventListener("click",()=>
// {
//   payment.style.display = "flex"; 
// })

const productButton = document.querySelector(".buyButton");
const payment = document.querySelector(".payment");
const close = document.querySelector(".close");

productButton.addEventListener("click", () => {
  payment.style.display = "flex";
});
close.addEventListener("click", () => {
  payment.style.display = "none";
});
