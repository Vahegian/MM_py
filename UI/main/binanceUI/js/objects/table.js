class Table {
    constructor(_tableName) {
        this.tableName = _tableName;
        this.tableHead = null;
        this.tableBody = null;
    }

    makeTableHead(list_Of_Items, classes=null) {
        this.tableHead = this.make_html_table_item("thead");
        if (classes != null) {
            this.tableHead.setAttribute("class", classes);
        }
        var row = this.make_html_table_item("tr");
        for (var item of list_Of_Items) {
            var hItem = this.make_html_table_item("th");
            hItem.innerHTML = item;
            row.appendChild(hItem);
        }
        this.tableHead.appendChild(row);
        return this.tableHead;
    }

    makeTableBody(list_of_list_with_items, classes=null) {
        this.tableBody = this.make_html_table_item("tbody");
        if (classes != null) {
            this.tableBody.setAttribute("class", classes);
        }
        for (var list of list_of_list_with_items) {
            var row = this.make_html_table_item("tr");
            for (var item of list) {
                var bItem = this.make_html_table_item("td");
                bItem.innerHTML = item;
                row.appendChild(bItem);
            }
            this.tableBody.appendChild(row);
        }
        return this.tableBody;
    }

    make_html_table_item(type) {
        return document.createElement(type);
    }

    makeTable(list_of_head_items, list2D_of_body_items, classes = null) {
        var table = this.make_html_table_item("table");
        if (classes != null) {
            table.setAttribute("class", classes);
        }
        table.setAttribute("id", this.tableName);
        this.makeTableHead(list_of_head_items);
        this.makeTableBody(list2D_of_body_items);
        table.appendChild(this.tableHead);
        table.appendChild(this.tableBody);
        return table
    }

    makeTableFrom(head, body, classes=null){
        var table = this.make_html_table_item("table");
        if (classes != null) {
            table.setAttribute("class", classes);
        }
        table.appendChild(head);
        table.appendChild(body);
        return table
    }

    /*          Static Methods      */
}