const banner = document.querySelector("#bannerid");

window.addEventListener("scroll", () => {
    const banner = document.querySelector("#bannerid")
    const currentScroll = window.pageYOffset;
    if (currentScroll > 100) {
        banner.classList.add("hidden");
        console.log(currentScroll);
    }
})