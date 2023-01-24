function tankCallback(x) {
    x = JSON.parse(x);
    for (i of x){
        divStart = '<div class="tank-box" style="margin-left: 20px;">'
        tname = '<p>'+ i.tname + '</p>'
        tankID = i.user_id + '-' + i.tname
        if (i.sensor_id == null)
        {
            sID = '<p>no sensor detected </p>'
        }
        else
        {
            sID = '<p> sensor id: '+ i.sensor_id + '</p>'
        }
        seaButton = '<button class="manage-button" id="'+tankID+'">manage sealife</button>'
        deleteButton = '<button class="manage-delete" style="background-color: red !important;" id="'+tankID+'">delete tank</button></div>'
        $("#tank-container").prepend(divStart+tname+sID+seaButton+deleteButton)
    }
}

$(document).ready(function(){$.get("/tankmanage/", {}, tankCallback);});