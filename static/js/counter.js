$( document ).ready( function() {

    jQuery(function ($) {
        "use strict";

        var counterUp = window.counterUp["default"]; // import counterUp from "counterup2"

        var $counters = $(".counter");

        /* Start counting, do this on DOM ready or with Waypoints. */
        $counters.each(function (ignore, counter) {
            var waypoint = new Waypoint( {
                element: $(this),
                handler: function() {
                    counterUp(counter, {
                        duration: 7000,
                        delay: 22
                    });
                    this.destroy();
                },
                offset: 'bottom-in-view',
            } );
        });

    });
});
