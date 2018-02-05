/*     Version: $Revision$
      (C) COPYRIGHT 2015-2018   Ahasuerus
         ALL RIGHTS RESERVED
      Date: $Date$ */

function validatePubURL(field_name) {
	// First check that the entered URL contains only valid URL characters
	if (validateURL(field_name) == false) {
		return false;
	}
	// Retrieve the URL field - use [0] because JS returns an array in case there are many fields with this name
	var element_name = document.getElementsByName(field_name)[0];
	// If there is no URL field, validation is successful
	if (element_name == null) {
		return true;
	}
	// Retrieve the value of the field
	var element_value = element_name.value;
	// Check if the resulting string contains a Wiki page URL and generate an alert error
	if (element_value.indexOf("http://www.isfdb.org/wiki/index.php/Image") !== -1) {
		alert("URL for the cover image should be for the image, not the Wiki page that the image is on");
		element_name.focus();
		return false;
	}
	return true;
}

function validateContents(title_add_point, title_field, title_date, author_add_point, author_field, display_name_author, display_name_title) {
	// Initialize variables
	var addpoint1;
	var addpoint2;
	var author_data;
	var defined_authors;
	var current_title_date;
	var current_title_field;
	var current_author_field;
	var current_title_page;
	var i;
	var int_next1;
	var int_next2;
	var j;
	var next1;
	var next2;
	var title_data;
	var title_date_data;
	var title_date_handle;
	var title_handle;
	var title_page_handle;
	var title_page_data;
	var length_field;
	var length_field_handle;
	var length_field_data;
	var ttype_field;
	var ttype_field_handle;
	var ttype_field_data;

	addpoint1 = document.getElementById(title_add_point);
	// Retrieve the next available title number
	next1 = addpoint1.getAttribute("next");
	// Convert the next available title number to integer so that we can use it in a loop
	int_next1 = parseInt(next1);
	// Check each title record defined on this page
	for (i = 1 ; i < int_next1 ; i++) {
		// Build the name of the title field that is being processed
		current_title_field = title_field + i;
		// Retrieve the handle of this title record in case we need to focus on it later
		title_handle = document.getElementsByName(current_title_field)[0];
		// Retrieve the title of this title record
		title_data = title_handle.value;
		// Strip all spaces in case the title consists of nothing but spaces
		title_data = title_data.split(" ").join("");
		// Check this title's page number -- must be processed first because it can be defined for greyed out titles
		// Build the name of the page number for the currently processed title
		current_title_page = display_name_title + "_page" + i;
		// Retrieve the handle of the current title page field
		title_page_handle = document.getElementsByName(current_title_page)[0];
		// Retrieve the value of the current title page field
		title_page_data = title_page_handle.value;
		// Strip all spaces in case the page number consists of nothing but spaces
		title_page_data = title_page_data.split(" ").join("");
		if (title_page_data.length > 20) {
			alert("Page number must be 20 character or less.");
			title_page_handle.focus();
			return false;
		}
		if ((title_page_data != "") && (title_data == "")) {
			alert("Page number entered, but no title is specified.");
			title_handle.focus();
			return false;
		}
		// Retrieve the number of authors for this record
		addpoint2 = document.getElementById(author_add_point + i);
		// If there is no author add point for this title, then it's read-only and we will skip it
		if (addpoint2 == null) {
			continue;
		}
		// Retrieve the next available author number for this title
		next2 = addpoint2.getAttribute("next");
		// Initialize the number of defined authors for this title
		defined_authors = 0;
		// Convert the next available author number to integer so that we can use it in a loop
		int_next2 = parseInt(next2);
		// Check each author name defined for this title
		for (j = 1 ; j < int_next2 ; j++) {
			current_author_field = author_field + i + "." + j;
			// Retrieve the author's name for this author
			author_data = document.getElementsByName(current_author_field)[0].value;
			// Strip all spaces to check for authors that consist of nothing but spaces
			author_value = author_data.split(" ").join("");
			if (author_value != "") {
				defined_authors++;
			}
		}
		if ((title_data != "") && (defined_authors == 0)) {
			alert("No " + display_name_author + " entered for " + display_name_title + " " + title_data + ". At least one " + display_name_author + " must be entered. See Help for details.");
			title_handle.focus();
			return false;
		}
		if ((title_data == "") && (defined_authors != 0)) {
			alert("No " + display_name_title + " entered, but at least one " + display_name_author + " is specified. See Help for details.");
			title_handle.focus();
			return false;
		}
		// Check this title's date
		// Build the name of the currently processed title field
		current_title_date = title_date + i;
		// Retrieve the handle of the current title date field
		title_date_handle = document.getElementsByName(current_title_date)[0];
		// Retrieve the value of the current title date field
		title_date_data = title_date_handle.value;
		// Strip all spaces in case the date consists of nothing but spaces
		title_date_data = title_date_data.split(" ").join("");
		if ((title_date_data != "") && (validateDate(title_date_data,"Date","title")) == false) {
			title_date_handle.focus();
			return false;
		}

		if (title_add_point != "AddTitle") {
			continue
		}
		// Check this title's Length value against the Title Type value
		// Build the name of the Length field being processed
		length_field = 'title_storylen' + i;
		// Retrieve the handle of the Length field being processed
		length_field_handle = document.getElementsByName(length_field)[0];
		// Retrieve the value of the Length field being processed
		length_field_data = length_field_handle.value;

		// Build the name of the Title Type field being processed
		ttype_field = 'title_ttype' + i;
		// Retrieve the handle of the Title Type field being processed
		ttype_field_handle = document.getElementsByName(ttype_field)[0];
		// Retrieve the value of the Title Type field being processed
		ttype_field_data = ttype_field_handle.value;

		// Only SHORTFICTION titles can have Length values
		if ((ttype_field_data != 'SHORTFICTION') && (length_field_data !='')) {
			alert("Only SHORTFICTION titles can have Length values");
			length_field_handle.focus();
			return false;
		}
	}
	return true;
}

function validateCovers() {
	// Initialize variables
	var addpoint1;
	var addpoint2;
	var artist_data;
	var artist_field;
	var cover_date_data;
	var cover_date_handle;
	var cover_date_name;
	var cover_title_data;
	var cover_title_handle;
	var cover_title_name;
	var defined_artists;
	var i;
	var int_next1;
	var int_next2;
	var j;
	var next1;
	var next2;

	addpoint1 = document.getElementById("AddCover");
	// If there is no cover art add point, then this is an old style data entry form
	// which handles cover art in the deprecated "Artist" field, so validation passes
	if (addpoint1 == null) {
		return true;
	}

	// Retrieve the next available cover ID
	next1 = addpoint1.getAttribute("next");
	// Convert the next available cover ID to integer so that we can use it in a loop
	int_next1 = parseInt(next1);
	// Check each cover record defined on the page
	for (i = 1 ; i < int_next1 ; i++) {
		// Retrieve the number of authors for this cover record
		addpoint2 = document.getElementById("AddArtist" + i);
		// If there is no artist add point for this cover, then it's read-only and
		// validation passes
		if (addpoint2 == null) {
			continue;
		}

		// Check this cover's date
		// Build the name of the cover field currently being processed
		cover_date_name = "cover_date" + i;
		// Retrieve the handle of the current cover date field
		cover_date_handle = document.getElementsByName(cover_date_name)[0];
		// Retrieve the value of the current cover date field
		cover_date_data = cover_date_handle.value;
		// Strip all spaces in case the date consists of nothing but spaces
		cover_date_data = cover_date_data.split(" ").join("");
		// Validate date format
		if ((cover_date_data != "") && (validateDate(cover_date_data,"Date","title")) == false) {
			cover_date_handle.focus();
			return false;
		}

		// Check this cover's title
		// Build the name of the cover title field that is being processed
		cover_title_name = "cover_title" + i;
		// Retrieve the handle of this title field in case we need to focus on it later
		cover_title_handle = document.getElementsByName(cover_title_name)[0];
		// Retrieve the title of this cover record
		cover_title_data = cover_title_handle.value;
		// Strip all spaces in case the title consists of nothing but spaces
		cover_title_data = cover_title_data.split(" ").join("");
		// If there was no title and no date entered, then validation passes. If one
		// or more artists were entered with no other data, the title and the date will
		// be defaulted to the title and date of the publication
		if ((cover_title_data == "") && (cover_date_data == "")) {
			return true;
		}

		// Retrieve the next available artist number for this cover
		next2 = addpoint2.getAttribute("next");
		// Initialize the number of defined artists for this cover
		defined_artists = 0;
		// Convert the next available artist number to integer so that we can use it in a loop
		int_next2 = parseInt(next2);
		// Check each artist name defined for this cover
		for (j = 1 ; j < int_next2 ; j++) {
			artist_field = "cover_artist" + i + "." + j;
			// Retrieve the name of this artist
			artist_data = document.getElementsByName(artist_field)[0].value;
			// Strip all spaces to check for authors that consist of nothing but spaces
			artist_data = artist_data.split(" ").join("");
			if (artist_data != "") {
				defined_artists++;
			}
		}
		if (defined_artists == 0) {
			alert("No artists were entered, but other cover data was specified. At least one artist must be entered. See Help for details.");
			cover_title_handle.focus();
			return false;
		}
	}
	return true;
}

function validatePubForm() {
	// Validate that a non-empty pub title has been entered
	if (validateRequired("pub_title","Publication Title") == false) {
		return false;
	}
	// Validate this pub's authors
	if (validateAuthors("pub_author", "author/editor") == false) {
		return false;
	}
	// Validate the date of the pub
	if (validateRequiredDate("pub_year", "Date", "required", "title") == false) {
		return false;
	}
	// Validate the cover image URL
	if (validatePubURL("pub_image") == false) {
		return false;
	}
	// Validate the Series Number (for NewPubs)
	if (validateSeriesNumber() == false) {
		return false;
	}
	// Validate the Content field (for NewPubs)
	if (validateContentIndicator() == false) {
		return false;
	}
	// Validate the Web Page URLs (for NewPubs)
	if (validateWebPages("title_webpages") == false) {
		return false;
	}
	// Validate covers
	if (validateCovers() == false) {
		return false;
	}
	// Validate the Title sub-section of the Contents section
	if (validateContents("AddTitle", "title_title", "title_date", "AddAuthor", "title_author", "author", "title") == false) {
		return false;
	}
	// Validate the revieweEs in the Review sub-section of the Contents section
	if (validateContents("AddReview", "review_title", "review_date", "AddReviewee", "review_author", "author", "review") == false) {
		return false;
	}
	// Validate the revieweRs in the Review sub-section of the Contents section
	if (validateContents("AddReview", "review_title", "review_date", "AddReviewer", "review_reviewer", "reviewer", "review") == false) {
		return false;
	}
	// Validate the intervieweEs in the Interview sub-section of the Contents section
	if (validateContents("AddInterview", "interview_title", "interview_date", "AddInterviewee", "interviewee_author", "interviewee", "interview") == false) {
		return false;
	}
	// Validate the intervieweRs in the Interview sub-section of the Contents section
	if (validateContents("AddInterview", "interview_title", "interview_date", "AddInterviewer", "interviewer_author", "interviewer", "interview") == false) {
		return false;
	}
	// Check for mismatch between the publication type and titles in the Content section
	if (validateTypeMismatch() == false) {
		return false;
	}

	return true;
}

function validateTypeMismatch()	{
	// If this page is Publication Editor, then the reference title must be entered explicitly in the Content section.
	// If this page is a Clone/Import/Export page, then the reference title check is not performed.
	// For NewPub and AddPub forms, the reference title is implied and should not be entered in the Content section.
	var reference_title = 'implied';
	if (document.title == 'Publication Editor') {
		reference_title = 'explicit';
	}
	else if (document.title.includes('Import') == true) {
		reference_title = 'ignore';
	}
	else if (document.title.includes('Clone') == true) {
		reference_title = 'ignore';
	}
	// Get the handle of the publication type (pub_ctype) field
	var pub_type_handle = document.getElementsByName("pub_ctype")[0];
	// Retrieve the value of the publication type field
	var pub_type_value = pub_type_handle.value;
	// Retrieve the next available title number
	var addpoint = document.getElementById("AddTitle");
	var next1 = addpoint.getAttribute("next");
	// Convert the next available title number to integer so that we can use it in a loop
	var int_next1 = parseInt(next1);
	var current_title_name;
	var current_title_handle;
	var title_title;
	var current_type_name;
	var current_type_handle;
	var title_type;
	var reference_title_type = '';
	var current_count;
	var anthology_count = 0;
	var chapbook_count = 0;
	var collection_count = 0;
	var editor_count = 0;
	var essay_count = 0;
	var interiorart_count = 0;
	var nonfiction_count = 0;
	var novel_count = 0;
	var omnibus_count = 0;
	var poem_count = 0;
	var serial_count = 0;
	var shortfiction_count = 0;
	var i;
	// Add the title type of each Content title record to type-specific counters
	for (i = 1 ; i < int_next1 ; i++) {
		// Build the name of the title field that is being processed
		current_title_name = "title_title" + i;
		// Retrieve the handle of the current title field
		current_title_handle = document.getElementsByName(current_title_name)[0];
		// Retrieve the title value
		title_title = current_title_handle.value;
		// If there is no title, then it's an empty title record and we skip it
		if (title_title == "") {
			continue;
		}
		// Build the name of the title type field that is being processed
		current_type_name = "title_ttype" + i;
		// Retrieve the handle of the current title type field
		current_type_handle = document.getElementsByName(current_type_name)[0];
		// Retrieve the title type value
		title_type = current_type_handle.value;
		if ((pub_type_value == 'FANZINE') || (pub_type_value == 'MAGAZINE')) {
			if (title_type == 'EDITOR') {
				reference_title_type = 'EDITOR';
			}
		}
		else if (title_type == pub_type_value) {
			reference_title_type = title_type;
		}
		if (title_type == 'ANTHOLOGY') {
			anthology_count = anthology_count + 1;
		}
		if (title_type == 'CHAPBOOK') {
			chapbook_count = chapbook_count + 1;
		}
		if (title_type == 'COLLECTION') {
			collection_count = collection_count + 1;
		}
		if (title_type == 'EDITOR') {
			editor_count = editor_count + 1;
		}
		if (title_type == 'ESSAY') {
			essay_count = essay_count + 1;
		}
		if (title_type == 'INTERIORART') {
			interiorart_count = interiorart_count + 1;
		}
		if (title_type == 'NONFICTION') {
			nonfiction_count = nonfiction_count + 1;
		}
		if (title_type == 'NOVEL') {
			novel_count = novel_count + 1;
		}
		if (title_type == 'OMNIBUS') {
			omnibus_count = omnibus_count + 1;
		}
		if (title_type == 'POEM') {
			poem_count = poem_count + 1;
		}
		if (title_type == 'SHORTFICTION') {
			shortfiction_count = shortfiction_count + 1;
		}
		if (title_type == 'SERIAL') {
			serial_count = serial_count + 1;
		}
	}
	if (editor_count > 1) {
		alert("Multiple EDITOR titles are not allowed");
		return false;
	}
	if (chapbook_count > 1) {
		alert("Multiple CHAPBOOK titles are not allowed.");
		return false;
	}

	// Check that the reference title was entered for pub edits and was NOT entered for other types of submissions
	if (reference_title_type != '') {
		if (reference_title == 'implied') {
			var article = determineArticle(reference_title_type);
			var message = 'When creating a new '+pub_type_value+' publication, ';
			message += article+' '+reference_title_type;
			message += ' title should not be entered in the Regular Titles subsection of the Content section. ';
			message += 'It will be added automatically at submission creation time.';
			alert(message);
			return false;
		}
	}
	else {
		if (reference_title == 'explicit') {
			var message = 'When editing publications, the Regular Titles subsection of the Content';
			message += ' section must contain one title whose type matches the publication type.';
			message += ' For Magazine and Fanzine publications the matching title type should be EDITOR.';
			alert(message);
			return false;
		}
	}

	// Check that the entered title types are valid for the specified publication type
	if ((pub_type_value != 'MAGAZINE') && (pub_type_value != 'FANZINE') && (editor_count > 0)) {
		alert("Only MAGAZINE and FANZINE publications can contain EDITOR titles.");
		return false;
	}

	if ((pub_type_value != 'CHAPBOOK') && (chapbook_count > 0)) {
		alert("Only CHAPBOOK publications can contain CHAPBOOK titles.");
		return false;
	}

	if (pub_type_value == "CHAPBOOK") {
		if ((anthology_count + collection_count + nonfiction_count + novel_count + omnibus_count) > 0) {
			alert("ANTHOLOGY, COLLECTION, NONFICTION, NOVEL, and OMNIBUS titles are not allowed within CHAPBOOK publications.");
			return false;
		}
	}

	if ((pub_type_value == 'MAGAZINE') || (pub_type_value == 'FANZINE')) {
		if (novel_count > 0) {
			alert("NOVEL titles are not allowed in MAGAZINE/FANZINE publications. Use (Complete Novel) SERIALs instead. See Help for more details.");
			return false;
		}
	}

	return true;
}

function addNewExternalID(field_name, table_name) {
	var field_name = field_name || 'external_id';
	var table_name = table_name || 'pubBody';
	var identifier_types = ExternalIdentifiers();
	var tbody = document.getElementById(table_name);

	var last_row = GetLastExternalId(field_name);
	var addpoint = document.getElementById(field_name + '.row.' + last_row);
	var next = last_row + 1;

	var tr   = document.createElement("tr");
	tr.setAttribute("id", field_name + '.row.' + next);
	var td1  = document.createElement("td");
	var select = document.createElement("select");
	select.setAttribute("name", field_name+"_type."+next);
	select.setAttribute("tabindex", "1");
	for (var i = 0; i < identifier_types.length; i++) {
		var option = document.createElement("option");
		option.value = identifier_types[i]["id"];
		option.text = identifier_types[i]["name"];
		select.appendChild(option);
	}
	td1.appendChild(select);
	tr.appendChild(td1);

	var td2  = document.createElement("td");
	var input = document.createElement("input");
	var attr = "external_id."+next;
	input.setAttribute("name", attr);
	input.setAttribute("id", attr);
	input.setAttribute("class", "metainput");
	input.setAttribute("tabindex", "1");
	td2.appendChild(input);
	tr.appendChild(td2);
	tbody.insertBefore(tr, addpoint.nextSibling);
}

function GetLastExternalId(field_name) {
	for (i = 1 ; i < 1000 ; i++) {
		row_data = document.getElementById(field_name + '.row.' + i);
		if (row_data == null) {
			return i-1;
		}
	}
	return 999;
}

function addNewBriefCover() {
	var record_type = "cover";
	var tbody = document.getElementById("coverBody");
	var last_row = GetLastRow('cover_id');
	var addpoint = document.getElementById('cover_id' + last_row + '.row');
	var next = last_row + 1;

	// First row - create top-level elements
	var tr1 = document.createElement("tr");
	var td1 = document.createElement("td");
	// Element: input title_idX
	var attr = record_type+"_id"+next;
	var input1 = document.createElement("input");
	input1.setAttribute("name", attr);
	input1.setAttribute("value", "0");
	input1.setAttribute("type", "HIDDEN");
	td1.appendChild(input1);
	// Element: input title_titleX
	attr = record_type+"_title"+next;
	var input2 = document.createElement("input");
	input2.setAttribute("name", attr);
	input2.setAttribute("type", "HIDDEN");
	td1.appendChild(input2);
	// Element: input title_dateX
	attr = record_type+"_date"+next;
	var input3 = document.createElement("input");
	input3.setAttribute("name", attr);
	input3.setAttribute("type", "HIDDEN");
	td1.appendChild(input3);
	tr1.appendChild(td1);
	tbody.insertBefore(tr1, addpoint.nextSibling);

	// Second row for "Artist1" - create top-level elements
	var tr2 = document.createElement("tr");
	tr2.setAttribute("id", "cover_artist"+next+".1.row");
	var td2 = document.createElement("td");
	var bold = document.createElement("b");
	var text1 = document.createTextNode("Artist1:");

	bold.appendChild(text1);
	td2.appendChild(bold);
	tr2.appendChild(td2);

	var td3 = document.createElement("td");
	var input4 = document.createElement("input");
	attr = "cover_artist"+next+".1";
	input4.setAttribute("id", attr);
	input4.setAttribute("name", attr);
	input4.setAttribute("class", "contentinput");
	input4.setAttribute("tabindex", "1");
	td3.appendChild(input4);
	tr2.appendChild(td3);
	tbody.insertBefore(tr2, tr1.nextSibling);

	// Third row - "Add Artist" Button
	var tr3    = document.createElement("tr");
	attr = "AddArtist"+next;
	tr3.setAttribute("id", attr);
	tr3.setAttribute("next", "2");
	var td4   = document.createElement("td");
	tr3.appendChild(td4);

	// <td> button element
	var td5   = document.createElement("td");
	var input5 = document.createElement("input");
	input5.setAttribute("type", "button");
	input5.setAttribute("tabindex", "1");
	input5.setAttribute("value", "Add Artist");

	isIE = navigator.userAgent.indexOf("MSIE") > -1;
	if (isIE) {
		var fnTitleHelper = function(oEvent) {
			var oElement = oEvent.srcElement;
			var buttonNumber = oElement.getAttribute("id");
			addArtist(buttonNumber);
		}
		input5.attachEvent("onclick", fnTitleHelper);
	}
	attr = "addArtist("+next+")";
	input5.setAttribute("onclick", attr);
	td5.appendChild(input5);
	tr3.appendChild(td5);
	tbody.insertBefore(tr3, tr2.nextSibling);

	// Spacer
	var tr4  = document.createElement("tr");
	tr4.setAttribute("id", "cover_id"+next+".row");
	tr4.className = "titleeditspacer";
	var td6 = document.createElement("td");
	td6.colSpan = 2;
	tr4.appendChild(td6);
	tbody.insertBefore(tr4, tr3.nextSibling);
}

function addNewFullCover() {
	var body_name = "coverBody";
	var addpoint_name = "AddCover";
	var record_type = "cover";
	var tbody = document.getElementById(body_name);
	var addpoint = document.getElementById(addpoint_name);
	// Update the 'next' attribute for later additions
	next = addpoint.getAttribute("next");
	var int_next = parseInt(next);
	int_next += 1;
	var str_next = int_next.toString();
	addpoint.setAttribute("next", str_next);
	// First row - create top-level elements
	var tr1    = document.createElement("tr");
	var td1   = document.createElement("td");
	// Element: input title_idX
	var attr = record_type+"_id"+next;
	var input1 = document.createElement("input");
	input1.setAttribute("name", attr);
	input1.setAttribute("value", "0");
	input1.setAttribute("type", "HIDDEN");
	td1.appendChild(input1);
	// Element: input title_titleX
	var td2   = document.createElement("td");
	attr = record_type+"_title"+next;
	var input2 = document.createElement("input");
	input2.setAttribute("id", attr);
	input2.setAttribute("name", attr);
	input2.setAttribute("class", "contentinput");
	input2.setAttribute("tabindex", "1");
	td2.appendChild(input2);
	// Element: input title_dateX
	var td3 = document.createElement("td");
	attr = record_type+"_date"+next;
	var input3 = document.createElement("input");
	input3.setAttribute("name", attr);
	input3.setAttribute("class", "contentyearinput");
	input3.setAttribute("tabindex", "1");
	td3.appendChild(input3);
	tr1.appendChild(td1);
	tr1.appendChild(td2);
	tr1.appendChild(td3);
	tbody.insertBefore(tr1, addpoint);

	// Second row for "Artist1" - create top-level elements
	var tr2    = document.createElement("tr");
	tr2.setAttribute("id", "cover_artist"+next+".1.row");
	var td2   = document.createElement("td");
	var bold   = document.createElement("b");
	var text1 = document.createTextNode("Artist1:");

	bold.appendChild(text1);
	td2.appendChild(bold);
	tr2.appendChild(td2);

	var td3 = document.createElement("td");
	var input4 = document.createElement("input");
	attr = "cover_artist"+next+".1";
	input4.setAttribute("id", attr);
	input4.setAttribute("name", attr);
	input4.setAttribute("class", "contentinput");
	input4.setAttribute("tabindex", "1");
	td3.appendChild(input4);
	tr2.appendChild(td3);
	tbody.insertBefore(tr2, addpoint);

	// Third row - "Add Artist" Button
	var tr3    = document.createElement("tr");
	attr = "AddArtist"+next;
	tr3.setAttribute("id", attr);
	tr3.setAttribute("next", "2");
	var td4   = document.createElement("td");
	tr3.appendChild(td4);

	// <td> button element
	var td5   = document.createElement("td");
	var input5 = document.createElement("input");
	input5.setAttribute("type", "button");
	input5.setAttribute("tabindex", "1");
	input5.setAttribute("value", "Add Artist");

	isIE = navigator.userAgent.indexOf("MSIE") > -1;
	if (isIE) {
		var fnTitleHelper = function(oEvent) {
			var oElement = oEvent.srcElement;
			var buttonNumber = oElement.getAttribute("id");
			addArtist(buttonNumber);
		}
		input5.attachEvent("onclick", fnTitleHelper);
	}
	attr = "addArtist("+next+")";
	input5.setAttribute("onclick", attr);
	td5.appendChild(input5);
	tr3.appendChild(td5);
	tbody.insertBefore(tr3, addpoint);

	// Spacer
	var tr4  = document.createElement("tr");
	tr4.className = "titleeditspacer";
	var td6 = document.createElement("td");
	td6.colSpan = 3;
	tr4.appendChild(td6);
	tbody.insertBefore(tr4, addpoint);
}

function addNewTitle() {
	addRecord("titleBody", "AddTitle", "title")
}

function addNewReview() {
	addRecord("reviewBody", "AddReview", "review")
}

function addNewInterview() {
	addRecord("interviewBody", "AddInterview", "interview")
}

function addRecord(body_name, addpoint_name, record_type) {
	var tbody = document.getElementById(body_name);
	var addpoint = document.getElementById(addpoint_name);

	// Update the 'next' attribute for later additions
	var next = addpoint.getAttribute("next");
	var int_next = parseInt(next);
	int_next += 1;
	var str_next = int_next.toString();
	addpoint.setAttribute("next", str_next);

	// Create top-level elements
	var tr    = document.createElement("tr");
	var input = document.createElement("input");
	var td1   = document.createElement("td");
	var input1 = document.createElement("input");
	var td2   = document.createElement("td");
	var input2 = document.createElement("input");
	var td3   = document.createElement("td");
	var input3 = document.createElement("input");
	var td4   = document.createElement("td");
	var td5   = document.createElement("td");

	// Element: input title_idX
	var attr = record_type+"_id"+next;
	input.setAttribute("name", attr);
	input.setAttribute("value", "-1");
	input.setAttribute("type", "HIDDEN");
	tr.appendChild(input);

	//# Element: input title_pageX
	attr = record_type+"_page"+next;
	input1.setAttribute("name", attr);
	input1.setAttribute("value", "");
	input1.setAttribute("class", "contentpageinput");
	input1.setAttribute("tabindex", "1");
	td1.appendChild(input1);
	tr.appendChild(td1);

	// Element: input title_titleX
	attr = record_type+"_title"+next;
	input2.setAttribute("name", attr);
	input2.setAttribute("value", "");
	input2.setAttribute("class", "contentinput");
	input2.setAttribute("tabindex", "1");
	td2.appendChild(input2);
	tr.appendChild(td2);

	// Element: input title_dateX
	attr = record_type+"_date"+next;
	input3.setAttribute("name", attr);
	input3.setAttribute("value", "");
	input3.setAttribute("class", "contentyearinput");
	input3.setAttribute("tabindex", "1");
	td3.appendChild(input3);
	tr.appendChild(td3);

	if (record_type == "title") {
		// Element: input title_ttypeX
		var select = document.createElement("select");
		var option1 = document.createElement("option");
		var option2 = document.createElement("option");
		var option3 = document.createElement("option");
		var option4 = document.createElement("option");
		var option5 = document.createElement("option");
		var option6 = document.createElement("option");
		var option7 = document.createElement("option");
		var option8 = document.createElement("option");
		var option9 = document.createElement("option");
		var option10 = document.createElement("option");
		var option11 = document.createElement("option");
		var option12 = document.createElement("option");
		var option13 = document.createElement("option");

		// <select name="title_ttypeX">
		attr = "title_ttype"+next;
		select.setAttribute("name", attr);
		select.setAttribute("class", "contenttypeinput");
		select.setAttribute("tabindex", "1");
		option1.setAttribute("selected", "selected");

		// Retrieve the handle of the publication type field
		// Use [0] because JS returns an array in case there are many fields with this name
		var pub_ctype_handle = document.getElementsByName("pub_ctype")[0];

		// Retrieve the value of the pub type field
		var pub_ctype_value = pub_ctype_handle.value;

		if (pub_ctype_value == 'NONFICTION') {
			var text1 = document.createTextNode("ESSAY");
		}
		else if (pub_ctype_value == 'OMNIBUS') {
			var text1 = document.createTextNode("NOVEL");
		}
		else {
			var text1 = document.createTextNode("SHORTFICTION");
		}
		option1.appendChild(text1);
		select.appendChild(option1);

		var text2 = document.createTextNode("ANTHOLOGY");
		option2.appendChild(text2);
		select.appendChild(option2);

		var text3 = document.createTextNode("CHAPBOOK");
		option3.appendChild(text3);
		select.appendChild(option3);

		var text4 = document.createTextNode("COLLECTION");
		option4.appendChild(text4);
		select.appendChild(option4);

		var text5 = document.createTextNode("EDITOR");
		option5.appendChild(text5);
		select.appendChild(option5);

		if (pub_ctype_value != 'NONFICTION') {
			var text6 = document.createTextNode("ESSAY");
			option6.appendChild(text6);
			select.appendChild(option6);
		}

		var text7 = document.createTextNode("INTERIORART");
		option7.appendChild(text7);
		select.appendChild(option7);

		var text8 = document.createTextNode("NONFICTION");
		option8.appendChild(text8);
		select.appendChild(option8);

		if (pub_ctype_value != 'OMNIBUS') {
			var text9 = document.createTextNode("NOVEL");
			option9.appendChild(text9);
			select.appendChild(option9);
		}

		var text10 = document.createTextNode("OMNIBUS");
		option10.appendChild(text10);
		select.appendChild(option10);

		var text11 = document.createTextNode("POEM");
		option11.appendChild(text11);
		select.appendChild(option11);

		var text12 = document.createTextNode("SERIAL");
		option12.appendChild(text12);
		select.appendChild(option12);

		if ((pub_ctype_value == 'OMNIBUS') || (pub_ctype_value == 'NONFICTION')) {
			var text13 = document.createTextNode("SHORTFICTION");
			option13.appendChild(text13);
			select.appendChild(option13);
		}

		td4.appendChild(select);
		tr.appendChild(td4);

		// Element: input title_storylen
		var select2 = document.createElement("select");

		// <td><select name="title_storylenX">
		attr = "title_storylen"+next;
		select2.setAttribute("name", attr);
		select2.setAttribute("tabindex", "1");
		select2.setAttribute("class", "contentleninput");
		td5.appendChild(select2);

		// <option></option>
		var option14 = document.createElement("option");
		var text14 = document.createTextNode("");
		option14.appendChild(text14);

		// <option>novella</option>
		var option15 = document.createElement("option");
		var text15 = document.createTextNode("novella");
		option15.appendChild(text15);

		// <option>short story</option>
		var option16 = document.createElement("option");
		var text16 = document.createTextNode("short story");
		option16.appendChild(text16);

		// <option>novelette</option>
		var option17 = document.createElement("option");
		var text17 = document.createTextNode("novelette");
		option17.appendChild(text17);

		select2.appendChild(option14);
		select2.appendChild(option15);
		select2.appendChild(option16);
		select2.appendChild(option17);
		tr.appendChild(td5);
	}
	// Author section
	var tr2    = document.createElement("tr");
	var tda1   = document.createElement("td");
	var bold   = document.createElement("b");
	if (record_type == "title") {
		var text18 = document.createTextNode("Author1:");
		attr = "title_author"+next+".1";
	}
	else if (record_type == "review") {
		var text18 = document.createTextNode("Author1:");
		attr = "review_author"+next+".1";
	}
	else if (record_type == "interview") {
		var text18 = document.createTextNode("Interviewee1:");
		attr = "interviewee_author"+next+".1";
	}
	bold.appendChild(text18);
	tda1.appendChild(bold);
	tr2.appendChild(tda1);

	var tda2   = document.createElement("td");
	var input4 = document.createElement("input");
	input4.setAttribute("name", attr);
	input4.setAttribute("class", "contentinput");
	input4.setAttribute("tabindex", "1");
	tda2.appendChild(input4);
	tr2.appendChild(tda2);

	// Add Author Button

	// <tr> table element
	var tr3    = document.createElement("tr");
	if (record_type == "title") {
		attr = "AddAuthor"+next;
	}
	else if (record_type == "review") {
		attr = "AddReviewee"+next;
	}
	else if (record_type == "interview") {
		attr = "AddInterviewee"+next;
	}
	tr3.setAttribute("id", attr);
	tr3.setAttribute("next", "2");

	// <td> Spacer element
	var tda3   = document.createElement("td");
	var text19 = document.createTextNode(" ");
	tda3.appendChild(text19);
	tr3.appendChild(tda3);

	// <td> button element
	var tda4   = document.createElement("td");
	var input5 = document.createElement("input");
	input5.setAttribute("type", "button");
	input5.setAttribute("tabindex", "1");
	if (record_type == "title") {
		input5.setAttribute("value", "Add Author");
	}
	else if (record_type == "review") {
		input5.setAttribute("value", "Add Author");
	}
	else if (record_type == "interview") {
		input5.setAttribute("value", "Add Interviewee");
	}

	isIE = navigator.userAgent.indexOf("MSIE") > -1;
	if (record_type == "title") {
		if (isIE) {
			var fnTitleHelper = function(oEvent) {
				var oElement = oEvent.srcElement;
				var buttonNumber = oElement.getAttribute("id");
				addContentTitleAuthor(buttonNumber);
			}
			input5.attachEvent("onclick", fnTitleHelper);
		}
		else {
			attr = "addContentTitleAuthor("+next+")";
		}
		input5.setAttribute("onclick", attr);
	}
	else if (record_type == "review") {
		if (isIE) {
			var fnReviewHelper = function(oEvent) {
				var oElement = oEvent.srcElement;
				var buttonNumber = oElement.getAttribute("id");
				addReviewee(buttonNumber);
			}
			input5.attachEvent("onclick", fnReviewHelper);
		}
		else {
			attr = "addReviewee("+next+")";
		}
		input5.setAttribute("onclick", attr);
	}
	else if (record_type == "interview") {
		if (isIE) {
			var fnInterviewHelper = function(oEvent) {
				var oElement = oEvent.srcElement;
				var buttonNumber = oElement.getAttribute("id");
				addInterviewee(buttonNumber);
			}
			input5.attachEvent("onclick", fnInterviewHelper);
		}
		else {
			attr = "addInterviewee("+next+")";
		}
		input5.setAttribute("onclick", attr);
	}
	if (record_type == "review") {
		// Reviewer section
		var tr4    = document.createElement("tr");
		var tda5   = document.createElement("td");
		var bold2  = document.createElement("b");
		var text20 = document.createTextNode("Reviewer1:");
		attr = "review_reviewer"+next+".1";
		bold2.appendChild(text20);
		tda5.appendChild(bold2);
		tr4.appendChild(tda5);

		var tda6   = document.createElement("td");
		var input4 = document.createElement("input");
		input4.setAttribute("name", attr);
		input4.setAttribute("class", "contentinput");
		input4.setAttribute("tabindex", "1");
		tda6.appendChild(input4);
		tr4.appendChild(tda6);

		// Add Reviewer Button
		var tr5    = document.createElement("tr");
		attr = "AddReviewer"+next;
		tr5.setAttribute("id", attr);
		tr5.setAttribute("next", "2");

		var tda7   = document.createElement("td");
		var text21 = document.createTextNode(" ");
		tda7.appendChild(text21);
		tr5.appendChild(tda7);

		var tda8   = document.createElement("td");
		var input6 = document.createElement("input");
		input6.setAttribute("type", "button");
		input6.setAttribute("value", "Add Reviewer");
		input6.setAttribute("tabindex", "1");

		if (isIE) {
			var fnReviewerHelper = function(oEvent) {
				var oElement = oEvent.srcElement;
				var buttonNumber = oElement.getAttribute("id");
				addReviewer(buttonNumber);
			}
			input6.attachEvent("onclick", fnReviewerHelper);
		}
		else {
			attr = "addReviewer("+next+")";
			input6.setAttribute("onclick", attr);
		}

		tda8.appendChild(input6);
		tr5.appendChild(tda8);
	}

	else if (record_type == "interview") {
		// Interviewer section
		var tr4    = document.createElement("tr");
		var tda5   = document.createElement("td");
		var bold2  = document.createElement("b");
		var text22 = document.createTextNode("Interviewer1:");
		attr = "interviewer_author"+next+".1";
		bold2.appendChild(text22);
		tda5.appendChild(bold2);
		tr4.appendChild(tda5);

		var tda6   = document.createElement("td");
		var input4 = document.createElement("input");
		input4.setAttribute("name", attr);
		input4.setAttribute("class", "contentinput");
		input4.setAttribute("tabindex", "1");
		tda6.appendChild(input4);
		tr4.appendChild(tda6);

		// Add Interviewer Button
		var tr5    = document.createElement("tr");
		attr = "AddInterviewer"+next;
		tr5.setAttribute("id", attr);
		tr5.setAttribute("next", "2");

		var tda7   = document.createElement("td");
		var text23 = document.createTextNode(" ");
		tda7.appendChild(text23);
		tr5.appendChild(tda7);

		var tda8   = document.createElement("td");
		var input6 = document.createElement("input");
		input6.setAttribute("type", "button");
		input6.setAttribute("tabindex", "1");
		input6.setAttribute("value", "Add Interviewer");

		if (isIE) {
			var fnInterviewerHelper = function(oEvent) {
				var oElement = oEvent.srcElement;
				var buttonNumber = oElement.getAttribute("id");
				addInterviewer(buttonNumber);
			}
			input6.attachEvent("onclick", fnInterviewerHelper);
		}
		else {
			attr = "addInterviewer("+next+")";
			input6.setAttribute("onclick", attr);
		}

		tda8.appendChild(input6);
		tr5.appendChild(tda8);
	}
	tda4.appendChild(input5);
	tr3.appendChild(tda4);

	tbody.insertBefore(tr, addpoint);
	tbody.insertBefore(tr2, addpoint);
	tbody.insertBefore(tr3, addpoint);
	if (record_type != "title") {
		tbody.insertBefore(tr4, addpoint);
		tbody.insertBefore(tr5, addpoint);
	}

	var tr6  = document.createElement("tr");
	tr6.className = "titleeditspacer";
	var tdx = document.createElement("td");
	if (record_type == "title") {
		tdx.colSpan = 5;
	}
	else {
		tdx.colSpan = 3;
	}
	tr6.appendChild(tdx);
	tbody.insertBefore(tr6, addpoint);
}
