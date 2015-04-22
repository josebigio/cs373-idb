var xmlhttp = new XMLHttpRequest();
var url = "myTutorials.txt";

xmlhttp.onreadystatechange = function() {
    if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
        var element_info = JSON.parse(xmlhttp.responseText);
    }
}
xmlhttp.open("GET", url, true);
xmlhttp.send();

temp = 72;
gas_count = 0;
liquid_count = 0;
solid_count = 0;

for (var key in element_info) {
    if(element_info.hasOwnProperty(key)) {
        if(temp > key[boiling_point_k]) {
            gas_count++;
        }
        else if(temp > key[melting_point_k]) {
            liquid_count++;
        }
        else {
            solid_count++;
        }
    }
}

var data = [
{
    value: gas_count,
    color:"#F7464A",
    highlight: "#FF5A5E",
    label: "Gas"
},
{
    value: liquid_count,
    color: "#46BFBD",
    highlight: "#5AD3D1",
    label: "Liquid"
},
{
    value: solid_count,
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
                window.elements_chart = new Chart(ctx).Doughnut(data, options);
            };