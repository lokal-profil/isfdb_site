/*     Version: $Revision$
      (C) COPYRIGHT 2015-2018   Ahasuerus
         ALL RIGHTS RESERVED
      Date: $Date$ */

function validateParentTitle() {
	// Validate that a non-empty parent ID has been entered
	if (validateRequired("Parent","Parent Title Number") == false) {
		return false;
	}
	return true;
}

function validateTitleForm(title_type) {
	// Validate that a non-empty title has been entered
	if (validateRequired("title_title","Title") == false) {
		return false;
	}
	// Validate this title's authors if the title is a review
	if (title_type == "REVIEW") {
		// First check the authors of the title being reviewed
		if (validateAuthors("review_author1.", "reviewee") == false) {
			return false;
		}
		// If the first check passed, check the authors of the review
		if (validateAuthors("review_reviewer1.", "reviewer") == false) {
			return false;
		}
	}
	// Validate this title's authors if the title is an interview
	else if (title_type == "INTERVIEW") {
		// First check the authors being interviewed
		if (validateAuthors("interviewee_author1.", "interviewee") == false) {
			return false;
		}
		// If the first check passed, check the interviewers
		if (validateAuthors("interviewer_author1.", "interviewer") == false) {
			return false;
		}
	}
	// Validate this title's authors if the title is a regular title
	else {
		if (validateAuthors("title_author", "author/editor") == false) {
			return false;
		}
	}
	// Validate the Web Page URLs
	if (validateWebPages("title_webpages") == false) {
		return false;
	}
	// Validate the date of the title
	if (validateRequiredDate("title_copyright", "Date", "required", "title") == false) {
		return false;
	}
	// Validate the Series Number field
	if (validateSeriesNumber() == false) {
		return false;
	}
	// Validate the Length field
	if (validateLength() == false) {
		return false;
	}
	// Perform CHAPBOOK-specific validation
	if (validateChapbook() == false) {
		return false;
	}

	// Validate the Content field
	if (validateContentIndicator() == false) {
		return false;
	}
	return true;
}

function validateLength() {
	// Retrieve the id of the Length field
	var length_name = document.getElementsByName("title_storylen")[0];
	// If there is no Length field in the form, validation is successful
	if (length_name == null) {
		return true;
	}
	// Retrieve the value of the Length field
	var length_value = length_name.value;

	// Retrieve the id of the Title Type field
	var type_name = document.getElementsByName("title_ttype")[0];
	// If there is no Length field in the form, validation is successful
	if (type_name == null) {
		return true;
	}

	// Retrieve the value of the Title Type field
	var type_value = type_name.value;

	if ((type_value != "SHORTFICTION") && (length_value != "")) {
		alert("Only SHORTFICTION titles can have length specified.");
			length_name.focus();
			return false;
	}

	return true;
}

function validateChapbook() {
	// Retrieve the id of the Title Type field
	var type_name = document.getElementsByName("title_ttype")[0];
	// Retrieve the value of the Title Type field
	var type_value = type_name.value;
	// If the title type is not CHAPBOOK, then no additional validation is needed
	if (type_value != "CHAPBOOK") {
		return true;
	}

	// Retrieve the id of the Synopsis field
	var synopsis_name = document.getElementsByName("title_synopsis")[0];
	// Retrieve the value of the Synopsis field; strip spaces
	var synopsis_value = synopsis_name.value.split(" ").join("");

	if (synopsis_value != "") {
		alert("CHAPBOOKs cannot have synopsis data.");
		synopsis_name.focus();
		return false;
	}

	// Retrieve the id of the Series field
	var series_name = document.getElementsByName("title_series")[0];
	// Retrieve the value of the Series field; strip spaces
	var series_value = series_name.value.split(" ").join("");

	if (series_value != "") {
		alert("CHAPBOOKs cannot have series data.");
		series_name.focus();
		return false;
	}

	// Retrieve the id of the Series Number field
	var seriesnum_name = document.getElementsByName("title_seriesnum")[0];
	// Retrieve the value of the Series Number field; strip spaces
	var seriesnum_value = seriesnum_name.value.split(" ").join("");

	if (seriesnum_value != "") {
		alert("CHAPBOOKs cannot have series data.");
		seriesnum_name.focus();
		return false;
	}

	return true;
}

function validateVariantTitleForm() {
	// Validate that a non-empty title has been entered
	if (validateRequired("title_title","Title") == false) {
		return false;
	}
	// Validate this title's authors
	if (validateAuthors("title_author", "author/editor") == false) {
		return false;
	}
	// Validate the date of the title
	if (validateRequiredDate("title_copyright", "Date", "required", "title") == false) {
		return false;
	}
	return true;
}

function addMetadataTitleAuthor() {
	AddMultipleField("Author", "title_author", "titleBody");
}

function addContentTitleAuthor(entry) {
	tag = "AddAuthor"+entry;
	body_name = "titleBody";
	label_name = "Author";
	attr_name = "title_author";
	width_class = "contentinput";
	addPerson(entry, tag, body_name, label_name, attr_name, width_class);
}

function addReviewee(entry, width_class) {
	var width_class = width_class || 'contentinput';
	tag = "AddReviewee"+entry;
	body_name = "reviewBody";
	label_name = "Author";
	attr_name = "review_author";
	addPerson(entry, tag, body_name, label_name, attr_name, width_class);
}

function addReviewer(entry, width_class) {
	var width_class = width_class || 'contentinput';
	tag = "AddReviewer"+entry;
	body_name = "reviewBody";
	label_name = "Reviewer";
	attr_name = "review_reviewer";
	addPerson(entry, tag, body_name, label_name, attr_name, width_class);
}

function addInterviewee(entry, width_class) {
	var width_class = width_class || 'contentinput';
	tag = "AddInterviewee"+entry;
	body_name = "interviewBody";
	label_name = "Interviewee";
	attr_name = "interviewee_author";
	addPerson(entry, tag, body_name, label_name, attr_name, width_class);
}

function addInterviewer(entry, width_class) {
	var width_class = width_class || 'contentinput';
	tag = "AddInterviewer"+entry;
	body_name = "interviewBody";
	label_name = "Interviewer";
	attr_name = "interviewer_author";
	addPerson(entry, tag, body_name, label_name, attr_name, width_class);
}

function addArtist(entry, width_class) {
	var width_class = width_class || 'contentinput';
	tag = "AddArtist"+entry;
	body_name = "coverBody";
	label_name = "Artist";
	attr_name = "cover_artist";
	addPerson(entry, tag, body_name, label_name, attr_name, width_class);
}

function addPerson(entry, tag, body_name, label_name, attr_name, width_class) {
	var addpoint = document.getElementById(tag);
	var tbody = document.getElementById(body_name);
	// Update the 'next' attribute for later additions
	next = addpoint.getAttribute("next");
	var int_next = parseInt(next);
	int_next += 1;
	var str_next = int_next.toString();
	addpoint.setAttribute("next", str_next);
	// Create the DOM elements
	var tr   = document.createElement("tr");
	var td1  = document.createElement("td");
	var td2  = document.createElement("td");
	var b  = document.createElement("b");
	label = label_name+next+":";
	var txt1 = document.createTextNode(label);
	var input = document.createElement("input");
	var attr = attr_name+entry+"."+next;
	tr.setAttribute("id", attr + '.row');
	input.setAttribute("name", attr);
	input.setAttribute("class", width_class);
	input.setAttribute("tabindex", "1");
	input.setAttribute("id", attr);
	// Link the elements into the DOM
	td1.appendChild(b);
	b.appendChild(txt1);
	td2.appendChild(input);
	tr.appendChild(td1);
	tr.appendChild(td2);
	tbody.insertBefore(tr, addpoint);
}
