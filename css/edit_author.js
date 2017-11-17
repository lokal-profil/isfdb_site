/*     Version: $Revision$
      Date: $Date$ */

function validateAuthorForm() {
	// Validate that a non-empty author name has been entered
	if (validateRequired("author_canonical","Canonical Name") == false) {
		return false;
	}
	// Validate that a non-empty directory entry has been entered
	if (validateRequired("author_lastname","Directory Entry") == false) {
		return false;
	}
	// Validate that the author's canonical name doesn't contain double quotes
	if (validateDoubleQuotes("author_canonical","Canonical Name") == false) {
		return false;
	}
	// Validate the birth date
	if (validateRequiredDate("author_birthdate", "Birth Date", "not required", "author") == false) {
		return false;
	}
	// Validate the death date
	if (validateRequiredDate("author_deathdate", "Death Date", "not required", "author") == false) {
		return false;
	}
	// Validate the author image URL
	if (validateURL("author_image") == false) {
		return false;
	}
	// Validate the Web Page URLs
	if (validateWebPages("AddWebPage", "author_webpages") == false) {
		return false;
	}
	// If validation passes, return "true", which will let the form submit
	return true;
}

function validateDoubleQuotes(field_name, display_name) {
	// Retrieve the Title field - use [0] because JS returns an array in case there are many fields with this name
	var element_name = document.getElementsByName(field_name)[0];
	// Retrieve the value of the field
	var element_value = element_name.value;
	// Check if the resulting string contains double quotes and generate an alert error
	if (element_value.indexOf("\"") !== -1) {
		alert("Double quotes are not allowed in " + display_name + ". Use single quotes instead.");
		element_name.focus();
		return false;
	}
	return true;
}
