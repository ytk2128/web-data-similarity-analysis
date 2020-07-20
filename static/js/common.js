$(document).ready(function() {
    google.charts.load("current", {"packages": ["corechart"]});

    $("#buttonAdd").click(function() {
        textUrl = $("#url");
        if (textUrl.val().length == 0) return;

        buttonAdd = $("#buttonAdd");
        buttonBrowse = $("#buttonBrowse");
        loading = $("#loading");
        list = $("#list");

        textUrl.prop("disabled", true);
        buttonAdd.prop("disabled", true);
        buttonBrowse.prop("disabled", true);
        loading.removeClass("d-none");
        list.addClass("d-none");

        $.post("/add", { url: textUrl.val() }, function(data) {
            textUrl.prop("disabled", false);
            buttonAdd.prop("disabled", false);
            buttonBrowse.prop("disabled", false);
            loading.addClass("d-none");
            list.removeClass("d-none");
            
            $("#reportModalBody").html(`
            <table class="table" style="margin-bottom: 0px">
                <tr class>
                    <th><i class="fas fa-link mr-2"></i>URL</th>
                    <th><i class="fas fa-poll-h mr-2"></i>Status</th>
                </tr>
                <tr>
                    <td><span class="badge badge-dark">${data["url"]}</span></td>
                    <td><span class="badge badge-secondary">${data["status"]}</span></td>
                </tr>
            </table>
            `);
            $("#reportModal").modal({backdrop: "static", keyboard: false});
        });
    });

    $("#buttonBrowse").click(function() {
        $("#buttonBrowse2").click();
    });
    $("#buttonBrowse2").change(function() {
        var fr = new FileReader();
        fr.onload = function() {
            textUrl = $("#url");
            buttonAdd = $("#buttonAdd");
            buttonBrowse = $("#buttonBrowse");
            loading = $("#loading");
            list = $("#list");
    
            textUrl.prop("disabled", true);
            buttonAdd.prop("disabled", true);
            buttonBrowse.prop("disabled", true);
            loading.removeClass("d-none");
            list.addClass("d-none");
    
            $.post("/add2", { url: fr.result }, function(data) {
                textUrl.prop("disabled", false);
                buttonAdd.prop("disabled", false);
                buttonBrowse.prop("disabled", false);
                loading.addClass("d-none");
                list.removeClass("d-none");
                
                var dataList = data["urls"];
                var tableCode = `
                <table class="table" style="margin-bottom: 0px">
                    <tr class>
                        <th><i class="fas fa-link mr-2"></i>URL</th>
                        <th><i class="fas fa-poll-h mr-2"></i>Status</th>
                    </tr>
                `;
                for (var i = 0; i < dataList.length; i++) {
                    tableCode += `
                        <tr>
                            <td><span class="badge badge-dark">${dataList[i][0]}</span></td>
                            <td><span class="badge badge-secondary">${dataList[i][1]}</span></td>
                        </tr>
                    `;
                }
                tableCode += "</table>";
                $("#reportModalBody").html(tableCode);
                $("#reportModal").modal({backdrop: "static", keyboard: false});
            });
        }
        fr.readAsText(this.files[0]);
    });
});

function restore() {
    $("#tfidfLoading").removeClass("d-none");
    $("#tfidfReport").addClass("d-none");
    $("#csLoading").removeClass("d-none");
    $("#csReport").addClass("d-none");
}

function tfidf(url) {
    $("#tfidfModal").modal({backdrop: "static", keyboard: false});

    $.post("/tfidf", { url: url }, function(data) {
        $("#tfidfLoading").addClass("d-none");
        $("#tfidfUrl").html(url);
        $("#tfidfEtime").html(`${data["time"]} seconds`);
        $("#tfidfStatus").html(data["status"]);

        if (data["status"] == "success") {
            $("#tfidfTable").empty();
            var dataArray = [["Word", "TF-IDF"]];
            var dataList = data["tfidf"];
            var tableCode = `
            <div><i class="fas fa-sort-amount-down mr-2"></i><b>Top 10 Keywords and Pie Chart</b></div>
            <table class="table mt-2" style="margin-bottom: 0px">
                <tr>
                    <th><i class="far fa-file-word mr-2"></i>Word</th>
                    <th><i class="fas fa-wave-square mr-2"></i>TF-IDF</th>
                </tr>
            `;
            
            for (var i = 0; i < dataList.length; i++) {
                tableCode += `
                    <tr>
                        <td><span class="badge badge-light">${dataList[i][0]}</span></td>
                        <td><span class="badge badge-primary">${dataList[i][1]}</span></td>
                    </tr>
                `;

                dataArray.push([dataList[i][0], parseFloat(dataList[i][1])]);
            }
            tableCode += "</table>";
            $("#tfidfTable").append(tableCode);

            var chartData = google.visualization.arrayToDataTable(dataArray);
            var options = {
                "title": "Pie Chart for Top 10 Keywords",
                "width": 450,
                "height": 400,
                "pieSliceTextStyle": {color: 'black'}
            };

            var chart = new google.visualization.PieChart(document.getElementById("tfidfGraph"));
            chart.draw(chartData, options);
        }

        $("#tfidfReport").removeClass("d-none");
    });
}

function cosine_similarity(url) {
    $("#csModal").modal({backdrop: "static", keyboard: false});

    $.post("/cs", { url: url }, function(data) {
        $("#csLoading").addClass("d-none");
        $("#csUrl").html(url);
        $("#csEtime").html(`${data["time"]} seconds`);
        $("#csStatus").html(data["status"]);

        if (data["status"] == "success") {
            $("#csTable").empty();
            var dataArray = [["URL", "Similarity"]];
            var dataList = data["cos"];
            var tableCode = `
            <div><i class="fas fa-sort-amount-down mr-2"></i><b>Top 3 Similarity and Pie Chart</b></div>
            <table class="table mt-2" style="margin-bottom: 0px">
                <tr>
                    <th><i class="fas fa-link mr-2"></i>URL</th>
                    <th><i class="fas fa-vector-square mr-2"></i>Similarity</th>
                </tr>
            `;
            
            for (var i = 0; i < dataList.length; i++) {
                tableCode += `
                    <tr>
                        <td><span class="badge badge-light">${dataList[i][1]}</span></td>
                        <td><span class="badge badge-primary">${dataList[i][2]} %</span></td>
                    </tr>
                `;

                dataArray.push([dataList[i][1], parseFloat(dataList[i][2])]);
            }
            tableCode += "</table>";
            $("#csTable").append(tableCode);
            
            if (dataList.length > 0) {
                var chartData = google.visualization.arrayToDataTable(dataArray);
                var options = {
                    "title": "Pie Chart for Top 3 Similarity",
                    "width": 450,
                    "height": 400,
                    "pieSliceTextStyle": {color: 'black'}
                };

                var chart = new google.visualization.PieChart(document.getElementById("csGraph"));
                chart.draw(chartData, options);
            }
            else {
                $("#csGraph").html('<b style="width: 100px;">Number of data must be greater than 1<br/> in order to draw a chart.</b>');
            }
        }

        $("#csReport").removeClass("d-none");
    });
}