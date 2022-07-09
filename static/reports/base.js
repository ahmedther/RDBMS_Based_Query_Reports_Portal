const spinnerBox = document.getElementById('spinner-box')
const dataBox = document.getElementById('table_id')

$.ajax({

    type : 'GET',
    url: '/stock',

    success: function(response){
        spinnerBox.classList.add('not-visible')

    }
})
