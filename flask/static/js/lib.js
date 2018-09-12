$(function() {
    $('#btn-process').click(function() {

        dtext = $('#description').val()
        if(dtext.trim().length < 50)
        {
            toast("Your input text is too short (min 50 chars.)", true);
            return;
        }

        if(dtext.trim().length > 5000)
        {
            toast("Your input text too long (max 5000 chars.)", true);
            return;
        }

        //alert("Holi")
        $("#btn-process").prop("disabled",true);
        $('#typeloader').show();
        $('#feedback').hide();
        $('#stname').text("Loading...");
        $('#ltname').text("...");
        $.ajax({
            url: '/process',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                //here we get the list of types and add it to the listing
                //console.log(response);

                var jresp = JSON.parse(response);

                var tname = jresp.predictions;
                var short_name = tname.substring(tname.lastIndexOf("/")+1,tname.length-1);
                var link_name = tname.substring(1, tname.length-1)

                $('#debug').val(response);
                //$('#description').val("");
                $('#stname').text(short_name);
                $('#stname').attr("href", link_name);
                $('#ltname').text(tname);

                $('#typeloader').hide();
                $('#feedback').show();
                $("#btn-process").prop("disabled",false);

            },
            error: function(error) {
                //we should show a pop up error
                console.log(error);
            }
        });
    });
});

function send_feedback(resp) {

    $("[id^=feed-btn]").prop("disabled",true);

    if (resp == 'yes')
    {
        $('#feed-expected-div').hide();
    }
    else
    {
        $('#feed-expected-div').show();
    }

    $('#feed-extra-modal').modal('show');

    $('#feed-resp').val(resp);
}



function submit_feedback() {


    var debug_text = $('#debug').val();
    var debug_json = JSON.parse(debug_text);
    debug_json["feedback"] = $('#feed-resp').val();
    debug_json["expectedtype"] = $('#expected-type').val();

    var d = new Date();
    debug_json["date"] = d.getTime();

    exp_array = []
    $("input:checkbox[name=feed-exp]:checked").each(function(){
        exp_array.push($(this).val());
    });


    debug_json["expertise"] = exp_array;

    debug_json["source"] = $('input[name=feed-source-radios]:checked').val();

    console.log(debug_json);


    $.ajax({
        url: '/feedback',
        contentType: 'application/json',
        data: JSON.stringify(debug_json),
        type: 'POST',
        success: function(response) {
            //here we get the list of types and add it to the listing
            console.log(response);

            if( response == "error")
            {
                toast("Something wrong happened, could not collect feedback, sorry :(", true);
            }
            else
            {

                toast("Thanks for the feedback!", false);

                // reset everything
                $('#feedback').hide();
                $('#debug').val("");
                $('#description').val("");

                $('#stname').text("...");
                $('#stname').attr("href", "");
                $('#ltname').text("...");

                $('#expected-type').val("None")

                // close modal
                $('#feed-extra-modal').modal('hide');



            }

            $("[id^=feed-btn]").prop("disabled",false);

        },
        error: function(error) {
            //we should show a pop up error
            console.log(error);
            $("[id^=feed-btn]").prop("disabled",false);
        }
    });
}

function toast(msg, error) {
    //alert(msg);


    if(error)
    {
        $('#feed_msg_head').html("<i class='fas fa-exclamation-triangle'></i> Error");
        $('#feed_msg_head').css('color', 'red');
    }
    else
    {
        $('#feed_msg_head').html("<i class='fas fa-check'></i> Success");
        $('#feed_msg_head').css('color', 'green');
    }

    $('#feed_msg_text').text(msg);
    $('#feed_msg').modal('show')
}

$(function() {

    // feedback buttons
    $('#feed-btn-yes').click(function() {
       send_feedback('yes')
    });
    $('#feed-btn-no').click(function() {
       send_feedback('no')
    });
    $('#feed-btn-abstract').click(function() {
       send_feedback('abstract')
    });
    $('#feed-btn-precise').click(function() {
       send_feedback('precise')
    });
    $('#feed-btn-related').click(function() {
       send_feedback('related')
    });

    // feedback information
    $('#feed-info-btn').click(function() {
        $('#feed-info-modal').modal('show')
    });

    // submit extra feedback
    $('#feed-submit-btn').click(function() {
        submit_feedback();
    });


});

$('#feed-extra-modal').on("hide.bs.modal", function() {
	$("[id^=feed-btn]").prop("disabled",false);
    $('#feed-resp').val("notdefined");
})
