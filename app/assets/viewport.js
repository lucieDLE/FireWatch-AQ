// Reports the browser viewport width into the "viewport-width" dcc.Store so that
// server-side callbacks can rebuild figures with a device-appropriate layout
// (e.g. the responsive box-plot facet grid). Debounced to avoid flooding resizes.
(function () {
    let timer;

    function reportWidth() {
        if (window.dash_clientside && window.dash_clientside.set_props) {
            window.dash_clientside.set_props("viewport-width", { data: window.innerWidth });
        }
    }

    window.addEventListener("resize", function () {
        clearTimeout(timer);
        timer = setTimeout(reportWidth, 200);
    });

    // Report once after the page (and Dash) have finished loading.
    window.addEventListener("load", function () {
        setTimeout(reportWidth, 300);
    });
})();
