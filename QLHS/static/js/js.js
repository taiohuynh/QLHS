function searchKeyWordTable() {
  let input, filter, table, tr, td, i, j, txtValue;
  input = document.getElementById("keyword");
  filter = input.value.toUpperCase();
  table = document.getElementById("pupil-table");
  tr = table.getElementsByTagName("tr");

  for (i = 0; i < tr.length; i++) {
    for (j = 0; j < 3; j++) {
        td = tr[i].getElementsByTagName("td")[j]
        if (td) {
          txtValue = td.textContent || td.innerText;
          if (txtValue.toUpperCase().indexOf(filter) > -1) {
            tr[i].style.display = "";
            break;
          } else {
            tr[i].style.display = "none";
          }
        }
    }
  }
}

fetch('/classlist', {
    method: "post",
    body: JSON.stringify({
        "mahs": document.getElementById("mahs").value,
        "lop_id": document.getElementById("lop").value
    }),
    headers: {
        'Content-Type': 'application/json'
    }
}).then(response => response.json())
.then(data => {
    console.log(data);
})
.catch(error => {
    console.error(error);
});