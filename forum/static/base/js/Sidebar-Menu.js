let windowStatus = 1;
$("#menu-toggle").click(function (e) {
    e.preventDefault();
    $("#wrapper").toggleClass("toggled");
    const sidebar = document.getElementById("sidebar-wrapper");
    const nav = document.getElementById("navcol-1");
    if (nav.offsetHeight !== 0) {
        document.getElementById("navbartoggler").click();
    }
    if (sidebar.offsetWidth === 0) {
        document.getElementById("main").style.opacity = "0.5";
    } else {
        document.getElementById("main").style.opacity = "1";
    }
});

$("#navbartoggler").click(function (e) {
    const sidebar = document.getElementById("sidebar-wrapper");
    const nav = document.getElementById("navcol-1");
    if (sidebar.offsetWidth !== 0) {
        document.getElementById("menu-toggle").click();
    }
    if (nav.offsetHeight === 0) {
        $("#nav-bar").animate({height: 150});
        document.getElementById("main").style.opacity = "0.5";
    } else {
        $("#nav-bar").animate({height: 70});
        document.getElementById("main").style.opacity = "1";
    }
})

function showSidebar() {
    const sidebar = document.getElementById("sidebar-wrapper");
    const nav = document.getElementById("navcol-1");
    const width = Number(window.innerWidth);
    //console.log(windowStatus);
    if (width >= 768) {
        if (sidebar.offsetWidth === 0) {
            $("#wrapper").toggleClass("toggled");
        }
        if (nav.offsetWidth !== 0 && windowStatus === 0) {
            document.getElementById("navbartoggler").click();
        }
        windowStatus = 1;
        document.getElementById("main").style.opacity = "1";
    } else {
        if (windowStatus === 1 && nav.offsetHeight === 78) {
            document.getElementById("navbartoggler").click();
        }
        if (nav.offsetWidth !== 0)
            windowStatus = 0;

    }
}

window.addEventListener("resize", showSidebar);
