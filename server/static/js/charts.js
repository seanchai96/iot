// DOUGHNUT CHART // 
function loadDonut() {
    console.log("test")
var xhttp  = new XMLHttpRequest();
        var site = "/get_doughnut"
        xhttp.open("GET", site, true);
        xhttp.onload = function() {
            if (this.status == 200 && this.readyState == 4 ) {
                var result = JSON.parse(this.responseText)
                var empt = result[0]
                var hog = result[1]
                var occ = result[2]
                var dataset_doughnut = {
                    labels: ["EMPTY", "HOGGED", "OCCUPIED"],
                    datasets: [{
                        data: [empt, hog, occ], //empt, hog, occ
                        backgroundColor: ['#29AB23', '#EFE509', '#F30C0C']
                    }]
                }
                
                $('#doughnut').remove();
                $('#world-map_donut').append('<canvas id="doughnut"></canvas>');
                var ctx = document.getElementById('doughnut');
                
                var myDoughnutChart = new Chart(ctx, {
                    type: 'doughnut',
                    data: dataset_doughnut,
                    options: {
                    title:{
                        display:true,
                        text: 'Real-time Seat Occupancy Counter' 
                    }
                } 
                });
                console.log("doughnut chart load successful")
            } else {
                console.log("failed to load doughnut chart")
            }
        }
    xhttp.send()

}
//=======
//console.log("HLELO")
//var dataset_doughnut = {
//    labels: ["Empty", "Hogging", "Occupied"],
//    datasets: [{
//        data: [20, 10, 30],
//        backgroundColor: ['#29AB23', '#EFE509', '#F30C0C'],
//        borderColor: [
//            '#0fe109',
//            '#edf40b',
//            '#ea2323'
//          ],
//          borderWidth: 2
//    }]
//}
//
//
//var ctx = document.getElementById('someChart');
//
//var myDoughnutChart = new Chart(ctx, {
//    type: 'doughnut',
//    data: dataset_doughnut,
//    options: {
//    title:{
//        display:true,
//        text: 'Real-time Seat Occupancy Counter' 
//    }
//} 
//});
//
//
//var ctx = document.getElementById('doughnut');
//>>>>>>> 15b7ca701449d34282863774adddd5c7f363310f

function loadStackedBarChart() {
    // STACKED BAR CHART // 
    var xhttp  = new XMLHttpRequest();
            var site = "/get_stacked"
            xhttp.open("GET", site, true);
            xhttp.onload = function() {
                if (this.status == 200 && this.readyState == 4 ) {
                    var result = JSON.parse(this.responseText)

                    mon_total = result[0][0] + result[0][1] + result[0][2]
                    tue_total = result[1][0] + result[1][1] + result[1][2] 
                    wed_total = result[2][0] + result[2][1] + result[2][2]
                    thu_total = result[3][0] + result[3][1] + result[3][2]
                    fri_total = result[4][0] + result[4][1] + result[4][2]

                    var dataset_stacked = {
                        labels:["Monday","Tuesday", "Wednesday", "Thursday", "Friday"],
                        datasets:[{
                            label: "EMPTY",
                            data: [(result[0][0]/mon_total*100),(result[1][0]/tue_total*100),(result[2][0]/wed_total*100),(result[3][0]/thu_total*100),(result[4][0]/fri_total*100)], //get_data[0,"WEEKLY"], get_data[1,"WEEKLY"], get_data[2,"WEEKLY"], get_data[3,"WEEKLY"], get_data[4,"WEEKLY"]
                            backgroundColor: "#29AB23"
                        },
                        {
                            label: "HOG",
                            data: [(result[0][1]/mon_total*100),(result[1][1]/tue_total*100),(result[2][1]/wed_total*100),(result[3][1]/thu_total*100),(result[4][1]/fri_total*100)],
                            backgroundColor: "#EFE509"
                        },
                        {
                            label: "OCCUPIED",
                            data: [(result[0][2]/mon_total*100),(result[1][2]/tue_total*100),(result[2][2]/wed_total*100),(result[3][2]/thu_total*100),(result[4][2]/fri_total*100)],
                            backgroundColor: "#F30C0C"
                        }]
                    }
                    
                    var ctx = document.getElementById('stacked-bar');
                    
                    var myStackedBar = new Chart(ctx, {
                        type: 'bar',
                        data: dataset_stacked,
                        options:{
                            responsive:true, 
                            maintainAspectRatio:true,
                            tooltips:{
                                mode:'index',
                                intersect: false,
                                callbacks:{
                                    label: function(tooltipItems, data) {
                                        return (parseFloat(tooltipItems.yLabel)).toFixed(1) + '%';
                                    }
                                }
                            },
                            scales: {
                                xAxes: [{ 
                                    stacked: true 
                                }], 
                                yAxes: [{ 
                                    stacked: true,
                                    ticks:{
                                        stepSize:20,
                                        max:100,
                                        callback: function(value,index,values) {
                                            return value + '%';
                                        }
                                        
                                    }
                                }]
                            }
                        }
                    })
                    console.log("stacked bar chart load successful")
                } else {
                    console.log("failed to load stacked bar chart")
                }
            }
        xhttp.send()
    }

    function loadStackedBarChartCur() {
        // STACKED BAR CHART // 
        var xhttp  = new XMLHttpRequest();
                var site = "/get_stacked_cur"
                xhttp.open("GET", site, true);
                xhttp.onload = function() {
                    if (this.status == 200 && this.readyState == 4 ) {
                        var result = JSON.parse(this.responseText)
    
                        mon_total = result[0][0] + result[0][1] + result[0][2]
                        tue_total = result[1][0] + result[1][1] + result[1][2] 
                        wed_total = result[2][0] + result[2][1] + result[2][2]
                        thu_total = result[3][0] + result[3][1] + result[3][2]
                        fri_total = result[4][0] + result[4][1] + result[4][2]
    
                        var dataset_stacked = {
                            labels:["Monday","Tuesday", "Wednesday", "Thursday", "Friday"],
                            datasets:[{
                                label: "EMPTY",
                                data: [(result[0][0]/mon_total*100),(result[1][0]/tue_total*100),(result[2][0]/wed_total*100),(result[3][0]/thu_total*100),(result[4][0]/fri_total*100)], //get_data[0,"WEEKLY"], get_data[1,"WEEKLY"], get_data[2,"WEEKLY"], get_data[3,"WEEKLY"], get_data[4,"WEEKLY"]
                                backgroundColor: "#29AB23"
                            },
                            {
                                label: "HOG",
                                data: [(result[0][1]/mon_total*100),(result[1][1]/tue_total*100),(result[2][1]/wed_total*100),(result[3][1]/thu_total*100),(result[4][1]/fri_total*100)],
                                backgroundColor: "#EFE509"
                            },
                            {
                                label: "OCCUPIED",
                                data: [(result[0][2]/mon_total*100),(result[1][2]/tue_total*100),(result[2][2]/wed_total*100),(result[3][2]/thu_total*100),(result[4][2]/fri_total*100)],
                                backgroundColor: "#F30C0C"
                            }]
                        }
                        
                        var ctx = document.getElementById('stacked-bar-cur');
                        
                        var myStackedBar = new Chart(ctx, {
                            type: 'bar',
                            data: dataset_stacked,
                            options:{
                                responsive:true, 
                                maintainAspectRatio:true,
                                tooltips:{
                                    mode:'index',
                                    intersect: false,
                                    callbacks:{
                                        label: function(tooltipItems, data) {
                                            return (parseFloat(tooltipItems.yLabel)).toFixed(1) + '%';
                                        }
                                    }
                                },
                                scales: {
                                    xAxes: [{ 
                                        stacked: true 
                                    }], 
                                    yAxes: [{ 
                                        stacked: true,
                                        ticks:{
                                            stepSize:20,
                                            max:100,
                                            callback: function(value,index,values) {
                                                return value + '%';
                                            }
                                            
                                        }
                                    }]
                                }
                            }
                        })
                        console.log("stacked bar chart load successful")
                    } else {
                        console.log("failed to load stacked bar chart")
                    }
                }
            xhttp.send()
        }

function getClick(source){
    if (document.getElementById(source.id).value === "false"){
        document.getElementById(source.id).value = "true" ;
    } else if (document.getElementById(source.id).value === "true"){
        document.getElementById(source.id).value = "false";
    }
    var emp_fill = (document.getElementById("emp_line").value == 'true');
    var occ_fill = (document.getElementById("occ_line").value == 'true');
    var hog_fill = (document.getElementById("hog_line").value == 'true');

    $('#line-chart').remove();
    $('#daily_line').append('<canvas id="line-chart" width="500" height="300"></canvas>');


    loadLineChart(emp_fill, occ_fill, hog_fill);
}

function getClickw(source){
    if (document.getElementById(source.id).value === "false"){
        document.getElementById(source.id).value = "true" ;
    } else if (document.getElementById(source.id).value === "true"){
        document.getElementById(source.id).value = "false";
    }
    var emp_fill_w = (document.getElementById("emp_line_w").value == 'true');
    var occ_fill_w = (document.getElementById("occ_line_w").value == 'true');
    var hog_fill_w = (document.getElementById("hog_line_w").value == 'true');

    $('#line-chart-weekly').remove();
    $('#weekly_line').append('<canvas id="line-chart-weekly" width="500" height="300"></canvas>');


    loadLineChartWeekly(emp_fill_w, occ_fill_w, hog_fill_w);
}

function getClickall(source){
    if (document.getElementById(source.id).value === "false"){
        document.getElementById(source.id).value = "true" ;
    } else if (document.getElementById(source.id).value === "true"){
        document.getElementById(source.id).value = "false";
    }
    var emp_fill_all = (document.getElementById("emp_line_all").value == 'true');
    var occ_fill_all = (document.getElementById("occ_line_all").value == 'true');
    var hog_fill_all = (document.getElementById("hog_line_all").value == 'true');

    $('#line-chart-all').remove();
    $('#all_line').append('<canvas id="line-chart-all" width="500" height="300"></canvas>');

    loadLineChartAll(emp_fill_all, occ_fill_all, hog_fill_all);
}


function loadLineChart(emp_fill, occ_fill, hog_fill) {
    var xhttp  = new XMLHttpRequest();
        var site = "/get_line"
        xhttp.open("GET", site, true);
        xhttp.onload = function() {
            if (this.status == 200 && this.readyState == 4 ) {
                var result = JSON.parse(this.responseText)
                empt = result[0]
                occ = result[1]
                hog = result[2]
        
                var chart_data = [{
                    label: "EMPTY",
                    data: empt,
                    fill: emp_fill,
                    backgroundColor:"rgba(44, 135, 68, 0.58)",
                    borderWidth: 1,                 // LINE THICKNESS HERE //
                    borderColor:"rgba(44, 135, 68, 0.58)",            // LINE COLOR HERE // 
                    pointRadius: 1,
                    type:'line',
                    lineTension:0
                }, {
                    label: "HOGGED",
                    data: hog,
                    fill: hog_fill,
                    backgroundColor: "rgba(192, 206, 3, 0.58)",
                    borderWidth: 1,
                    borderColor: "rgba(192, 206, 3, 0.58)",
                    pointRadius: 1,
                    type: 'line',
                    lineTension:0
                },{
                    label: "OCCUPIED",
                    data: occ,
                    fill: occ_fill,
                    backgroundColor: "rgba(128, 15, 15, 0.58)",
                    borderWidth: 1,
                    borderColor: "rgba(128, 15, 15, 0.58)",
                    pointRadius: 1,
                    type: 'line',
                    lineTension:0
                }];

                var ctx = document.getElementById('line-chart');
                
                var lineChart = new Chart(ctx, {
                    type:'line',
                    connectNullData:false,
                    data: {
                        labels: ["7AM","7:15AM","7:30AM","7:45AM","8AM","8:15AM","8:30AM","8:45AM", "9AM","9:15AM","9:30AM","9:45AM", "10AM","10:15AM","10:30AM","10:45AM", "11AM","11:15AM","11:30AM","11:45AM", "12PM","12:15PM","12:30PM","12:45PM", "1PM","1:15PM","1:30PM","1:45PM", "2PM","2:15PM","2:30PM","2:45PM", "3PM","3:15PM","3:30PM","3:45PM","4PM","4:15PM","4:30PM","4:45PM", "5PM","5:15PM","5:30PM","5:45PM", "6PM", "6:15PM","6:30PM","6:45PM","7PM"],
                        datasets: chart_data
                    }, 
                    options:{
                        responsive:true, 
                        maintainAspectRatio:false,
                        bezierCurve: false,
                        layout:{
                            padding:{
                                bottom:11
                            }
                        },
                        tooltips:{
                            mode:'index',
                            intersect: false
                        },
                        scales:{
                            yAxes:[{
                                ticks:{
                                    stepSize:1,
                                    max: 2
                                }
                            }]
                        }
                    }
                    })

                console.log("daily line chart load successful")
            } else {
                console.log("failed to load daily line chart")
            }
        }
    xhttp.send()
}

function loadLineChartWeekly(emp_fill, occ_fill, hog_fill) {
    var xhttp  = new XMLHttpRequest();
        var site = "/get_line_weekly"
        xhttp.open("GET", site, true);
        xhttp.onload = function() {
            if (this.status == 200 && this.readyState == 4 ) {
                var result = JSON.parse(this.responseText)
                empt = result[0]
                occ = result[1]
                hog = result[2]
        
                var chart_data = [{
                    label: "EMPTY",
                    data: empt,
                    fill: emp_fill,
                    backgroundColor:"rgba(44, 135, 68, 0.58)",
                    borderWidth: 1,                 // LINE THICKNESS HERE //
                    borderColor:"rgba(44, 135, 68, 0.58)",            // LINE COLOR HERE // 
                    pointRadius: 1,
                    type:'line',
                    lineTension:0
                }, {
                    label: "HOGGED",
                    data: hog,
                    fill: hog_fill,
                    backgroundColor: "rgba(192, 206, 3, 0.58)",
                    borderWidth: 1,
                    borderColor: "rgba(192, 206, 3, 0.58)",
                    pointRadius: 1,
                    type: 'line',
                    lineTension:0
                },{
                    label: "OCCUPIED",
                    data: occ,
                    fill: occ_fill,
                    backgroundColor: "rgba(128, 15, 15, 0.58)",
                    borderWidth: 1,
                    borderColor: "rgba(128, 15, 15, 0.58)",
                    pointRadius: 1,
                    type: 'line',
                    lineTension:0
                }];

                var ctx = document.getElementById('line-chart-weekly');
                
                var lineChart = new Chart(ctx, {
                    type:'line',
                    connectNullData:false,
                    data: {
                        labels: ["7AM","7.15AM","7.30AM","7.45AM","8AM","8.15AM","8.30AM","8.45AM", "9AM","9.15AM","9.30AM","9.45AM", "10AM","10.15AM","10.30AM","10.45AM", "11AM","11.15AM","11.30AM","11.45AM", "12PM","12.15PM","12.30PM","12.45PM", "1PM","1.15PM","1.30PM","1.45PM", "2PM","2.15PM","2.30PM","2.45PM", "3PM","3.15PM","3.30PM","3.45PM","4PM","4.15PM","4.30PM","4.45PM", "5PM","5.15PM","5.30PM","5.45PM", "6PM", "6.15PM","6.30PM","6.45PM","7PM"],
                        datasets: chart_data
                    }, 
                    options:{
                        responsive:true, 
                        maintainAspectRatio:false,
                        bezierCurve: false,
                        layout:{
                            padding:{
                                bottom:11
                            }
                        },
                        tooltips:{
                            mode:'index',
                            intersect: false
                        },
                        scales:{
                            yAxes:[{
                                ticks:{
                                    stepSize:1,
                                    max: 2
                                }
                            }]
                        }
                    }
                    })

                console.log("weekly line chart load successful")
            } else {
                console.log("failed to load weekly line chart")
            }
        }
    xhttp.send()
}

function loadLineChartAll(emp_fill, occ_fill, hog_fill) {
    var xhttp  = new XMLHttpRequest();
        var site = "/get_line_all"
        xhttp.open("GET", site, true);
        xhttp.onload = function() {
            if (this.status == 200 && this.readyState == 4 ) {
                var result = JSON.parse(this.responseText)
                empt = result[0]
                occ = result[1]
                hog = result[2]
        
                var chart_data = [{
                    label: "EMPTY",
                    data: empt,
                    fill: emp_fill,
                    backgroundColor:"rgba(44, 135, 68, 0.58)",
                    borderWidth: 1,                 // LINE THICKNESS HERE //
                    borderColor:"rgba(44, 135, 68, 0.58)",            // LINE COLOR HERE // 
                    pointRadius: 1,
                    type:'line',
                    lineTension:0
                }, {
                    label: "HOGGED",
                    data: hog,
                    fill: hog_fill,
                    backgroundColor: "rgba(192, 206, 3, 0.58)",
                    borderWidth: 1,
                    borderColor: "rgba(192, 206, 3, 0.58)",
                    pointRadius: 1,
                    type: 'line',
                    lineTension:0
                },{
                    label: "OCCUPIED",
                    data: occ,
                    fill: occ_fill,
                    backgroundColor: "rgba(128, 15, 15, 0.58)",
                    borderWidth: 1,
                    borderColor: "rgba(128, 15, 15, 0.58)",
                    pointRadius: 1,
                    type: 'line',
                    lineTension:0
                }];

                var ctx = document.getElementById('line-chart-all');
                
                var lineChart = new Chart(ctx, {
                    type:'line',
                    connectNullData:false,
                    data: {
                        labels: ["7AM","7.15AM","7.30AM","7.45AM","8AM","8.15AM","8.30AM","8.45AM", "9AM","9.15AM","9.30AM","9.45AM", "10AM","10.15AM","10.30AM","10.45AM", "11AM","11.15AM","11.30AM","11.45AM", "12PM","12.15PM","12.30PM","12.45PM", "1PM","1.15PM","1.30PM","1.45PM", "2PM","2.15PM","2.30PM","2.45PM", "3PM","3.15PM","3.30PM","3.45PM","4PM","4.15PM","4.30PM","4.45PM", "5PM","5.15PM","5.30PM","5.45PM", "6PM", "6.15PM","6.30PM","6.45PM","7PM"],
                        datasets: chart_data
                    }, 
                    options:{
                        responsive:true, 
                        maintainAspectRatio:false,
                        bezierCurve: false,
                        layout:{
                            padding:{
                                bottom:11
                            }
                        },
                        tooltips:{
                            mode:'index',
                            intersect: false
                        },
                        scales:{
                            yAxes:[{
                                ticks:{
                                    stepSize:1,
                                    max: 2
                                }
                            }]
                        }
                    }
                    })

                console.log("all-time line chart load successful")
            } else {
                console.log("failed to all-time weekly line chart")
            }
        }
    xhttp.send()
}

// Second line chart // 
function plot_secondline(){
    var chart_data = [{
        label: "EMPTY",
        data: [37.3, 31.44, 32.57, 45.52, 46.82, 100, 100, 41.11, 39.28, 36.61, 29.46, 34.76, 100, 100, 25.91, 31.46, 37.64, 32.34, 37.89, 100, 100, 64.59, 65.59, 71.21, 70.38, 75.49, 100, 100, 70.28, 100, 100, 100],
        fill: false,
        backgroundColor:"rgba(44, 135, 68, 0.58)",
        borderWidth: 1,                 // LINE THICKNESS HERE //
        borderColor:"rgba(44, 135, 68, 0.58)",            // LINE COLOR HERE // 
        pointRadius: 1,
        type:'line',
        lineTension:0
    }, {
        label: "HOGGED",
        data: [24.56, 23.93, 35.66, 28.95, 41.22, 0, 0, 27.89, 37.84, 19.88, 43.37, 21.03, 0, 0, 22.43, 32.23, 34.32, 37.89, 34.23, 0, 0, 12.13, 15.33, 10.01, 14.19, 15.32, 0, 0, 9.39, 0, 0, 0],
        fill: false,
        backgroundColor: "rgba(192, 206, 3, 0.58)",
        borderWidth: 1,
        borderColor: "rgba(192, 206, 3, 0.58)",
        pointRadius: 1,
        type: 'line',
        lineTension:0
    },{
        label: "OCCUPIED",
        data: [38.14, 44.63, 31.77, 25.53, 11.96, 0, 0, 31, 22.88, 43.51, 27.17, 44.21, 0, 0, 51.66, 36.31, 28.04, 29.77, 27.88, 0, 0, 23.28, 19.08, 18.78, 15.43, 9.19, 0, 0, 20.33, 0, 0, 0],
        fill: false,
        backgroundColor: "rgba(128, 15, 15, 0.58)",
        borderWidth: 1,
        borderColor: "rgba(128, 15, 15, 0.58)",
        pointRadius: 1,
        type: 'line',
        lineTension:0
    }];
    var getDaysArray = function(start, end) {
        for(var arr=[],dt=start; dt<=end; dt.setDate(dt.getDate()+1)){
            arr.push(new Date(dt));
        }
        return arr;
    };

    console.log(chart_data)
    
    var daylist = getDaysArray(new Date("2020-03-02"),new Date("2020-04-02"));
    console.log(daylist);

    var ctx = document.getElementById('secondline');
                
                var lineChart = new Chart(ctx, {
                    type:'line',
                    connectNullData:false,
                    data: {
                        labels:daylist,
                        datasets: chart_data
                    }, 
                    options:{
                        responsive:true, 
                        maintainAspectRatio:false,
                        bezierCurve: false,
                        layout:{
                            padding:{
                                bottom:11
                            }
                        },
                        tooltips:{
                            mode:'index',
                            intersect: false,
                            callbacks:{
                                    label: function(tooltipItems, data) {
                                        return (parseFloat(tooltipItems.yLabel)).toFixed(1) + '%';
                                    }
                                }
                        },
                        scales:{
                            xAxes:[{
                                type:'time',
                                gridLines:{
                                  display:true,
                                  lineWidth:0.3  
                                },
                                time:{
                                    tooltipFormat:'DD MMM',
                                    unit:'day'
                                }
                            }], 
                            yAxes: [{ 
                                        stacked: false,
                                        ticks:{
                                            callback: function(value,index,values) {
                                                return value + "%" ;
                                            }
                                            
                                        }
                                    }]
                        }
            }
        }
    )
}
// get all data, hourly basis 
