$(document).ready(function() {

    const btns = $('.publish-btn');
    btns.on('click', (evt) => {
      const imageId = $(evt.target).attr("id");
      const text = $(evt.target).html();
      let action;
      console.log(imageId)
      console.log(text)
  
      if (text === "Unpublish") {
        action = "unpublish";
      } else {
        action = "publish";
      }
  
      $.post("/publish", {publish: imageId, action: action}, (res) => {  
        if (res.status === "published") {    
          $(evt.target).html("Unpublish"); 
        }
        if (res.status === "unpublished") {
          $(evt.target).html("Publish");
        }
      });      
    });
  })
  