$(document).ready(function () {
    // Init
    $('.image-section').hide();
    $('.loader').hide();
    $('.result').hide();
    $('.feedback').hide();

    // Upload Preview
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#imagePreview').attr('src', e.target.result);
                // $('#imagePreview').css('background-image', 'url(' + e.target.result + ')');
                $('#imagePreview').hide();
                $('#imagePreview').fadeIn(650);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }
    $("#imageUpload").change(function () {
        $('.image-section').show();
        $('.cat-label').css("background-color", "rgb(131, 131, 131, 0.25)");
        $('.cat-label').css("color", "rgb(73, 110, 128, 0.5)");

        $('#cardboard').text('cardbboard');
        $('#glass').text('glass');
        $('#metal').text('metal');
        $('#paper').text('paper');
        $('#trash').text('trash');
        $('#plastic').text('plastic');

        $('#btn-predict').text('Predict!');
        $('#btn-predict').show();
        // $('.result').text('');
        $('.result-cat').text('');
        $('.result-prob').text('');
        $('.result').hide();
        $('.feedback').hide();
        readURL(this);
    });

    // Predict
    $('#btn-predict').click(function () {
        var form_data = new FormData($('#upload-file')[0]);
        // Show loading animation
        $(this).hide();
        $('.feedback').hide();
        $('.loader').show();

        // Make prediction by calling api /predict
        $.ajax({
            type: 'POST',
            url: '/predict',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
                // Get and display the result
                var cat_label = data.split(",")[0];
                var cat_prob = data.split(",")[1];
                var cat_input = "#"+cat_label;

                $('.loader').hide();
                $('.result').fadeIn(600);
                $('#btn-predict').text('Results');
                $('#btn-predict').show();
                $(cat_input).css("background-color", "#39D2B4");
                $(cat_input).css("color", "black");
                $(cat_input).text(cat_label + ", " + cat_prob);
                // $('#result-cat').text(data.split(",")[0]);
                // $('#result-prob').text(data.split(',')[1]);
                $('.feedback').show();
                console.log('Success!');
            },
        });
    });
});