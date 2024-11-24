const eye = document.querySelector(".bi-eye");
eye.classList.add("none");
// const passwordInput = document.querySelector("#password");
// passwordInput.type = 'password';

document.querySelector(".icon").addEventListener("click", function () {
  const passwordInput = document.querySelector("#password");
  const passwordToggle = document.querySelector(".bi-eye-slash");

  if (passwordInput.type == "password") {
    passwordInput.type = "text";
    passwordToggle.classList.add("none");
    eye.classList.remove("none");
  } else {
    passwordInput.type = "password";
    passwordToggle.classList.remove("none");
    eye.classList.add("none");
  }
});
