function change() {
    document.getElementById("heading").innerHTML = "Welcome to Cricket!";

    document.getElementById("changeBtn").innerHTML = "Changed";
    document.getElementById("changeBtn").style.backgroundColor = "green";
    console.log("Button clicked");
    history.pushState({ page: "cricket" }, "Cricket", "cricket.html");
}