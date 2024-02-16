<script>
export default {
    data() {
        return {
            series: [
                {
                    name: "",
                    data: [{
                        x: 'Sunday',
                        y: -1,
                        z: "",
                    }, {
                        x: 'Monday',
                        y: 0,
                        z: ""
                    }, {
                        x: 'Tuesday',
                        y: 50,
                        z: ""
                    }, {
                        x: 'Wednesday',
                        y: 75,
                        z: ""
                    }, {
                        x: 'Thursday',
                        y: 100,
                        z: ""
                    }, {
                        x: 'Friday',
                        y: 29,
                        z: ""
                    }, {
                        x: 'Saturday',
                        y: 13,
                        z: ""
                    },]
                },
                {
                    name: "",
                    data: [{
                        x: 'Sunday',
                        y: 22,
                        z: ""
                    }, {
                        x: 'Monday',
                        y: 29,
                        z: ""
                    }, {
                        x: 'Tuesday',
                        y: 13,
                        z: ""
                    }, {
                        x: 'Wednesday',
                        y: 32,
                        z: ""
                    }, {
                        x: 'Thursday',
                        y: 22,
                        z: ""
                    }, {
                        x: 'Friday',
                        y: 29,
                        z: ""
                    }, {
                        x: 'Saturday',
                        y: 13,
                        z: ""
                    },]
                },
                {
                    name: "",
                    data: [{
                        x: 'Sunday',
                        y: 22,
                        z: ""
                    }, {
                        x: 'Monday',
                        y: 29,
                        z: ""
                    }, {
                        x: 'Tuesday',
                        y: 13,
                        z: ""
                    }, {
                        x: 'Wednesday',
                        y: 32,
                        z: ""
                    }, {
                        x: 'Thursday',
                        y: 22,
                        z: ""
                    }, {
                        x: 'Friday',
                        y: 29,
                        z: ""
                    }, {
                        x: 'Saturday',
                        y: 13,
                        z: ""
                    },]
                },
                {
                    name: "",
                    data: [{
                        x: 'Sunday',
                        y: 22,
                        z: ""
                    }, {
                        x: 'Monday',
                        y: 29,
                        z: ""
                    }, {
                        x: 'Tuesday',
                        y: 13,
                        z: ""
                    }, {
                        x: 'Wednesday',
                        y: 32,
                        z: ""
                    }, {
                        x: 'Thursday',
                        y: 22,
                        z: ""
                    }, {
                        x: 'Friday',
                        y: 29,
                        z: ""
                    }, {
                        x: 'Saturday',
                        y: 13,
                        z: ""
                    },]
                },
                {
                    name: "",
                    data: [{
                        x: 'Sunday',
                        y: 22,
                        z: ""
                    }, {
                        x: 'Monday',
                        y: 29,
                        z: ""
                    }, {
                        x: 'Tuesday',
                        y: 13,
                        z: ""
                    }, {
                        x: 'Wednesday',
                        y: 32,
                        z: ""
                    }, {
                        x: 'Thursday',
                        y: 22,
                        z: ""
                    }, {
                        x: 'Friday',
                        y: 29,
                        z: ""
                    }, {
                        x: 'Saturday',
                        y: 13,
                        z: ""
                    },]
                },

            ],
            chartOptions: {
                chart: {
                    type: 'heatmap',
                },
                plotOptions: {
                    heatmap: {
                        shadeIntensity: 0.5,
                        radius: 1,
                        colorScale: {
                            ranges: [
                                {
                                    from: -1,
                                    to: -1,
                                    color: '#808080', // Making squares with -1 appear as spacers
                                    name: 'No Data'
                                },
                                {
                                    from: 0,
                                    to: 40,
                                    name: 'Poor Gas Mileage',
                                    color: '#B81B0E'
                                },
                                {
                                    from: 41,
                                    to: 70,
                                    name: 'Average Gas Mileage',
                                    color: '#F7B500'
                                },
                                {
                                    from: 71,
                                    to: 100,
                                    name: 'Good Gas Mileage',
                                    color: '#57E964'
                                }]
                        }
                    }
                },
                dataLabels: {
                    enabled: true,
                    formatter: function (val, opts) {
                        return opts.w.config.series[opts.seriesIndex].data[opts.dataPointIndex].z
                    },
                },
                colors: ["#008FFB"],
                title: {
                    text: 'Driving Efficiency for the Month',
                },
                xaxis: {
                    type: 'category',
                },
            },
        }
    },
    mounted() {
        this.generateDataForCurrentMonth()
    },
    methods: {
        generateDataForCurrentMonth() {
            const now = new Date();
            const year = now.getFullYear();
            const month = now.getMonth();

            // Find the first and last day of the month
            const firstDayDate = new Date(year, month, 2);
            const lastDayDate = new Date(year, month + 1, 0); // 0th day of next month is the last day of the current month

            const daysInMonth = lastDayDate.getDate();
            const firstDayOfWeek = firstDayDate.getDay(); // Day of week the month starts on

            // Calculate total slots based on starting day of the week (assuming Sunday is the start of the week)
            const totalSlots = firstDayOfWeek + daysInMonth;

            // Initialize the array with -1 for non-existing days
            const monthArray = new Array(totalSlots).fill(-1);
            // Fill the actual days with random numbers
            for (let i = firstDayOfWeek; i < totalSlots; i++) {
                monthArray[i] = Math.floor(Math.random() * 100) + 1;
            }
            var row = 0
            var day = 1
            for (var i = 4; i > -1; i--) {
                if (i == 4) {
                    row = 1
                }
                else {
                    row += 7
                }
                for (var j = 0; j < 7; j++) {
                    if (monthArray[row + j] == -1) {
                        this.series[i].data[j].y = -1
                    }
                    else {
                        this.series[i].data[j].y = monthArray[row + j]
                        this.series[i].data[j].z = day
                        day++
                    }
                }
            }
        },
    }
}
</script>

<template>
    <div>
        <v-card>
            <apexchart type="heatmap" height="350" :options="chartOptions" :series="series"></apexchart>
        </v-card>
    </div>
</template>

<style>
</style>