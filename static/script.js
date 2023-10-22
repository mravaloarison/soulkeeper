// Initialize Firebase with your project's configuration
var config = {
    apiKey: "AIzaSyBtOIa2Wa9cBTdQ8mgRwt4dFbOV3egAnt8",
    authDomain: "soulkeeper-a0b72.firebaseapp.com",
    projectId: "soulkeeper-a0b72",
    storageBucket: "soulkeeper-a0b72.appspot.com",
    messagingSenderId: "734672571215",
    appId: "1:734672571215:web:7d263a080398934b64533a",
};
firebase.initializeApp(config);
// Add click event listener to Google Sign-In button
var googleSignInButton = document.getElementById("google-signin-button");
googleSignInButton.addEventListener("click", function() {
    var provider = new firebase.auth.GoogleAuthProvider();
    firebase.auth().signInWithPopup(provider)
        .then(function(result) {
            // Handle successful sign-in here
            var user = result.user;
            var email = user.email; // Get the user's email address
            var idToken = result.credential.idToken; // Get the user's ID token
            var uid = user.uid; // Get the user's unique User ID

            // Prepare the data to send to your Flask backend
            var userData = {
                email: email,
                idToken: idToken,
                uid: uid
            };

            // Send the data to your Flask backend using a POST request
            fetch("/login_in", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(userData)
            })
            .then(response => {
                if (response.ok) {
                    location.href = "/home";
                } else {
                    // Handle errors if needed
                }
            })
            .catch(error => {
                console.error("Error:", error);
            });
        })
        .catch(function(error) {
            // Handle sign-in errors here
            var errorCode = error.code;
            var errorMessage = error.message;
            console.log("Sign-in error:", errorCode, errorMessage);
        });
});




