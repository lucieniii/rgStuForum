let windowStatus = 1;

function handler() {
    const width = Number(window.innerWidth);
    const avatarBox = document.getElementById("avatarBox");
    const flexButtons = document.getElementsByClassName("flex-button");
    const commentAvatars = document.getElementsByClassName("CommentAvatar");
    const bodyHeight = window.innerHeight;
    const bodyWidth = window.innerWidth;
    document.getElementById("reply-button").style.left = bodyWidth - 100 + "px";
    document.getElementById("return-button").style.left = bodyWidth - 180 + "px";
    if (width >= 1440) {
        avatarBox.style.minWidth = "150px";
        avatarBox.style.maxWidth = "150px";
        Array.prototype.forEach.call(commentAvatars, function (el) {
            el.style.minWidth = "150px";
            el.style.maxWidth = "150px";
        });
        Array.prototype.forEach.call(flexButtons, function (el) {
            el.style.width = "60px";
            el.style.height = "60px";
            el.style.fontSize = "2em";
            el.style.top = bodyHeight - 100 + "px";
        });
        //document.getElementById("avatarBox").style.fontSize = "1rem";
        document.getElementById("titleWrapper").style.fontSize = "1rem";
    } else if (width < 375) {
        avatarBox.style.minWidth = "80px";
        avatarBox.style.maxWidth = "80px";
        Array.prototype.forEach.call(commentAvatars, function (el) {
            el.style.minWidth = "80px";
            el.style.maxWidth = "80px";
        });
        Array.prototype.forEach.call(flexButtons, function (el) {
            el.style.width = "40px";
            el.style.height = "40px";
            el.style.fontSize = "2em";
            el.style.top = bodyHeight - 100 + "px";
        });
        //document.getElementById("avatarBox").style.fontSize = "0.8rem";
        document.getElementById("titleWrapper").style.fontSize = "0.8rem";
    } else {
        w = (width - 375) / 1065 * 70 + 80;
        r = (width - 375) / 1065 * 0.2 + 0.8;
        d = (width - 375) / 1065 * 20 + 40;
        dr = (width - 375) / 1065 + 1;
        avatarBox.style.minWidth = w + "px";
        avatarBox.style.maxWidth = w + "px";
        Array.prototype.forEach.call(commentAvatars, function (el) {
            el.style.minWidth = w + "px";
            el.style.maxWidth = w + "px";
        });
        Array.prototype.forEach.call(flexButtons, function (el) {
            el.style.width = d + "px";
            el.style.height = d + "px";
            el.style.fontSize = dr + "em";
            el.style.top = bodyHeight - 100 + "px";
        });
        //document.getElementById("avatarBox").style.fontSize = r + "rem";
        document.getElementById("titleWrapper").style.fontSize = r + "rem";
    }
    const nav = document.getElementById("navcol-1");
    //console.log(windowStatus);
    if (width >= 768) {
        if (nav.offsetWidth !== 0 && windowStatus === 0) {
            document.getElementById("navbartoggler").click();
        }
        windowStatus = 1;
        document.getElementById("titleWrapper").style.opacity = "1";
    } else {
        if (windowStatus === 1 && nav.offsetHeight === 78) {
            document.getElementById("navbartoggler").click();
        }
        if (nav.offsetWidth !== 0)
            windowStatus = 0;
    }
}

window.addEventListener("resize", handler);
$("#navbartoggler").click(function (e) {
    const nav = document.getElementById("navcol-1");
    if (nav.offsetHeight === 0) {
        $("#nav-bar").animate({height: 150});
        document.getElementById("titleWrapper").style.opacity = "0.5";
    } else {
        $("#nav-bar").animate({height: 70});
        document.getElementById("titleWrapper").style.opacity = "1";
    }
})

/*
window.addEventListener('scroll', function (e) {
    const bodyHeight = window.innerHeight;
    const bodyWidth = window.innerWidth;
    const flexButtons = document.getElementsByClassName("flex-button");
    document.getElementById("reply-button").style.left = bodyWidth - 100 + "px";
    Array.prototype.forEach.call(flexButtons, function (el) {
        el.style.top = bodyHeight - 100 + "px";
    });
});*/