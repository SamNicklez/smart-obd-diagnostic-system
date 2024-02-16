<script>
export default {
    data() {
        return {
            series: [
                {
                    name: "",
                    data: [{
                        x: 'Sunday',
                        y: -1
                    }, {
                        x: 'Monday',
                        y: 0
                    }, {
                        x: 'Tuesday',
                        y: 50
                    }, {
                        x: 'Wednesday',
                        y: 75
                    }, {
                        x: 'Thursday',
                        y: 100
                    }, {
                        x: 'Friday',
                        y: 29
                    }, {
                        x: 'Saturday',
                        y: 13
                    },]
                },
                {
                    name: "",
                    data: [{
                        x: 'Sunday',
                        y: 22
                    }, {
                        x: 'Monday',
                        y: 29
                    }, {
                        x: 'Tuesday',
                        y: 13
                    }, {
                        x: 'Wednesday',
                        y: 32
                    }, {
                        x: 'Thursday',
                        y: 22
                    }, {
                        x: 'Friday',
                        y: 29
                    }, {
                        x: 'Saturday',
                        y: 13
                    },]
                },
                {
                    name: "",
                    data: [{
                        x: 'Sunday',
                        y: 22
                    }, {
                        x: 'Monday',
                        y: 29
                    }, {
                        x: 'Tuesday',
                        y: 13
                    }, {
                        x: 'Wednesday',
                        y: 32
                    }, {
                        x: 'Thursday',
                        y: 22
                    }, {
                        x: 'Friday',
                        y: 29
                    }, {
                        x: 'Saturday',
                        y: 13
                    },]
                },
                {
                    name: "",
                    data: [{
                        x: 'Sunday',
                        y: 22
                    }, {
                        x: 'Monday',
                        y: 29
                    }, {
                        x: 'Tuesday',
                        y: 13
                    }, {
                        x: 'Wednesday',
                        y: 32
                    }, {
                        x: 'Thursday',
                        y: 22
                    }, {
                        x: 'Friday',
                        y: 29
                    }, {
                        x: 'Saturday',
                        y: 13
                    },]
                },
                {
                    name: "",
                    data: [{
                        x: 'Sunday',
                        y: 22
                    }, {
                        x: 'Monday',
                        y: 29
                    }, {
                        x: 'Tuesday',
                        y: 13
                    }, {
                        x: 'Wednesday',
                        y: 32
                    }, {
                        x: 'Thursday',
                        y: 22
                    }, {
                        x: 'Friday',
                        y: 29
                    }, {
                        x: 'Saturday',
                        y: 13
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
                                    from: -2,
                                    to: -1,
                                    name: 'No Data',
                                    color: '#FFFFFF'
                                },
                                {
                                    from: 0,
                                    to: 50,
                                    name: 'low',
                                    color: '#00A100'
                                },
                                {
                                    from: 51,
                                    to: 75,
                                    name: 'medium',
                                    color: '#128FD9'
                                },
                                {
                                    from: 76,
                                    to: 100,
                                    name: 'high',
                                    color: '#FFB200'
                                }]
                        }
                    }
                },
                dataLabels: {
                    enabled: false
                },
                colors: ["#008FFB"],
                title: {
                    text: 'HeatMap Chart (Current Month)'
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
            const firstDayDate = new Date(year, month, 1);
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
            console.log(monthArray.length)
            var row = 0
            for(var i = 4; i > -1; i--){
                if(i == 4){
                    row = 1
                }
                else{
                    row += 7
                }
                for(var j = 0; j < 7; j++){
                    this.series[i]['data'][j].y = monthArray[row + j]
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
