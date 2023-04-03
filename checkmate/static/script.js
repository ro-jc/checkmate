// function starPageOnly() {
//     document.getElementById("starPage").style.display = "block";
//     document.getElementById("groupPage").style.display = "none";
//     document.getElementById("friendPage").style.display = "none";
//     document.getElementById('starBtn').classList.add('bottomBarIcon-active');
//     document.getElementById('groupBtn').classList.remove('bottomBarIcon-active');
//     document.getElementById('friendBtn').classList.remove('bottomBarIcon-active');
// }

function showPreview(event) {
  if (event.target.files.length > 0) {
    var src = URL.createObjectURL(event.target.files[0]);
    var preview = document.getElementById("file-ip-1-preview");
    preview.src = src;
    preview.style.display = "block";
  }
}

function groupPageOnly() {
  document.getElementById("groupPage").style.display = "block";
  // document.getElementById("starPage").style.display = "none";
  document.getElementById("friendPage").style.display = "none";
  // document.getElementById('starBtn').classList.remove('bottomBarIcon-active');
  document.getElementById("groupBtn").classList.add("bottomBarIcon-active");
  document.getElementById("friendBtn").classList.remove("bottomBarIcon-active");
}
function friendPageOnly() {
  document.getElementById("friendPage").style.display = "block";
  document.getElementById("groupPage").style.display = "none";
  // document.getElementById("starPage").style.display = "none";
  // document.getElementById('starBtn').classList.remove('bottomBarIcon-active');
  document.getElementById("groupBtn").classList.remove("bottomBarIcon-active");
  document.getElementById("friendBtn").classList.add("bottomBarIcon-active");
}

function openNav() {
  document.getElementById("mySidenav").style.width = "100vw";
  document.getElementById("main").style.marginRight = "100vw";
}

function closeNav() {
  document.getElementById("mySidenav").style.width = "0";
  document.getElementById("main").style.marginRight = "0";
}

vhpx = document.documentElement.clientHeight;
function scrollDown() {
  window.scrollBy(0, vhpx);
}
function scrollUp() {
  window.scrollBy(0, -vhpx);
}

function uNameDone() {
  document.getElementById("setUser").style.display = "none";
  document.getElementById("setPswd").style.display = "flex";
  document.getElementById("setName").style.display = "none";
  document.getElementById("setMail").style.display = "none";
  document.getElementById("setTT").style.display = "none";
}

function pswdDone() {
  document.getElementById("setUser").style.display = "none";
  document.getElementById("setPswd").style.display = "none";
  document.getElementById("setName").style.display = "flex";
  document.getElementById("setMail").style.display = "none";
  document.getElementById("setTT").style.display = "none";
  document.getElementById("selectImgBtn").style.display = "block";
  document.getElementById("file-ip-1-preview").style.background = "white";
}

function nameDone() {
  document.getElementById("setUser").style.display = "none";
  document.getElementById("setPswd").style.display = "none";
  document.getElementById("setName").style.display = "none";
  document.getElementById("setMail").style.display = "flex";
  document.getElementById("setTT").style.display = "none";
}

function mailDone() {
  document.getElementById("setUser").style.display = "none";
  document.getElementById("setPswd").style.display = "none";
  document.getElementById("setName").style.display = "none";
  document.getElementById("setMail").style.display = "none";
  document.getElementById("setTT").style.display = "flex";
}


function pswdPrev(){
  document.getElementById("setUser").style.display = "flex";
  document.getElementById("setPswd").style.display = "none";
  document.getElementById("setName").style.display = "none";
  document.getElementById("setMail").style.display = "none";
  document.getElementById("setTT").style.display = "none";
}
function NamePrev() {
  document.getElementById("setUser").style.display = "none";
  document.getElementById("setPswd").style.display = "flex";
  document.getElementById("setName").style.display = "none";
  document.getElementById("setMail").style.display = "none";
  document.getElementById("setTT").style.display = "none";
}
function mailPrev() {
  document.getElementById("setUser").style.display = "none";
  document.getElementById("setPswd").style.display = "none";
  document.getElementById("setName").style.display = "flex";
  document.getElementById("setMail").style.display = "none";
  document.getElementById("setTT").style.display = "none";
}

function TTPrev(){
  document.getElementById("setUser").style.display = "none";
  document.getElementById("setPswd").style.display = "none";
  document.getElementById("setName").style.display = "none";
  document.getElementById("setMail").style.display = "flex";
  document.getElementById("setTT").style.display = "none";
}