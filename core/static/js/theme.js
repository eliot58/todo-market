function themeChange() {
    if (localStorage.getItem('theme') == 'light') {
        document.querySelector(".auth_tab.active").style.backgroundColor = "#00A550"
        localStorage.removeItem("theme")
        const lights = document.querySelectorAll(".light")
        for (let light of lights) {
            light.classList.remove("light")
            light.classList.add("dark")
        }

        document.querySelector('.profile-icon').src = '/static/img/profile.svg';
        try {
            document.querySelector('.orders-icon').src = '/static/img/orders.svg';
        } catch (_) {
            console.log("orders not fount")
        }
        document.querySelector('.works-icon').src = '/static/img/works.svg';
        // document.querySelector('.archive-icon').src = '/static/img/archive.svg';
        document.querySelector('.help-icon').src = '/static/img/help.svg';

        try {
            document.querySelector('.moon-icon').src = '/static/img/moon.svg';
        } catch (_) {
            console.log("moon not found")
        }
        try {
            document.querySelector('.user-icon').src = '/static/img/user.svg';
        } catch (_) {
            console.log("user not found")
        }
        try {
            if (window.location.pathname == '/cart/') {
                document.querySelector('.cart-icon').src = '/static/img/cart-active.svg';
            } else {
                document.querySelector('.cart-icon').src = '/static/img/cart.svg';
            }

        } catch (_) {
            console.log("cart not found")
        }

        try {
            document.querySelector('.target-icon').src = '/static/img/target.svg';
        } catch (_) {
            console.log("target not found")
        }

        try {
            document.querySelector('.earth-icon').src = '/static/img/earth.svg';
        } catch (_) {
            console.log("earth not found")
        }

        try {
            document.querySelector('.search-icon').src = '/static/img/search.svg';
        } catch (_) {
            console.log("search not found")
        }

        try {
            document.querySelector('.truck-icon').src = '/static/img/truck.svg';
        } catch (_) {
            console.log("truck not found")
        }

        try {
            document.querySelector('.star-icon').src = '/static/img/star.svg';
        } catch (_) {
            console.log("star not found")
        }

        try {
            for (const deals of document.querySelectorAll('.success_deal')) {
                deals.src = '/static/img/success_deal.png';
            }
        } catch (_) {
            console.log("deals not found")
        }

        try {
            for (const close of document.querySelectorAll('.close-icon')) {
                close.src = '/static/img/close.svg';
            }
        } catch (_) {
            console.log("close not found")
        }

        try {
            for (const upload of document.querySelectorAll('.upload-icon')) {
                upload.src = '/static/img/upload.png';
            }
        } catch (_) {
            console.log("upload not found")
        }

        try {
            document.querySelector('.signup-img').src = '/static/img/signup.png';
        } catch (_) {
            console.log("signup not found")
        }

        try {
            document.querySelector('.delivery').src = '/static/img/delivery.png';
        } catch (_) {
            console.log("delivery not found")
        }

        try {
            document.querySelector('.location-img').src = '/static/img/location.svg';
        } catch (_) {
            console.log("location not found")
        }

        try {
            document.querySelector('.clip-img').src = '/static/img/clip.svg';
        } catch (_) {
            console.log("clip not found")
        }

        document.querySelector('.logo').src = '/static/img/logo.svg';


    } else {
        document.querySelector(".auth_tab.active").style.backgroundColor = "#2094AD"
        const darks = document.querySelectorAll(".dark")
        for (let dark of darks) {
            dark.classList.remove("dark")
            dark.classList.add("light")
        }

        document.querySelector('.profile-icon').src = '/static/img/light-profile.svg';
        try {
            document.querySelector('.orders-icon').src = '/static/img/light-orders.svg';
        } catch (_) {
            console.log("orders not found")
        }
        document.querySelector('.works-icon').src = '/static/img/light-works.svg';
        // document.querySelector('.archive-icon').src = '/static/img/light-archive.svg';
        document.querySelector('.help-icon').src = '/static/img/light-help.svg';

        try {
            document.querySelector('.moon-icon').src = '/static/img/light-moon.svg';
        } catch (_) {
            console.log("moon not found")
        }
        try {
            document.querySelector('.user-icon').src = '/static/img/light-user.svg';
        } catch (_) {
            console.log("user not found")
        }
        try {
            if (window.location.pathname == '/cart/') {
                document.querySelector('.cart-icon').src = '/static/img/light-cart-active.svg';
            } else {
                document.querySelector('.cart-icon').src = '/static/img/light-cart.svg';
            }
        } catch (_) {
            console.log("cart not found")
        }

        try {
            document.querySelector('.target-icon').src = '/static/img/light-target.svg';
        } catch (_) {
            console.log("target not found")
        }

        try {
            document.querySelector('.earth-icon').src = '/static/img/light-earth.svg';
        } catch (_) {
            console.log("earth not found")
        }

        try {
            document.querySelector('.search-icon').src = '/static/img/light-search.svg';
        } catch (_) {
            console.log("search not found")
        }

        try {
            document.querySelector('.truck-icon').src = '/static/img/light-truck.svg';
        } catch (_) {
            console.log("truck not found")
        }

        try {
            document.querySelector('.star-icon').src = '/static/img/light-star.svg';
        } catch (_) {
            console.log("star not found")
        }

        try {
            for (const deals of document.querySelectorAll('.success_deal')) {
                deals.src = '/static/img/success_deal_light.png';
            }
        } catch (_) {
            console.log("deals not found")
        }

        try {
            for (const close of document.querySelectorAll('.close-icon')) {
                close.src = '/static/img/light-close.svg';
            }
        } catch (_) {
            console.log("close not found")
        }

        try {
            for (const upload of document.querySelectorAll('.upload-icon')) {
                upload.src = '/static/img/light-upload.png';
            }
        } catch (_) {
            console.log("upload not found")
        }

        try {
            document.querySelector('.signup-img').src = '/static/img/light-signup.png';
        } catch (_) {
            console.log("signup not found")
        }

        try {
            document.querySelector('.delivery').src = '/static/img/delivery-light.png';
        } catch (_) {
            console.log("delivery not found")
        }

        try {
            document.querySelector('.location-img').src = '/static/img/light-location.svg';
        } catch (_) {
            console.log("location not found")
        }

        try {
            document.querySelector('.clip-img').src = '/static/img/light-clip.svg';
        } catch (_) {
            console.log("clip not found")
        }

        document.querySelector('.logo').src = '/static/img/logo-light.png';

        localStorage.setItem("theme", "light")

    }
}

document.addEventListener('DOMContentLoaded', function () {

    if (localStorage.getItem('theme') == 'light') {
        localStorage.removeItem("theme")
        const darks = document.querySelectorAll(".dark")
        for (let dark of darks) {
            dark.classList.remove("dark")
            dark.classList.add("light")
        }

        document.querySelector('.profile-icon').src = '/static/img/light-profile.svg';
        try {
            document.querySelector('.orders-icon').src = '/static/img/light-orders.svg';
        } catch (_) {
            console.log("orders not found")
        }
        document.querySelector('.works-icon').src = '/static/img/light-works.svg';
        // document.querySelector('.archive-icon').src = '/static/img/light-archive.svg';
        document.querySelector('.help-icon').src = '/static/img/light-help.svg';
        try {
            document.querySelector('.moon-icon').src = '/static/img/light-moon.svg';
        } catch (_) {
            console.log("moon not found")
        }
        try {
            document.querySelector('.user-icon').src = '/static/img/light-user.svg';
        } catch (_) {
            console.log("user not found")
        }
        try {
            if (window.location.pathname == '/cart/') {
                document.querySelector('.cart-icon').src = '/static/img/light-cart-active.svg';
            } else {
                document.querySelector('.cart-icon').src = '/static/img/light-cart.svg';
            }
        } catch (_) {
            console.log("cart not found")
        }

        try {
            document.querySelector('.target-icon').src = '/static/img/light-target.svg';
        } catch (_) {
            console.log("target not found")
        }

        try {
            document.querySelector('.earth-icon').src = '/static/img/light-earth.svg';
        } catch (_) {
            console.log("earth not found")
        }

        try {
            document.querySelector('.search-icon').src = '/static/img/light-search.svg';
        } catch (_) {
            console.log("search not found")
        }

        try {
            document.querySelector('.truck-icon').src = '/static/img/light-truck.svg';
        } catch (_) {
            console.log("truck not found")
        }

        try {
            document.querySelector('.star-icon').src = '/static/img/light-star.svg';
        } catch (_) {
            console.log("star not found")
        }

        try {
            for (const deals of document.querySelectorAll('.success_deal')) {
                deals.src = '/static/img/success_deal_light.png';
            }
        } catch (_) {
            console.log("deals not found")
        }

        try {
            for (const close of document.querySelectorAll('.close-icon')) {
                close.src = '/static/img/light-close.svg';
            }
        } catch (_) {
            console.log("close not found")
        }

        try {
            for (const upload of document.querySelectorAll('.upload-icon')) {
                upload.src = '/static/img/light-upload.png';
            }
        } catch (_) {
            console.log("upload not found")
        }

        try {
            document.querySelector('.signup-img').src = '/static/img/light-signup.png';
        } catch (_) {
            console.log("signup not found")
        }

        try {
            document.querySelector('.delivery').src = '/static/img/delivery-light.png';
        } catch (_) {
            console.log("delivery not found")
        }

        try {
            document.querySelector('.location-img').src = '/static/img/light-location.svg';
        } catch (_) {
            console.log("location not found")
        }

        try {
            document.querySelector('.clip-img').src = '/static/img/light-clip.svg';
        } catch (_) {
            console.log("clip not found")
        }

        document.querySelector('.logo').src = '/static/img/logo-light.png';

        localStorage.setItem("theme", "light")
    }

});