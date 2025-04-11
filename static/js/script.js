


/*------------------------------------           Nav bar           --------------------------------*/
let open = false;
dp_btn = document.querySelector(".dp_btn");
dp_btn.onclick = ()=>{
  let items = document.querySelectorAll(".nav_items");
    if (open){
      for(let e of items){
        e.style.display = "none";
        e.style["background-color"] = "rgba(255,255,255,0)";
      }
      document.querySelector(".nav_menu").style["background-color"] = "rgba(255,255,255,0)";
      document.querySelector(".img_logo").src = "../static/Images/colored_logo.png";
      open = false;
    }else{
      for(let e of items){
        e.style.display = "flex";
        e.style["background-color"] = "black";
      }
      document.querySelector(".img_logo").src = "../static/Images/white_logo.png";
      document.querySelector(".nav_menu").style["background-color"] = "black";
      open = true;
    }
  }

/*-------------------------------------------------------------------------------------------------*/


/*------------------------------------      Timeline Slide        --------------------------------*/
let last_slide = 9;
let first_slide=0;
next_slide = function (){
  document.querySelector(".left_arrow").style.display="";
  if(last_slide<19){
    first_slide++;
    last_slide++;
    let items_slide = document.querySelectorAll(".slide_img");
    for (let si = 0 ;si<19;si++){
      if(si < first_slide || si >last_slide){
        items_slide[si].style.display="none"
      }else{
        items_slide[si].style.display=""
      }
    }
  }else{
    document.querySelector(".right_arrow").style.display="none";
  }
}


previous_slide = function (){
  document.querySelector(".right_arrow").style.display="";
  if(first_slide>0){
    first_slide--;
    last_slide--;
    let items_slide = document.querySelectorAll(".slide_img");
    for (let si = 0 ;si<19;si++){
      if(si < first_slide || si >last_slide){
        items_slide[si].style.display="none"
      }else{
        items_slide[si].style.display=""
      }
    }  
  }else{
    document.querySelector(".left_arrow").style.display="none";
  }
}
/*-------------------------------------------------------------------------------------------------*/


/*------------------------------------      Timeline Story        ---------------------------------*/
document.onload=(()=>{
  let w_url = window.location.href;
  let r_match = w_url.match(/.*\/timeline\/(\d{1,2})/);
  if (r_match != null){
    let current = Number(r_match[1]);
    document.querySelector(".slide_image").src = "/static/Images/timeline/timeline" + current + ".jpg";
    let items = document.querySelectorAll(".time_item");
    let max = items.length;
    for(let i = 0; i < items.length; i++){
      items[i].style.color="black";
      if(i + 1 == current){
        items[i].style.color = "green";
      }
    }
    items.forEach((e)=>{
      e.onclick = ()=>{
        for(let i = 0;i<items.length;i++){
          items[i].style.color="black";
          if(items[i] == e){
            items[i].style.color = "green";
            current=i+1;
            document.querySelector(".slide_image").src = "/static/Images/timeline/timeline" + current + ".jpg";
          }
        }
      }
    })
    right_clicked =()=>{
      current+=1;
      if (current>max){
        current=1;
      }
      document.querySelector(".slide_image").src="/static/Images/timeline/timeline"+current+".jpg";
      for(let i=0;i<items.length;i++){
        items[i].style.color="black";
        if(i==current-1){
          items[i].style.color="green";
        }
      }
    }
    left_clicked =()=>{
      current-=1;
      if (current<1){
        current=max;
      }
      document.querySelector(".slide_image").src="/static/Images/timeline/timeline"+current+".jpg"; 
      for(let i=0;i<items.length;i++){
        items[i].style.color="black";
        if(i==current-1){
          items[i].style.color="green";
        }
      }

    }
  }
})();




/*-------------------------------------------------------------------------------------------------*/
