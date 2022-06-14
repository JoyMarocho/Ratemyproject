$(document).ready(function() {
    $('form').submit(function(event) {
        event.preventDefault()
        form = $("form")

    $.ajax({
        'url':'/ajax/ratings/',
        'type': 'POST',
        'data': form.serialize(),
        'dataType': 'json',
        'success': function(data) {
            alert(data['success'])
        },
    }) //End of Ajax method
    $('id_your_name').val('')
    $('id_your_email').val('')
  }) //End of submit function

}) //End of document ready function