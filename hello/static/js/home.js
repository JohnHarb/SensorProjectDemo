function tankCallback(x) {
    x = JSON.parse(x);
    $("#tank-container").html("");
    for (i of x){
        divStart = '<div class="tank-box" style="margin-left: 20px;">'
        tname = '<p>'+ i.tname + '</p>'
        tankID = i.user_id + '-' + i.tname
        sID = '<p> sensor id: '+ i.sensor_id + '</p>'
        seaButton = '<button class="manage-button" id="'+tankID+'">manage sealife</button>'
        deleteButton = '<button class="manage-delete" style="background-color: red !important;" id="'+tankID+'">delete tank</button></div>'
        $("#tank-container").html($("#tank-container").html()+divStart+tname+sID+seaButton+deleteButton);
    }
    addTank = '<button id= "addTank" type="button" style="margin-left: 20px; align-self: flex-start;">+</button>'
    $("#tank-container").html($("#tank-container").html()+addTank);
}

$(document).ready(function(){$.get("/dbget/", {}, tankCallback);});