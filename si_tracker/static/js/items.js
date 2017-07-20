/**
 * Created by Александр on 16.06.2017.
 */
var app = new Vue({
        el: '#app',
        data: {
            items: "None",
            user: null,
            statuses: null,
            controls:{
                sorts: {
                    title: true,
                    date1: true,
                    date2: true,
                    type: true,
                    status: true,
                    user1: true,
                    user2: true,
                },
                filter: {
                    self: false,
                    issue: true,
                    idea:true,
                    task: true,
                    status: 'Open',
                }
            }
        },
        methods: {
            filterChanged: function () {
                $.cookie('filter', JSON.stringify(this.controls.filter), { expires: 365, path: '/' });
            },

            onlyIssue: function () {
                this.items = this.items.filter(function(p) {
                    return p['type'] === 'Issue';
                })
            },

            sortBy: function (param) {
                var how;
                if (param === 'title') {
                    how = this.controls.sorts.title;
                    this.controls.sorts.title = !how;
                } else if (param === 'date_raised') {
                    how = this.controls.sorts.date1;
                    this.controls.sorts.date1 = !how;
                } else if (param === 'date_due') {
                    how = this.controls.sorts.date2;
                    this.controls.sorts.date2 = !how;
                } else if (param === 'type') {
                    how = this.controls.sorts.type;
                    this.controls.sorts.type = !how;
                }  else if (param === 'status') {
                    how = this.controls.sorts.status;
                    this.controls.sorts.status = !how;
                } else if (param === 'raised_user') {
                    how = this.controls.sorts.user1;
                    this.controls.sorts.user1 = !how;
                } else if (param === 'assigned_user') {
                    how = this.controls.sorts.user2;
                    this.controls.sorts.user2 = !how;
                } else if (param === 'location') {
                    how = this.controls.sorts.localtion;
                    this.controls.sorts.localtion = !how;
                } else {
                    return false;
                }
                console.log(param + ':', how);
                how = how ? (p1, p2) => { return (p1 < p2) ? -1 : (p1 > p2) ? 1 : 0 } : (p1, p2) => { return (p1 > p2) ? -1 : (p1 < p2) ? 1 : 0 };

                this.items.sort(function (p1, p2) {
                    return how(!p1[param] ? ' ' : p1[param].toLowerCase(), !p2[param] ? ' ' : p2[param].toLowerCase())
                });
            },

            filterStatus: function (status) {
                if(this.controls.filter.status === 'All')
                    return true;
                else if(this.controls.filter.status === 'Open')
                    return this.statuses.open.indexOf(status) !== -1 ? true : false;
                else if(this.controls.filter.status === 'Closed')
                    return this.statuses.close.indexOf(status) !== -1 ? true : false;
                return false;
            },

            filterBy: function (field, param) {
                if(param === 'Issue')
                    this.controls.filter.issue = !this.controls.filter.issue;
                else if(param === 'Task')
                    this.controls.filter.task = !this.controls.filter.task;
                else if(param === 'Idea')
                    this.controls.filter.idea = !this.controls.filter.idea;


                this.filterStatus('All');
                for (var i = 0; i < this.items.length; i++)
                    if(this.items[i][field] === param)
                        this.items[i].hide = !this.items[i].hide;
            }
        },
        created: function () {

            var data;
            axios.get("/items")
                .then(function (res) {
                    console.log("Res: ", res.data['results']);
                    app.$data.items = res.data['results'].map(function (p) {
                        p.hide = false;
                        p.date_raised = dateConvert(p.date_raised);
                        p.date_due = dateConvert(p.date_due);
                        if(p.tasks.length) {
                            p.expand = 0;
                        } else {
                            p.expand = -1;
                        }
                        return p;
                    });
                    app.$data.statuses = res.data['statuses'];
                    app.$data.user = res.data['user'];
                })
                .catch(function (error) {
                    console.log(error)
                });
        },
        mounted: function () {
            var filters = $.cookie('filter');
            if(filters)
                this.controls.filter = JSON.parse(filters);
        }
    });

function dateConvert(dateStr) {
    if(!dateStr)
        return dateStr;
    var dateAr = dateStr.split('-');
    dateAr.reverse();
    return dateAr.join('/');
}

