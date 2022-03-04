const facebookBtn = document.querySelector(".facebook-btn");
const twitterBtn = document.querySelector(".twitter-btn");
const linkedinBtn = document.querySelector(".linkedin-btn");
const whatsappBtn = document.querySelector(".whatsapp-btn");

function init() {
  let postUrl = encodeURI(document.location.href);
  let postTitle = encodeURI("Hi everyone, please check this post on @iRead_Blog: ");

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
      id: id,
    },
    success: function (data) {
      var ele = document.getElementById("like_dislike");
      if (data.is_liked) {
        ele.className = "fa fa-thumbs-up";
        ele.innerHTML = ` ${data.total_likes}`;
      } else if (!data.is_liked) {
        ele.className = "fa fa-thumbs-o-up";
        ele.innerHTML = ` ${data.total_likes}`;
      } else {
        likeFeedBackArea.style.display = "block";
        likeFeedBackArea.innerHTML = `<p>${data.like_error}</p>`;
      }
    },
  });
});

function copyLink(link,) {
  Swal.fire({
    html:
      `<input id="text_to_be_copied" class="swal2-input" readonly value='${link}'>` +
      '<div class="linkFeedBackArea invalid-feedback" style="display: none"><p>Unable to shorten link</p></div>' +
      '<button type="button" class="btn btn-primary swal-confirm" style="margin-left:5px; margin-top: 5px;" id="btn-copy" >Copy Link</button>' +
      "</div>",
    showConfirmButton: false,
    type: "success",
    onOpen: () => {
      const linkFeedBackArea = document.querySelector(".linkFeedBackArea");
      linkFeedBackArea.style.display = "none";

      $("#btn-copy").click(() => {
        $("#text_to_be_copied").select();
        document.execCommand("copy");
        var btn = document.getElementById("btn-copy");
        btn.innerHTML = "Link Copied";
        btn.classList.remove("btn-primary");
        btn.classList.add("btn-success");
      });
    },
  });
}
