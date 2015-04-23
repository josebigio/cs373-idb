var xmlhttp = new XMLHttpRequest();
var url = "http://theperiodictableproject.me/api/element?columns=symbol,element,boiling_point_k,melting_point_k";

var elements_info;

var data = [
    {
        value: 1,
        color:"#F7464A",
        highlight: "#FF5A5E",
        label: "Gas"
    },
    {
        value: 2,
        color: "#46BFBD",
        highlight: "#5AD3D1",
        label: "Liquid"
    },
    {
        value: 3,
        color: "#FDB45C",
        highlight: "#FFC870",
        label: "Solid"
    }
    
]
    var options = {
        segmentShowStroke : false,
        animateScale : true
    }

window.onload = function(){
                var ctx = document.getElementById("elements_chart").getContext("2d");
                window.elements_chart = new Chart(ctx).Pie(data, options);
            };

xmlhttp.onreadystatechange = function() {
    if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
        elements_info = JSON.parse(xmlhttp.responseText);
        construct_chart(295);
    }
}
xmlhttp.open("GET", url, true);
xmlhttp.send();

var slider = new Slider(document.getElementById('temperature_slider'), {
    formatter: function(value) {
        return 'Current temperature: ' + value;
    },
    change: function(event) {
        construct_chart(slider.data('slider').getValue());
    }
});

function construct_chart(temp) {

    var gas_count = 0;
    var liquid_count = 0;
    var solid_count = 0;

    for (var atomic_number in elements_info) 
    {
        if(temp > elements_info[atomic_number.toString()]["boiling_point_k"]) 
        {
            gas_count = gas_count + 1;
        }
        else if(temp > elements_info[atomic_number.toString()]["melting_point_k"]) 
        {
            liquid_count = liquid_count + 1;
        }
        else 
        {
            solid_count = solid_count + 1;
        }
    }

    window.elements_chart.segments[0].value = gas_count;
    window.elements_chart.segments[1].value = liquid_count;
    window.elements_chart.segments[2].value = solid_count;

    window.elements_chart.update();

}

