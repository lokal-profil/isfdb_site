/*     Version: $Revision$
      (C) COPYRIGHT 2015-2017   Ahasuerus
         ALL RIGHTS RESERVED
      Date: $Date$ */

function validateURL(field_name) {
	// Retrieve the URL field - use [0] because JS returns an array in case there are many fields with this name
	var element_name = document.getElementsByName(field_name)[0];
	// If there is no URL field, validation is successful
	if (element_name == null) {
		return true;
	}
	// Retrieve the value of the field
	var element_value = element_name.value;
	// If the value is empty, then validation passes
	if (element_value == "") {
		return true;
	}
	// Check that the url starts with "http" (case insensitive)
	if (element_value.match(/^http/gi) == null) {
		alert("URLs must start with \"http\".");
		element_name.focus();
		return false;
	}
	return true;
}

function validateWebPages(add_point_name, field_name) {
	var addpoint = document.getElementById(add_point_name);
	// If there is no Web Page field, validation is successful
	if (addpoint == null) {
		return true;
	}
	// Retrieve the next available Web page number
	var next = addpoint.getAttribute("next");
	// Convert the next available Web page number to integer so that we can use it in a loop
	var int_next = parseInt(next);
	var count = 0;
	var web_page_field;
	for (i = 1 ; i < int_next ; i++) {
		web_page_field = field_name + i;
		// Validate each URL
		if (validateURL(web_page_field) == false) {
			return false;
		}
	}
	return true;
}

function validateRequired(field_name, display_name) {
	// Retrieve the Title field - use [0] because JS returns an array in case there are many fields with this name
	var element_name = document.getElementsByName(field_name)[0];
	// Retrieve the value of the field
	var element_value = element_name.value;
	// Strip all spaces to check for titles that consist of nothing but spaces
	element_value = element_value.split(" ").join("");
	//  Check if the resulting string is empty and generate an alert error
	if (element_value == "") {
		alert(display_name + " is a required field.");
		element_name.focus();
		return false;
	}
	return true;
}

function validateDate(value, display_name, type_of_date) {
	// Check that the entered string follows the YYYY-MM-DD format
	if ((value.match(/^\d{4}-{1}\d{2}-{1}\d{2}$/) == null) && (value.match(/^\d{4}$/) == null) && (value.match(/^\d{4}-{1}\d{2}$/) == null)) {
		if (type_of_date == "title") {
			alert(display_name + " must be in YYYY, YYYY-MM or YYYY-MM-DD format. 0000-00-00 means \"Unknown\", 8888-00-00 means \"Unpublished\" and 9999-00-00 means \"Forthcoming\".");
		}
		if (type_of_date == "award") {
			alert(display_name + " must be in YYYY, YYYY-MM or YYYY-MM-DD format. 8888-00-00 means \"Unpublished\" and 9999-00-00 means \"Forthcoming\".");
		}
		// For author dates, allow 0000-MM-DD dates
		if (type_of_date == "author") {
			if (value.match(/^0{4}-{1}\d{2}-{1}\d{2}$/) == null) {
				alert(display_name + " must be in YYYY, YYYY-MM or YYYY-MM-DD format.");
			}
		}
	return false;
	}
	// Parse the entered string and move the components to 'year', 'month' and 'day'
	var dateParts = new Array();
	dateParts = value.split("-");
	var year = dateParts[0];
	if (dateParts.length < 2) {
		var month = "00";
	}
	else {
		var month = dateParts[1];
	}
	if (dateParts.length < 3) {
		var day = "00";
	}
	else {
		var day = dateParts[2];
	}
	var currentDate = new Date();
	var currentYear = currentDate.getFullYear();
	if ((type_of_date == "author") && (year > currentYear)) {
		alert("For authors, dates later than the current year are not allowed.");
		return false;
	}
	if (type_of_date == "award") {
		if (year == "0000") {
			alert("For awards, 0000 years are not allowed.");
			return false;
		}
		if ((month != "00") || (day != "00")) {
			alert("Bad YEAR value. Only YYYY and YYYY-00-00 values are valid for awards.");
			return false;
		}
	}
	var nextYear = currentYear + 1;
	if ((year > nextYear) && (year != "0000") && (year != "9999") && (year != "8888")) {
		alert("Dates more than 1 year in the future are not allowed. Use 8888-00-00 for \"Unpublished\" and 9999-00-00 for \"Forthcoming\".");
		return false;
	}
	if ((year == "0000") || (year == "9999") || (year == "8888")) {
		if (((month != "00") || (day != "00")) && (type_of_date != "author")) {
			alert("Month and day must be 00 when entering 0000-00-00, 8888-00-00 or 9999-00-00.");
			return false;
		}
	}
	if (month > 12) {
		alert("Months must be between 01 and 12.");
		return false;
	}
	// Determine the last day in the entered month
	switch(month) {
	case "00":
		max_day = 31;
		break;
	case "01":
		max_day = 31;
		break;
	case "02":
		max_day = 28;
		break;
	case "03":
		max_day = 31;
		break;
	case "04":
		max_day = 30;
		break;
	case "05":
		max_day = 31;
		break;
	case "06":
		max_day = 30;
		break;
	case "07":
		max_day = 31;
		break;
	case "08":
		max_day = 31;
		break;
	case "09":
		max_day = 30;
		break;
	case "10":
		max_day = 31;
		break;
	case "11":
		max_day = 30;
		break;
	case "12":
		max_day = 31;
		break;
	default:
		alert("Bad month " + month + ".");
		return false;
	}
	/*If the year is a leap year and the month is February, change the last day from 28 to 29
	Note that this doesn't work correctly for the Julian calendar, which was superseded (in
	Europe) by the Gregorian calendar between 1582 and 1923. MySQL only allows Gregorian dates,
	so any YYYY-02-29 dates that follow the Julian calendar would cause errors at file time. */
	if ((month == "02") && (((year % 4 == 0) && (year % 100 != 0)) || (year % 400 == 0))) {
		max_day = 29;
	}
	if (day > max_day) {
		alert("Day greater than the last day in the entered month.");
		return false;
	}
	return true;
}

function validateRequiredDate(field_name, display_name, required, type_of_date) {
	// Retrieve the Title field - use [0] because JS returns an array in case there are many fields with this name
	var element_name = document.getElementsByName(field_name)[0];
	// Retrieve the value of the field
	var element_value = element_name.value;
	// Strip all spaces to check for years that consist of nothing but spaces
	element_value = element_value.split(" ").join("");
	// Check if the resulting string is empty
	if (element_value == "") {
		// If a value is required, generate an error if no value was entered
		if (required == "required") {
			alert(display_name + " is a required field.");
			element_name.focus();
			return false;
		}
		else {
			return true;
		}
	}
	// If a value was entered, call validateDate, which performs detailed validation
	if (validateDate(element_value, display_name, type_of_date) == false) {
		element_name.focus();
		return false;
	}
	return true;
}

function validateAuthors(author_type, field_name, display_name) {
	var addpoint = document.getElementById(author_type);
	// Check if the add point exists -- it does not for read-only authors
	if (addpoint == null) {
		return true;
	}
	// Retrieve the next available author number
	var next = addpoint.getAttribute("next");
	// Convert the next available author number to integer so that we can use it in a loop
	var int_next = parseInt(next);
	var count = 0;
	var author_field;
	var author_data;
	var author_value;
	for (i = 1 ; i < int_next ; i++) {
		author_field = field_name + i;
		author_data = document.getElementsByName(author_field)[0].value;
		// Strip all spaces to check for authors that consist of nothing but spaces
		author_value = author_data.split(" ").join("");
		if (author_value != "") {
			count++;
			break;
		}
	}
	if (count == 0) {
		alert("At least one " + display_name + " must be entered. See Help for details.");
		var first_field_name = field_name + "1";
		var first_field_handle = document.getElementsByName(first_field_name)[0];
		first_field_handle.focus();
		return false;
	}
	return true;
}

function addNewWebPage(webpage_type, bodyname) {
	var bodyname = bodyname || 'tagBody';
	var tbody = document.getElementById(bodyname);
	var addpoint = document.getElementById("AddWebPage");
	next = addpoint.getAttribute("next");
	var int_next = parseInt(next);
	int_next += 1;
	var str_next = int_next.toString();
	addpoint.setAttribute("next", str_next);
	var tr   = document.createElement("tr");
	var td1  = document.createElement("td");
	var td2  = document.createElement("td");
	var b  = document.createElement("b");
	label = "Web Page "+next+":";
	var txt1 = document.createTextNode(label);
	var input = document.createElement("input");
	attr = webpage_type+"_webpages"+next;
	input.setAttribute("name", attr);
	input.setAttribute("class", "metainput");
	input.setAttribute("tabindex", "1");
	td1.appendChild(b);
	b.appendChild(txt1);
	td2.appendChild(input);
	tr.appendChild(td1);
	tr.appendChild(td2);
	tbody.insertBefore(tr, addpoint);
}

function validateSeriesNumber() {
	// Retrieve the id of the Series Number field
	var element_name = document.getElementsByName("title_seriesnum")[0];
	// If there is no Series Number field in the form, validation is successful
	if (element_name == null) {
		return true;
	}
	// Retrieve the value of the field
	var element_value = element_name.value.split(" ").join("");
	// If the value doesn't match 0-9 numbers (the first one can't be 0), display an error
	if (element_value != "") {
		if (element_value.match(/^[0-9]{1,9}([\.]{1}[0-9]{1,4}){0,1}$/) == null) {
			alert("Series numbers must be between 1 and 999999999. You can use a decimal point and up to 4 digits after it to position titles in between other titles in the series, e.g. 3.5 will appear between 3 and 4");
			element_name.focus();
			return false;
		}
	}
	return true;
}

function validateContentIndicator() {
	// Retrieve the id of the Content field
	var content_name = document.getElementsByName("title_content")[0];
	// If there is no Content field in the form (pub edit forms), validation is successful
	if (content_name == null) {
		return true;
	}

	// Retrieve the value of the Content field; strip spaces
	var content_value = content_name.value.split(" ").join("");
	// If the Content field is empty, then no additional validation is needed
	if (content_value == "") {
		return true;
	}

	// Slash can't be the first character of the Content value
	if (content_value[0] == "/") {
		alert("Content value cannot begin with a slash.");
		content_name.focus();
		return false;
	}

	if (content_value.length > 31) {
		alert("Content value must be 31 characters or less.");
		content_name.focus();
		return false;
	}

	// Retrieve the id of the Title Type field
	var type_name = document.getElementsByName("title_ttype")[0];
	// If there is no Title Type field in the form (New Pub), validation is successful
	if (type_name == null) {
		return true;
	}
	// Retrieve the value of the Title Type field
	var type_value = type_name.value;
	// If the title type is not OMNIBUS, Content data is not allowed
	if (type_value != "OMNIBUS") {
		alert("Only OMNIBUS titles can have Content data.");
		content_name.focus();
		return false;
	}

	return true;
}

function AddMultipleField(addField, field, field_name, bodyname) {
	var bodyname = bodyname || 'tagBody';
	var tbody = document.getElementById(bodyname);
	var addpoint = document.getElementById(addField);
	next = addpoint.getAttribute("next");
	var int_next = parseInt(next);
	int_next += 1;
	var str_next = int_next.toString();
	addpoint.setAttribute("next", str_next);
	var tr   = document.createElement("tr");
	var td1  = document.createElement("td");
	var td2  = document.createElement("td");
	var b  = document.createElement("b");
	label = field+" "+next+":"
	var txt1 = document.createTextNode(label);
	var input = document.createElement("input");
	attr = field_name+next
	input.setAttribute("name", attr);
	input.setAttribute("class", "metainput");
	input.setAttribute("tabindex", "1");
	td1.appendChild(b);
	b.appendChild(txt1);
	td2.appendChild(input);
	tr.appendChild(td1);
	tr.appendChild(td2);
	tbody.insertBefore(tr, addpoint);
}

function determineArticle(word) {
	var article = 'a';
	switch(word[0]) {
	case "A":
		article = 'an';
		break;
	case "E":
		article = 'an';
		break;
	case "O":
		article = 'an';
		break;
	default:
		article = 'a';
		break;
	}
	return article;
}
