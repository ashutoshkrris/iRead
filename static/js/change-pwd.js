const oldPasswordField = document.querySelector("#oldPassword");
const oldPasswordFeedBackArea = document.querySelector(
  ".oldPasswordFeedBackArea"
);
const checkPasswordBtn = document.querySelector("#checkPasswordBtn");
const password1Field = document.querySelector("#newPassword1");
const newPassword1FeedBackArea = document.querySelector(
  ".newPassword1FeedBackArea"
);
const password2Field = document.querySelector("#newPassword2");
const newPassword2FeedBackArea = document.querySelector(
  ".newPassword2FeedBackArea"
);
const changePasswordBtn = document.querySelector("#changePasswordBtn");

// Functions
function checkPwd() {
  checkPasswordBtn.innerHTML =
    '<div class="spinner-border text-light" role="status"><span class="sr-only">Loading...</span></div>';

  let oldPasswordVal = $("#oldPassword").val();

  if (oldPasswordVal.length > 0) {
    fetch("/accounts/check-passwords/", {
      body: JSON.stringify({ oldPassword: oldPasswordVal }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
        if (data.password_error) {
          checkPasswordBtn.innerHTML = "Check Password";
          oldPasswordField.classList.add("is-invalid");
          oldPasswordFeedBackArea.style.display = "block";
          oldPasswordFeedBackArea.innerHTML = `<p>Incorrect Password</p>`;
        } else {
          checkPasswordBtn.removeAttribute("disabled");
          $("#beforeOldPassword").hide();
          checkPasswordBtn.hidden = true;
          $("#afterOldPassword").fadeIn(1000);
        }
      });
  }
}

password1Field.addEventListener("keyup", (e) => {
  const password1Val = e.target.value;

  password1Field.classList.remove("is-invalid");
  newPassword1FeedBackArea.style.display = "none";

  if (password1Val.length > 0) {
    fetch("/accounts/validate-password/", {
      body: JSON.stringify({
        password1: password1Val,
      }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.password_error) {
          changePasswordBtn.disabled = true;
          password1Field.classList.add("is-invalid");
          newPassword1FeedBackArea.style.display = "block";
          newPassword1FeedBackArea.innerHTML = `<p>${data.password_error}</p>`;
        } else {
          changePasswordBtn.removeAttribute("disabled");
        }
      });
  }
});

password2Field.addEventListener("keyup", (e) => {
  const passwordVal = e.target.value;
  const password1Val = document.getElementById("newPassword1").value;

  password2Field.classList.remove("is-invalid");
  newPassword2FeedBackArea.style.display = "none";

  if (passwordVal.length > 0) {
    fetch("/accounts/match-passwords/", {
      body: JSON.stringify({
        password1: password1Val,
        password2: passwordVal,
      }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.password_mismatch) {
          changePasswordBtn.disabled = true;
          password2Field.classList.add("is-invalid");
          newPassword2FeedBackArea.style.display = "block";
          newPassword2FeedBackArea.innerHTML = `<p>${data.password_mismatch}</p>`;
        } else {
          changePasswordBtn.removeAttribute("disabled");
        }
      });
  }
});