if ("serviceWorker" in navigator) {
  navigator.serviceWorker.register("/sw.js", { scope: "/" });
}

function showPreview(event) {
  if (event.target.files.length > 0) {
    var src = URL.createObjectURL(event.target.files[0]);
    var preview = document.getElementById("file-ip-1-preview");
    preview.src = src;
    preview.style.display = "block";
  }
}

function groupPageOnly() {
  document.getElementById("groupsPage").style.display = "flex";
  document.getElementById("friendsPage").style.display = "none";
  document.getElementById("groupBtn").classList.add("bottomBarIcon-active");
  document.getElementById("friendBtn").classList.remove("bottomBarIcon-active");
}

function friendPageOnly() {
  document.getElementById("friendsPage").style.display = "flex";
  document.getElementById("groupsPage").style.display = "none";
  document.getElementById("groupBtn").classList.remove("bottomBarIcon-active");
  document.getElementById("friendBtn").classList.add("bottomBarIcon-active");
}

function openNav() {
  document.getElementById("mySidenav").style.width = "80vw";
  document.getElementById("main").style.marginLeft = "80vw";
}

function closeNav() {
  document.getElementById("mySidenav").style.width = "0";
  document.getElementById("main").style.marginLeft = "0";
}

vhpx = document.documentElement.clientHeight;

function scrollDown() {
  window.scrollBy(0, vhpx);
}

function scrollUp() {
  window.scrollBy(0, -vhpx);
}

const divs = ["setUser", "setPswd", "setName", "setMail", "setTT"];

function setNextVisibility(myDiv) {
  let i = 0;
  for (; i < divs.length; i++) {
    document.getElementById(divs[i]).style.display = "none";
    if (divs[i] == myDiv) {
      document.getElementById(divs[i + 1]).style.display = "flex";
      break;
    }
  }
}

function moveForward(myDiv) {
  if (["setUser", "setMail"].includes(myDiv)) {
    const id = myDiv == "setUser" ? "uname" : "mail";

    if (!document.getElementById(id).value) {
      document.getElementById(id + "Error").innerHTML = "field cannot be empty";
    } else {
      let xhttp = new XMLHttpRequest();
      xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
          const response = JSON.parse(xhttp.response);
          document.getElementById(id + "Error").innerHTML = response["error"];
          setNextVisibility(myDiv);
        }
      };
      xhttp.open("POST", "/signup/validate");
      xhttp.setRequestHeader(
        "Content-type",
        "application/x-www-form-urlencoded"
      );
      xhttp.send(id + "=" + data);
    }
  } else if (myDiv == "setPswd") {
    const pswd = document.getElementById("pswd").value;
    const rePswd = document.getElementById("rePswd").value;
    if (pswd != rePswd) {
      document.getElementById("pswdError").innerHTML = "passwords don't match!";
    } else if (!pswd) {
      document.getElementById("pswdError").innerHTML = "fields cannot be empty";
    } else {
      document.getElementById("pswdError").innerHTML = "";
      setNextVisibility(myDiv);
    }
  } else {
    setNextVisibility(myDiv);
  }
}

function moveBack(myDiv) {
  document.getElementById(myDiv).style.display = "none";
  for (let i = 0; i < divs.length; i++) {
    if (divs[i] == myDiv) {
      document.getElementById(divs[i - 1]).style.display = "flex";
      break;
    }
  }
}

function requestSend(username) {
  let xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      let element = document.getElementById(username);
      element.innerHTML = "Sent";
    }
  };

  xhttp.open("GET", "/requests/send/" + username);
  xhttp.send();
}

function requestReturn(username, action) {
  let xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById(username).remove();
    }
  };

  xhttp.open("POST", "/requests/return");
  xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhttp.send("username=" + username + "&action=" + action);
}

$(document).on("pagecreate", function () {
  $("#foo").on("click", function () {
    var closeBtn = $(
      '<a href="#" data-rel="back" class="ui-btn-right ui-btn ui-btn-b ui-corner-all ui-btn-icon-notext ui-icon-delete ui-shadow">Close</a>'
    );
    var content =
      "<p>Lorem ipsum dolor sit amet, consectetur adipiscing. Morbi convallis sem et dui sollicitudin tincidunt.</p>";
    var popup = $("<div/>", {
      "data-role": "popup",
    })
      .css({
        width: $(window).width() / 2.5 + "px",
        padding: 5 + "px",
      })
      .append(closeBtn)
      .append(content);
    $.mobile.pageContainer.append(popup);
    $("[data-role=popup]")
      .popup({
        dismissible: false,
        history: false,
        theme: "b",
        positionTo: "window",
        overlayTheme: "b",
        transition: "pop",
        beforeposition: function () {
          $.mobile.pageContainer
            .pagecontainer("getActivePage")
            .addClass("blur-filter");
        },
        afterclose: function () {
          $(this).remove();
          $(".blur-filter").removeClass("blur-filter");
        },
      })
      .popup("open");
  });
});
