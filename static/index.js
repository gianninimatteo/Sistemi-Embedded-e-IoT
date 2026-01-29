function fetchData() {
    $.ajax({
        url: '/data',
        dataType: 'json',
        success: function(data) {
            $("#temperature").text(data.temperature);
            $("#humidity").text(data.humidity);
            $("#heating_status").text(data.heating_status);
        }
    });
}
setInterval(fetchData, 2000);
fetchData();
