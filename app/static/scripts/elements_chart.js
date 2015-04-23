var xmlhttp = new XMLHttpRequest();
var url = "http://theperiodictableproject.me/api/element?columns=symbol,element,boiling_point_k,melting_point_k";

var elements_info;

xmlhttp.onreadystatechange = function() {
    if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
        elements_info = JSON.parse(xmlhttp.responseText);
        construct_chart(elements_info)
    }
}
xmlhttp.open("GET", url, true);
xmlhttp.send();

function construct_chart(elements_info) {

    var temp = 72;
    var gas_count = 0;
    var liquid_count = 0;
    var solid_count = 0;

    for (var atomic_number in elements_info) {
        if(elements_info.hasOwnProperty(atomic_number))
        {
            for (var element_info in elements_info[atomic_number])
            {
                if(elements_info.hasOwnProperty(element_info)) {
                    if(temp > element_info["boiling_point_k"]) {
                        gas_count = gas_count + 1;
                    }
                    else if(temp > element_info["melting_point_k"]) {
                        liquid_count = liquid_count + 1;
                    }
                    else {
                        solid_count = solid_count + 1;
                    }
                }
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

}


//document.write(gas_count.toString());
//document.write(liquid_count.toString());
//document.write(solid_count.toString());

