const emailField = document.querySelector("#email");
const emailFeedBackArea = document.querySelector(".emailFeedBackArea");
const loginBtn = document.querySelector("#loginBtn");
const password = document.querySelector("#password");
const togglePassword = document.querySelector("#togglePassword");

emailField.addEventListener("keyup", (e) => {
  const emailVal = e.target.value;

  emailField.classList.remove("is-invalid");
  emailFeedBackArea.style.display = "none";

  if (emailVal.length > 0) {
    $.ajax({
      url: "/accounts/find-email",
      type: "GET",
      data: {
        email: emailVal,
      },
      success: function (data) {
        if (data.email_error) {
          loginBtn.disabled = true;
          emailField.classList.add("is-invalid");
          emailFeedBackArea.style.display = "block";
          emailFeedBackArea.innerHTML = `<p>${data.email_error}</p>`;
        } else {
          emailField.classList.remove("is-invalid");
          emailFeedBackArea.style.display = "none";
          loginBtn.removeAttribute("disabled");
        }
      },
    });
  }
});

togglePassword.addEventListener("click", function (e) {
  // toggle the type attribute
  const type =
    password.getAttribute("type") === "password" ? "text" : "password";
  password.setAttribute("type", type);
  // toggle the eye slash icon
  this.classList.toggle("fa-eye-slash");
});
