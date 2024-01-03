var count=0;
var isFetchingData = false;
$(document).ready(function(){
    $(window).scroll(function(){
      var mainDataDiv = $('#main_data_div');
      var distanceToBottom = mainDataDiv.offset().top + mainDataDiv.outerHeight() - $(window).scrollTop() - $(window).height();

        if(distanceToBottom <= 0){
         if($('#search_value').length){
            console.log('search value')
            if (!isFetchingData) {
               isFetchingData = true
               setTimeout("appendsearch()",1000);
            }
         }
         if($('#category_value').length){
            if (!isFetchingData) {
               isFetchingData = true
               console.log('category_value')
               setTimeout("appendcategory()", 1000);
            }
         }
        }
    });
});

var appendsearch=function(){
   let page_no = Number($('#page_no').val())+1
   let total_page = $('#total_page').val()
   let search_query = $('#search_value').val()
   console.log("|:| ",search_query,page_no)

   if (Number(page_no) <= Number(total_page)){
      $.ajax({
         url: '/search/',
         type: 'GET',
         data: {
             'page': page_no,
             'q':search_query,
             'type':'json'
         },
         success: function(response) {
            console.log(response)
            var add_html=''
            for(let each= 0;each<response.length;each++){
                  add_html += ` 
                  <div class="story-card-wrapper">
          <div class="story_card_col g-col-6 g-col-md-4" data-aos="fade-up"  data-aos-delay="200">
             <div class="news-card">
                <h6 data-aos="fade-left" data-aos-delay="300"><a href="/details/?id=${response[each].news_id}">${response[each].title}</a></h6>
                <p class="news-time">${response[each].publishedAt}</p>
                <p>
                ${response[each].description}
                </p>
             </div>
          </div>
       </div>
                  `
            }

            $('#main_data_div').append(add_html)
            AOS.init({
               easing: 'ease-out-back',
               duration: 1000
            });
            // alert("this is sucesss")
            $('#page_no').val(page_no)
            isFetchingData = false
         },
         error: function(error) {
            console.log(error)
            alert("Please try after some time")
        },
   });
}
};


var appendcategory=function(){
   let page_no = Number($('#page_no').val())+1
   let total_page = $('#total_page').val()
   let category = $('#category_value').val()
   console.log("|:| ",category,page_no)

   if (Number(page_no)<=Number(total_page)){
      $.ajax({
         url: '/category/',
         type: 'GET',
         data: {
             'page': page_no,
             'category':category,
             'type':'json'
         },
         success: function(response) {
            console.log(response)
            var add_html=''
            for(let each= 0;each<response.length;each++){
               if([0,4,7,10].includes(each)){
                  add_html +=`<div class="row">`
               }
               
               let class_no
               switch(each) {
                  case 4:
                     class_no=6
                    break;
                  case 5:
                     class_no=3
                    break;
                  case 6:
                     class_no=3
                    break;
                  default:
                     class_no=4
                }
               add_html += ` 
               <div class="col-md-${class_no} news_card_col" data-aos="fade-up"  data-aos-delay="200">
               <a href="/details/?id=${response[each].news_id}">
                  <h5 class="fw-600 titlelinelimitation" data-aos="fade-right"  data-aos-delay="200" id="title${response[each].news_id}" >
                  ${response[each].title}
                  </h5>
                  <p data-aos="fade-right"  data-aos-delay="200" class="descriptionlinelimitation" >
                     ${response[each].description}
                  </p>
               </a>
               <div class="card_actions_col" data-aos="fade-right"  data-aos-delay="200">
                  <ul>
                     <li class="smile-icon-wrap">
                     <a href="javascript:void(0)" id="reaction_tag${response[each].news_id}">`
                     console.log(response[each].reaction_type)
                     if(response[each].reaction_type & response[each].reaction_type == 'NoData'){
                        add_html += `<i class="fa-regular fa-face-smile"></i>`
                     }
                     else if(response[each].reaction_type){
                        add_html += `<i class="fa-regular fa-face-smile"></i> 
                        <i class="fa-regular ${response[each].reaction_type}" onclick="delete_reaction('${response[each].news_id}')"></i> 
                        `
                     }

                     add_html +=`
                        <span class="fw-500" id="reaction_count${response[each].news_id}">${response[each].reaction_count}</span>
                        
                     </a>  
                     <div class="tooltip">
                        <i class="fa-regular fa-thumbs-up" onclick="send_reaction('fa-thumbs-up','${response[each].news_id}')"></i>
                        <i class="fa-regular fa-heart" onclick="send_reaction('fa-heart','${response[each].news_id}')"></i>
                        <i class="fa-regular fa-face-sad-cry" onclick="send_reaction('fa-face-sad-cry','${response[each].news_id}')"></i>
                        <i class="fa-regular fa-face-laugh-wink" onclick="send_reaction('fa-face-laugh-wink','${response[each].news_id}')"></i>
                        <i class="fa-regular fa-face-meh" onclick="send_reaction('fa-face-meh','${response[each].news_id}')"></i>
                        <i class="fa-regular fa-face-frown" onclick="send_reaction('fa-face-frown','${response[each].news_id}')"></i>
                        <i class="fa-regular fa-face-tired" onclick="send_reaction('fa-face-tired','${response[each].news_id}')"></i>
                     </div>                                  
                     </li>
                     <li>
                        <a href="javascript:void(0)" class="comment-icon" onclick="toggleOverlay('${response[each].news_id}')">
                           <i class="fa-regular fa-comment"></i>
                           <span class="fw-500" id="comnt_count${response[each].news_id}"> ${response[each].cmnt_count} </span>
                        </a>
                     </li>
                     <li>
                        <a href="javascript:void(0)" class="copy-icon" onclick="textcopied('/details/?id=${response[each].news_id}')">
                           <i class="fa-regular fa-share-from-square"></i>
                        </a>
                     </li>
                  </ul>
               </div>
            </div>
               `
               if([3,6,9,response.length].includes(each)){
                  add_html +=`</div>`
               }
            }

            $('#main_data_div').append(add_html)
            AOS.init({
               easing: 'ease-out-back',
               duration: 1000
            });
            // alert("this is sucesss")
            $('#page_no').val(page_no)
            isFetchingData = false
         },
         error: function(error) {
            console.log(error)
            alert("kkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
        },
   });
}
};


// Infniteloading for comments  

// $(document).ready(function(){
//    $(window).scroll(function(){
//       console.log('helloooo')

//    })
// })