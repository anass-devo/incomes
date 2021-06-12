const usernamefield = document.querySelector("#usernamefield");
const emailfield = document.querySelector("#emailfield");
const passwordfield = document.querySelector("#passwordfield");
const feedbackArea = document.querySelector(".invalid_feedback");
const EmailfeedbackArea = document.querySelector(".invalidemail_feedback");
const usernameSuccessOutput = document.querySelector(".usernameSuccessOutput");
const showpassword = document.querySelector(".showpassword");
const submitbtn = document.querySelector("#submit-btn");

showpassword.addEventListener("click", (e) => {
    console.log("8888888", 888888);

    if (showpassword.textContent === "SHOW") {
        showpassword.textContent = "HIDE";
        passwordfield.setAttribute("type", "text");
    } else {
        showpassword.textContent = "SHOW";
        passwordfield.setAttribute("type", "password");
    }
});







emailfield.addEventListener("keyup", (e) => {
    console.log("4444", 4444);
    
    const emailval = e.target.value;
    emailfield.classList.remove("is-invalid");
    EmailfeedbackArea.style.display = "none";

    if (emailval.length > 0) {
        fetch("/authentication/validate-email", {
            body: JSON.stringify({ email: emailval }),
            method: "POST",
        })
            .then(res => res.json())
            .then(data => {
                console.log("data", data);
                if (data.email_error) {
                    submitbtn.disabled=true;
                    emailfield.classList.add("is-invalid");
                    EmailfeedbackArea.innerHTML = data.email_error;
                    EmailfeedbackArea.style.display = "block";
                } else {
                    submitbtn.removeAttribute("disabled");
                }

            });

    }


});



usernamefield.addEventListener("keyup", (e) => {
    console.log("777777", 77777);

    const usernameval = e.target.value;
    usernameSuccessOutput.style.display = "block";
    usernameSuccessOutput.textContent = "Checking....";

    usernamefield.classList.remove("is-invalid");
    feedbackArea.style.display = "none";

    if (usernameval.length > 0) {
        fetch("/authentication/validate-username", {
            body: JSON.stringify({ username: usernameval }),
            method: "POST",
        })
            .then(res => res.json())
            .then(data => {
                console.log("data", data);
                usernameSuccessOutput.style.display = "none";
                if (data.Username_error) {
                    submitbtn.disabled=true;
                    usernamefield.classList.add("is-invalid");
                    feedbackArea.innerHTML = data.Username_error;
                    feedbackArea.style.display = "block";
                } else {
                    submitbtn.removeAttribute("disabled");
                }

            });

    }

    
});