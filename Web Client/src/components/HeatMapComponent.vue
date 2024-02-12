<script>
export default {
    data() {
        return {
            series: [{
                name: 'Metric1',
                data: this.generateData(18, {
                    min: 0,
                    max: 90
                })
            },
            {
                name: 'Metric2',
                data: this.generateData(18, {
                    min: 0,
                    max: 90
                })
            },
            {
                name: 'Metric3',
                data: this.generateData(18, {
                    min: 0,
                    max: 90
                })
            },
            {
                name: 'Metric4',
                data: this.generateData(18, {
                    min: 0,
                    max: 90
                })
            },
            {
                name: 'Metric5',
                data: this.generateData(18, {
                    min: 0,
                    max: 90
                })
            },
            {
                name: 'Metric6',
                data: this.generateData(18, {
                    min: 0,
                    max: 90
                })
            },
            {
                name: 'Metric7',
                data: this.generateData(18, {
                    min: 0,
                    max: 90
                })
            },
            {
                name: 'Metric8',
                data: this.generateData(18, {
                    min: 0,
                    max: 90
                })
            },
            {
                name: 'Metric9',
                data: this.generateData(18, {
                    min: 0,
                    max: 90
                })
            }
            ],
            chartOptions: {
                chart: {
                    height: 350,
                    type: 'heatmap',
                },
                dataLabels: {
                    enabled: false
                },
                colors: ["#008FFB"],
                title: {
                    text: 'HeatMap Chart (Single color)'
                },
            },
        }
    },
    methods: {
        /**
         * Eventually this will be used to populate the heatmap with data from the servers
         * @param {*} count 
         * @param {*} yrange 
         */
        generateData(count, yrange) {
            var i = 0;
            var series = [];
            while (i < count) {
                var x = 'w' + (i + 1).toString();
                var y = Math.floor(Math.random() * (yrange.max - yrange.min + 1)) + yrange.min;
                series.push({
                    x: x,
                    y: y
                });
                i++;
            }
            return series;
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