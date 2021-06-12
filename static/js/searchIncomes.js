const SearchField = document.querySelector("#searchfield");
const tableOutPut = document.querySelector(".table-output");
const appTable = document.querySelector(".app-table");
const tablebody = document.querySelector(".t-body");
const paginationcontainer = document.querySelector(".pagination-container");
const Noresults = document.querySelector(".noresult");
tableOutPut.style.display = 'none';
Noresults.style.display = 'none';

SearchField.addEventListener("keyup", (e) => {
    const searchValue = e.target.value;
    if (searchValue.trim().length > 0) {
        console.log('searchValue', searchValue);
        paginationcontainer.style.display = 'none';
        tablebody.innerHTML = "";


        fetch("/income/search_income", {
            body: JSON.stringify({ SearchText: searchValue }),
            method: "POST",
        })
            .then((res) => res.json())
            .then((data) => {
                console.log("data", data);
                appTable.style.display = 'none';
                tableOutPut.style.display = 'block';
                console.log("data.length", data.length);
                if (data.length === 0) {
                    Noresults.style.display = "block";
                    tableOutPut.style.display = "none";
                } else {
                    Noresults.style.display = "none";
                    data.forEach((item) => {
                        console.log("item", item);
                        tablebody.innerHTML += "<tr><th>" + item.amount + "</th><th>" + item.source + "</th><th>" + item.description + "</th><th>" + item.date + "</th><th><a href='{% url 'income_edit' ${item.id} %}' class='btn btn-secondary btn-sm'>Edit</a></th></tr>";
                    });

                }
            });
    } else {
        tableOutPut.style.display = 'none';
        appTable.style.display = 'block';
        paginationcontainer.style.display = 'block';
    }
});