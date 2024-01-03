document.addEventListener("DOMContentLoaded", function () {
    const passwordInput = document.getElementById("passwordInput");
    const eyeIcon = document.getElementById("eyeIcon");
  
    eyeIcon.addEventListener("click", function () {
      if (passwordInput.type === "password") {
        passwordInput.type = "text";
        eyeIcon.classList.remove("fa-eye");
        eyeIcon.classList.add("fa-eye-slash");
      } else {
        passwordInput.type = "password";
        eyeIcon.classList.remove("fa-eye-slash");
        eyeIcon.classList.add("fa-eye");
      }
    });
  });

  
document.querySelector('.copy-icon').addEventListener('click', function() {
    var textToCopy = this.getAttribute('data-copy-text');

    var inputElement = document.createElement('input');
    inputElement.setAttribute('value', textToCopy);
    document.body.appendChild(inputElement);

    inputElement.select();
    document.execCommand('copy');

    document.body.removeChild(inputElement);
});


function toggleOverlay(news_id) {
    add_comments(news_id)
    document.getElementById("commentOverlay").style.display = "block";
    document.body.style.overflow = 'hidden';
    document.getElementById("overlay").style.zIndex = 9;
    document.getElementById("overlay").style.backgroundColor = 'rgba(0,0,0,0.7)';
    document.getElementById("overlay").style.visibility = 'visible';
    document.getElementById("overlay").style.opacity = 1;
    
}

function off() {
    document.getElementById("commentOverlay").style.display = "none";
    document.body.style.overflow = 'auto';
    document.getElementById("overlay").style.zIndex = 0;
    document.getElementById("overlay").style.backgroundColor = '#fff';
    document.getElementById("overlay").style.visibility = 'hidden';
    document.getElementById("overlay").style.opacity = 0;
  }



function news_search(){
    query = $('#news_search_bar').val()
    window.location.replace(`/search/?q=${query}`);
}


function delayedFunction() {
    var myDiv = document.getElementById('notification_shown');
    if (myDiv) {
      myDiv.style.display = 'none';
    }
  }


