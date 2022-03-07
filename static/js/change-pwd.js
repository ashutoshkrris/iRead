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
        if (data.password_error) {
          checkPasswordBtn.innerHTML = "Check Password";
          oldPasswordField.classList.add("is-invalid");
          oldPasswordFeedBackArea.style.display = "block";
          oldPasswordFeedBackArea.innerHTML = `<p>Incorrect Password</p>`;
        } else {
          oldPasswordFeedBackArea.style.display = "none";
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
          newPassword1FeedBackArea.style.display = "none";
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
          newPassword2FeedBackArea.style.display = "none";
          changePasswordBtn.removeAttribute("disabled");
        }
      });
  }
});


const togglePassword1 = document.querySelector("#togglePassword1");
const togglePassword2 = document.querySelector("#togglePassword2");
const togglePassword3 = document.querySelector("#togglePassword3");

togglePassword1.addEventListener("click", function (e) {
  // toggle the type attribute
  const type =
    oldPasswordField.getAttribute("type") === "password" ? "text" : "password";
  oldPasswordField.setAttribute("type", type);
  // toggle the eye slash icon
  this.classList.toggle("fa-eye-slash");
});

togglePassword2.addEventListener("click", function (e) {
  // toggle the type attribute
  const type =
    password1Field.getAttribute("type") === "password" ? "text" : "password";
  password1Field.setAttribute("type", type);
  // toggle the eye slash icon
  this.classList.toggle("fa-eye-slash");
});

togglePassword3.addEventListener("click", function (e) {
  // toggle the type attribute
  const type =
    password2Field.getAttribute("type") === "password" ? "text" : "password";
  password2Field.setAttribute("type", type);
  // toggle the eye slash icon
  this.classList.toggle("fa-eye-slash");
});