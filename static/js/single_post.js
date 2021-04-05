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
      id: id,
    },
    success: function (data) {
      console.log(data);
      var ele = document.getElementById("like_dislike");
      console.log(ele);
      if (data.is_liked == true) {
        ele.className = "fa fa-thumbs-up";
        ele.innerHTML = ` ${data.total_likes}`;
      } else if (data.is_liked == false) {
        ele.className = "fa fa-thumbs-o-up";
        ele.innerHTML = ` ${data.total_likes}`;
      } else {
        likeFeedBackArea.style.display = "block";
        likeFeedBackArea.innerHTML = `<p>${data.like_error}</p>`;
      }
    },
  });
});

function copyLink(link, api_key) {
  Swal.fire({
    html:
      `<input id="text_to_be_copied" class="swal2-input" readonly value='${link}'>` +
      '<div class="linkFeedBackArea invalid-feedback" style="display: none"><p>Unable to shorten link</p></div>' +
      '<button type="button" class="btn btn-primary swal-confirm" style="margin-left:5px; margin-top: 5px;" id="btn-copy" >Copy Link</button>' +
      '<button type="button" class="btn btn-success swal-confirm" style="margin-left:15px; margin-top: 5px;" id="btn-shorten">Shorten Link</button>' +
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
        document.getElementById("btn-shorten").classList.remove("btn-success");
        document.getElementById("btn-shorten").classList.add("btn-primary");
      });

      $("#btn-shorten").click(() => {
        fetch("https://srty.me/api/shorten/", {
          body: JSON.stringify({
            api_key: api_key,
            original: link,
          }),
          method: "POST",
        })
          .then((res) => res.json())
          .then((data) => {
            if (data.error) {
              linkFeedBackArea.style.display = "block";
            } else {
              document.getElementById("text_to_be_copied").value = data.short;
              document.getElementById("btn-shorten").style.display = "none";
              document
                .getElementById("btn-copy")
                .style.removeProperty("margin-left");
              document.getElementById("btn-copy").innerHTML = 'Copy Link'
            }
          });
      });
    },
  });
}
