var xmlhttp = new XMLHttpRequest();
var url = "http://theperiodictableproject.me/api/element?columns=symbol,element,boiling_point_k,melting_point_k";

xmlhttp.onreadystatechange = function() {
    document.write("In function");
    if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
        document.write("Success");
        var elements_info = JSON.parse(xmlhttp.responseText);
    }
}
xmlhttp.open("GET", url, true);
xmlhttp.send();

temp = 72;
gas_count = 0;
liquid_count = 0;
solid_count = 0;

for (var atomic_number in elements_info) {
    if(elements_info.hasOwnProperty(atomic_number))
    {
        for (var element_info in elements_info[atomic_number])
        {
            if(elements_info.hasOwnProperty(element_info)) {
                if(temp > element_info["boiling_point_k"]) {
                    gas_count++;
                }
                else if(temp > element_info["melting_point_k"]) {
                    liquid_count++;
                }
                else {
                    solid_count++;
                }
            }
        }
    }
}

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
                window.elements_chart = new Chart(ctx).Doughnut(data, options);
            };