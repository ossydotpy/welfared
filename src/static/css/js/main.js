document.addEventListener('DOMContentLoaded', function () {
    const siteHeader = document.querySelector('.site-header');
    // const mainContent = document.querySelector('main'); // We'll use body class for padding

    if (!siteHeader) {
        console.warn('Site header not found for sticky functionality.');
        return;
    }

    let lastScrollTop = 0;
    const headerInitialHeight = siteHeader.offsetHeight; // Height of header in its normal state

    // Scroll threshold: header becomes eligible to be sticky after scrolling down this much.
    // Using its own height is a good starting point.
    const scrollThreshold = headerInitialHeight > 0 ? headerInitialHeight : 150;

    window.addEventListener('scroll', function () {
        let st = window.pageYOffset || document.documentElement.scrollTop;

        if (st > lastScrollTop && st > scrollThreshold) {
            // --- Scrolling Down & past threshold ---
            // Header should not be sticky here. Remove if it was.
            if (siteHeader.classList.contains('sticky-active')) {
                siteHeader.classList.remove('sticky-active');
                document.body.classList.remove('header-is-sticky');
                document.documentElement.style.removeProperty('--header-sticky-height');
            }
        } else if (st < lastScrollTop && st > scrollThreshold) {
            // --- Scrolling Up & past threshold ---
            // Make header sticky
            if (!siteHeader.classList.contains('sticky-active')) {
                siteHeader.classList.add('sticky-active');
                // After 'sticky-active' is added, its offsetHeight might be what we need
                // for the placeholder if its padding/content changes in sticky state.
                // For this setup, siteHeader's own padding is constant.
                const currentHeaderHeight = siteHeader.offsetHeight;
                document.documentElement.style.setProperty('--header-sticky-height', currentHeaderHeight + 'px');
                document.body.classList.add('header-is-sticky');
            }
        } else if (st <= scrollThreshold) {
            // --- Near top (or at top, or scrolling up towards top from below threshold) ---
            // Remove sticky state
            if (siteHeader.classList.contains('sticky-active')) {
                siteHeader.classList.remove('sticky-active');
                document.body.classList.remove('header-is-sticky');
                document.documentElement.style.removeProperty('--header-sticky-height');
            }
        }
        lastScrollTop = st <= 0 ? 0 : st; // For Mobile or negative scrolling
    }, false);
});