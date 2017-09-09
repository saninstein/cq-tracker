'use strict';

var events = new Vue({
    el: '#events_app',
    data: {
        events: null,
        can_add: false,
        visible: false
    },

    methods: {
        displayWidget: function () {
            this.visible = !this.visible
        }
    },

    created: function () {
        document.getElementById("events_btn").onclick = function (e) {
            events.$methods.displayWidget()
        };
        axios.get('/api/events/')
            .then(function(res) {
                console.log("Events: ", status, res.data);
                events.$data.events = res.data['events'].map(function (p) {
                    p.date = dateConvert(p.date);
                    return p
                });
                events.$data.can_add = res.data['can_add_events'];
                if(!events.$data.events.length)
                    events.$data.events = [{'name': 'No events', 'date': ''}]
            })
            .catch(function (e) {
                console.log("Error:", e);
                events.$data.events = [{'name': 'No events', 'date': ''}]
            })
    },

});


function dateConvert(dateStr) {
    if(!dateStr)
        return dateStr;
    var dateAr = dateStr.split('-');
    dateAr.reverse();
    return dateAr.join('/');
}