function loadPage(url) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById('content').innerHTML = this.responseText;
        }
    };
    xhttp.open("GET", url, false);
    xhttp.send();
}

function toggleSidebar() {
    var sidebar = document.getElementById('sidebar');
    sidebar.style.width = (sidebar.style.width === '250px') ? '0' : '250px';
}

function showChangesContainer() {
    document.getElementById('changes-container').style.display = 'block';
    document.getElementById('job-seeking-container').style.display = 'none';
    document.getElementById('downloadButton').style.display = 'block';

}

function showJobSeekContainer() {
    document.getElementById('job-seeking-container').style.display = 'block';
    document.getElementById('changes-container').style.display = 'none';
    document.getElementById('downloadButton').style.display = 'none';
}