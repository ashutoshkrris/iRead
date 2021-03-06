const facebookBtn = document.querySelector(".facebook-btn");
const twitterBtn = document.querySelector(".twitter-btn");
const linkedinBtn = document.querySelector(".linkedin-btn");
const whatsappBtn = document.querySelector(".whatsapp-btn");


function init() {
  let postUrl = encodeURI(document.location.href);
  let postTitle = encodeURI("Hi everyone, please check this post on iRead: ");

  facebookBtn.setAttribute(
    "href",
    `https://www.facebook.com/sharer.php?u=${postUrl}`
  );

  twitterBtn.setAttribute(
    "href",
    `https://twitter.com/share?url=${postUrl}&text=${postTitle}`
  );

  linkedinBtn.setAttribute(
    "href",
    `https://www.linkedin.com/sharing/share-offsite/?url=${postUrl}`
  );

  whatsappBtn.setAttribute(
    "href",
    `https://wa.me/?text=${postTitle} ${postUrl}`
  );
}

init();

$(".like").click(function (e) {
  const likeFeedBackArea = document.querySelector(".likeFeedBackArea");
  var id = this.id;
  var href = $(".like").find("a").attr("href");
  e.preventDefault();
  $.ajax({
    url: href,
    data: {
      'id': id
    },
    success: function (data) {
      console.log(data)
      var ele = document.getElementById("like_dislike");
      console.log(ele)
      if (data.is_liked == true) {
        ele.className = "fa fa-thumbs-up"
        ele.innerHTML = ` ${data.total_likes}`
      } else if(data.is_liked == false) {
        ele.className = "fa fa-thumbs-o-up";
        ele.innerHTML = ` ${data.total_likes}`;
      } else {
        likeFeedBackArea.style.display = "block";
        likeFeedBackArea.innerHTML = `<p>${data.like_error}</p>`;
      }
    }
  })
})