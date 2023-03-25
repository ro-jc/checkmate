function starPageOnly() {
    document.getElementById("starPage").style.display = "block";
    document.getElementById("groupPage").style.display = "none";
    document.getElementById("friendPage").style.display = "none";
    document.getElementById('starBtn').classList.add('bottomBarIcon-active');
    document.getElementById('groupBtn').classList.remove('bottomBarIcon-active');
    document.getElementById('friendBtn').classList.remove('bottomBarIcon-active');
}
function groupPageOnly() {
    document.getElementById("groupPage").style.display = "block";
    document.getElementById("starPage").style.display = "none";
    document.getElementById("friendPage").style.display = "none";
    document.getElementById('starBtn').classList.remove('bottomBarIcon-active');
    document.getElementById('groupBtn').classList.add('bottomBarIcon-active');
    document.getElementById('friendBtn').classList.remove('bottomBarIcon-active');
}
function friendPageOnly() {
    document.getElementById("friendPage").style.display = "block";
    document.getElementById("groupPage").style.display = "none";
    document.getElementById("starPage").style.display = "none";
    document.getElementById('starBtn').classList.remove('bottomBarIcon-active');
    document.getElementById('groupBtn').classList.remove('bottomBarIcon-active');
    document.getElementById('friendBtn').classList.add('bottomBarIcon-active');
}

function openNav() {
    document.getElementById("mySidenav").style.width = "20vw";
}

function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
}

