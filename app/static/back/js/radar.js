var app = new Vue({
    el: '#app',
    data: {
        group1: {
            p1percent: 0,
            p2percent: 0,
            p3percent: 0,
            p4percent: 0,
            p5percent: 0,
            p6percent: 0
        }
    },
    created() {
        this.fetchProgressData();
    },
    computed: {
        g1fullEndPath: function () {
            let str = '';
            let vm = this;
            for (var point in vm.g1points) {
                str += `${this.g1points[point].x},${this.g1points[point].y} `;
            }
            return str.trim();
        },
        g1points: function () {
            return {
                "one": this.calcDistance(this.group1.p1percent, 1),
                "two": this.calcDistance(this.group1.p2percent, 2),
                "three": this.calcDistance(this.group1.p3percent, 3),
                "four": this.calcDistance(this.group1.p4percent, 4),
                "five": this.calcDistance(this.group1.p5percent, 5),
                "six": this.calcDistance(this.group1.p6percent, 6),
            };
        }
    },
    methods: {
        fetchProgressData() {
            const childId = 1; // Replace with actual childId or pass dynamically
            fetch(`/api/progress?childId=${childId}`)
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        console.error('Error:', data.error);
                    } else {
                        this.group1.p1percent = data.communication_skills || 0;
                        this.group1.p2percent = data.writing_skills || 0;
                        this.group1.p3percent = data.consistency || 0; // If `consistency` is available
                        this.group1.p4percent = data.emotions_understanding || 0;
                        this.group1.p5percent = data.expressive_proficiency || 0;
                        this.group1.p6percent = 0; // Or another variable if applicable
                    }
                })
                .catch(error => console.error('Error fetching progress data:', error));
        },
        calcDistance: function (percent, pointnumber) {
            let churn = function (startval, endval) {
                return ((percent * .01) * (endval - startval)) + startval;
            };
            switch (pointnumber) {
                case 1:
                    return {
                        x: churn(323.8, 75.6),
                        y: churn(338.6, 195.3)
                    };
                case 2:
                    return {
                        x: churn(323.8, 75.6),
                        y: churn(429.4, 572.7)
                    };
                case 3:
                    return {
                        x: churn(402.5, 402.5),
                        y: churn(474.9, 761.5)
                    };
                case 4:
                    return {
                        x: churn(481.2, 729.4),
                        y: churn(429.4, 572.7)
                    };
                case 5:
                    return {
                        x: churn(481.2, 729.4),
                        y: churn(338.6, 195.3)
                    };
                case 6:
                    return {
                        x: churn(402.5, 402.5),
                        y: churn(291.1, 6.5)
                    };

                default:
                    return { x: 0, y: 0 };
            }
        }
    }
});