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
	AddMultipleField("Author", "title_author");
}
