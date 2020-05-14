// Getting data every 1 second 

window.onload = function() {
    this.myData()
}

 var myVar = setInterval(myData, 60000);

function myData() {

     $.get("https://influx.77robinson.xyz/query?db=telegraf&q=SELECT%20LAST(count)%20FROM%20mqtt_consumer",
        function(LastCount) {


            var LastCountinRoom = LastCount["results"][0]["series"][0]["values"][0][1];


            //Second graph, heat map 
            //heatmap
            //second graph, set colour of heat mao
                    if(LastCountinRoom < 4){
                        thiscol = "	#FF0000"
                    }
                    else{
                        thiscol = "	#00FF00"
                    }

            

                
                 new Highcharts.chart('heatmap',{
                    chart: {
                        type: 'heatmap'
                    },
                    colorAxis: {
                            min: 0,
                            max: 6,
                            minColor: "#FF0000",
                            maxColor: "#00FF00",
                        },
                    title: { text: 'Rooms in R77' },
                    legend: { enabled: true,
                    },
                    credits: { enabled: false },
                    xAxis: { 
                        title: { text: '' },
                        labels: { enabled: false }
                    },
                    yAxis: { 
                        title: { text: '' },
                        labels: { enabled: false }
                    },
                    series: [{
                        borderWidth: 1,
                        borderColor:'rgba(255,255,255,.9)',
                        data: [
                            {x:0, y:2, value:1, title:'Meeting Room A', color:"#00FF00"}, 
                            {x:1, y:2, value:1, title:'Meeting Room B', color:"#FF0000"},
                            {x:2, y:2, value:1, title:'Meeting Room C', color:"#FF0000"},
                            {x:0, y:1, value:1, title:'Meeting Room D', color:"#FF0000"},
                            {x:1, y:1, value:1, title:'Meeting Room E', color:"#FF0000"},
                            {x:2, y:1, value:LastCountinRoom, title:'Meeting Room H', color:thiscol},
                            
                            
                        ],
                        dataLabels: {
                            enabled: true,
                            color: '#000000',
                            formatter: function () {
                                return this.point.title;
                            }
                        }
                    }]

                });






     });




     $.get("https://influx.77robinson.xyz/query?db=telegraf&q=SELECT%20LAST(Lux)%20FROM%20mqtt_consumer",
        function(LightLevels) {


            var latestlightlevel = LightLevels["results"][0]["series"][0]["values"][0][1];



            
                        //Second graph, heat map 
                        //heatmap
                        //second graph, set colour of heat mao
                    if(latestlightlevel<35){
                        lightcolor = "#FF0000"
                        lightText = "LIGHTS OFF"
                    }
                    else{
                        lightcolor = "#008000"
                        lightText = "LIGHTS ON"
                                    
                    }



                     new Highcharts.chart('heatmapForLight',{
                        chart: {
                            type: 'heatmap'
                        },
                        title: { text: lightText },
                        legend: { enabled: false },
                        credits: { enabled: false },
                        xAxis: { 
                            title: { text: '' },
                            labels: { enabled: false }
                        },
                        yAxis: { 
                            title: { text: '' },
                            labels: { enabled: false }
                        },
                        series: [{
                            borderWidth: 1,
                            // borderColor:'rgba(255,255,255,.9)',
                            data: [
                                {x:0, y:2, value:1, color:lightcolor}, 
                                
                            ],
                            dataLabels: {
                                enabled: true,
                                // color: '#000000',
                                formatter: function () {
                                    return this.point.title;
                                }
                            }
                        }]

                    });        
        
    });





    


        

    
};















