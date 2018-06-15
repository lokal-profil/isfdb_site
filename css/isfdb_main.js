/*     Version: $Revision: 19 $
      (C) COPYRIGHT 2018   Ahasuerus
         ALL RIGHTS RESERVED
      Date: $Date: 2017-10-31 19:26:25 -0400 (Tue, 31 Oct 2017) $ */

document.addEventListener('DOMContentLoaded', function() {
	var title = document.title;
	setPageFocus(title);
	createOnsubmit(title);
	createOnclick(title);
	createOnchange();
});

function createOnclick(title)	{
	if (document.getElementById('divothersites')) {
		document.getElementById('divothersites').onclick = function(event){
			void(0);
		};
	}

	if (document.getElementById('external_id.addsign')) {
		document.getElementById('external_id.addsign').onclick = function(event){
			addNewExternalID('external_id');
		};
	}

	/*
	var multiples = [{'id': 'trans_names', 'label': 'Transliterated Name'}, {'id': 'trans_legal_names', 'label': 'Trans. Legal Name'}];
	var i;
	var field_id;
	var addsign;
	var label;
	for (i = 0; i < multiples.length; i++) {
		field_id = multiples[i].id;
		addsign = field_id + '.addsign';
		label = multiples[i].label;
		alert(field_id+label);
		if (document.getElementById(addsign)) {
			document.getElementById(addsign).onclick = function(event){
				AddMultipleField(label, field_id);
			};
		}
	}
	*/

	if (document.getElementById('trans_names.addsign')) {
		document.getElementById('trans_names.addsign').onclick = function(event){
			AddMultipleField('Transliterated Name', 'trans_names');
		};
	}

	if (document.getElementById('trans_legal_names.addsign')) {
		document.getElementById('trans_legal_names.addsign').onclick = function(event){
			AddMultipleField('Trans. Legal Name', 'trans_legal_names');
		};
	}

	if (document.getElementById('author_webpages.addsign')) {
		document.getElementById('author_webpages.addsign').onclick = function(event){
			AddMultipleField('Web Page', 'author_webpages');
		};
	}

	if (document.getElementById('publisher_webpages.addsign')) {
		document.getElementById('publisher_webpages.addsign').onclick = function(event){
			AddMultipleField('Web Page', 'publisher_webpages');
		};
	}

	if (document.getElementById('pub_series_webpages.addsign')) {
		document.getElementById('pub_series_webpages.addsign').onclick = function(event){
			AddMultipleField('Web Page', 'pub_series_webpages');
		};
	}

	if (document.getElementById('title_webpages.addsign')) {
		document.getElementById('title_webpages.addsign').onclick = function(event){
			AddMultipleField('Web Page', 'title_webpages');
		};
	}

	if (document.getElementById('award_type_webpages.addsign')) {
		document.getElementById('award_type_webpages.addsign').onclick = function(event){
			AddMultipleField('Web Page', 'award_type_webpages');
		};
	}

	if (document.getElementById('award_cat_webpages.addsign')) {
		document.getElementById('award_cat_webpages.addsign').onclick = function(event){
			AddMultipleField('Web Page', 'award_cat_webpages');
		};
	}

	if (document.getElementById('series_webpages.addsign')) {
		document.getElementById('series_webpages.addsign').onclick = function(event){
			AddMultipleField('Web Page', 'series_webpages');
		};
	}

	if (document.getElementById('author_emails.addsign')) {
		document.getElementById('author_emails.addsign').onclick = function(event){
			AddMultipleField('Email Address', 'author_emails');
		};
	}

	if (document.getElementById('title_author.addsign')) {
		document.getElementById('title_author.addsign').onclick = function(event){
			AddMultipleField('Author', 'title_author');
		};
	}

	if (document.getElementById('trans_titles.addsign')) {
		document.getElementById('trans_titles.addsign').onclick = function(event){
			AddMultipleField('Transliterated Title', 'trans_titles');
		};
	}

	if (document.getElementById('pub_author.addsign')) {
		document.getElementById('pub_author.addsign').onclick = function(event){
			AddMultipleField('Author', 'pub_author');
		};
	}

	if (document.getElementById('trans_publisher_names.addsign')) {
		document.getElementById('trans_publisher_names.addsign').onclick = function(event){
			AddMultipleField('Transliterated Name', 'trans_publisher_names');
		};
	}

	if (document.getElementById('trans_pub_series_names.addsign')) {
		document.getElementById('trans_pub_series_names.addsign').onclick = function(event){
			AddMultipleField('Transliterated Name', 'trans_pub_series_names');
		};
	}

	if (document.getElementById('interviewee_author1..addsign')) {
		document.getElementById('interviewee_author1..addsign').onclick = function(event){
			AddMultipleField('Interviewee', 'interviewee_author1.');
		};
	}

	if (document.getElementById('interviewer_author1..addsign')) {
		document.getElementById('interviewer_author1..addsign').onclick = function(event){
			AddMultipleField('Interviewer', 'interviewer_author1.');
		};
	}

	if (document.getElementById('review_author1..addsign')) {
		document.getElementById('review_author1..addsign').onclick = function(event){
			AddMultipleField('Author', 'review_author1.');
		};
	}

	if (document.getElementById('review_reviewer1..addsign')) {
		document.getElementById('review_reviewer1..addsign').onclick = function(event){
			AddMultipleField('Reviewer', 'review_reviewer1.');
		};
	}

	if (document.getElementById('tag_name.addsign')) {
		document.getElementById('tag_name.addsign').onclick = function(event){
			AddMultipleField('Tag', 'tag_name');
		};
	}

	if (document.getElementById('ImportTitles.addsign')) {
		document.getElementById('ImportTitles.addsign').onclick = function(event){
			AddMultipleField('Title', 'ImportTitles');
		};
	}

}

function createOnchange()	{
	if (document.getElementById('author_1')) {
		document.getElementById('author_1').onchange = function(event){
			Selectors(1, this.value, 'author_selectors', 'authorterm');
		};
		document.getElementById('author_2').onchange = function(event){
			Selectors(2, this.value, 'author_selectors', 'authorterm');
		};
		document.getElementById('author_3').onchange = function(event){
			Selectors(3, this.value, 'author_selectors', 'authorterm');
		};
		document.getElementById('title_1').onchange = function(event){
			Selectors(1, this.value, 'title_selectors', 'titleterm');
		};
		document.getElementById('title_2').onchange = function(event){
			Selectors(2, this.value, 'title_selectors', 'titleterm');
		};
		document.getElementById('title_3').onchange = function(event){
			Selectors(3, this.value, 'title_selectors', 'titleterm');
		};
		document.getElementById('pub_1').onchange = function(event){
			Selectors(1, this.value, 'pub_selectors', 'pubterm');
		};
		document.getElementById('pub_2').onchange = function(event){
			Selectors(2, this.value, 'pub_selectors', 'pubterm');
		};
		document.getElementById('pub_3').onchange = function(event){
			Selectors(3, this.value, 'pub_selectors', 'pubterm');
		};
	}
}

function createOnsubmit(title)	{
	if (title.startsWith('Award Editor') == true) {
		document.getElementById('data').onsubmit = function(event){
			if (validateAwardForm() == false) {
				event.preventDefault();
			}
		};
	}

	else if (title == 'Add New Award Type') {
		document.getElementById('data').onsubmit = function(event){
			if (validateAwardTypeForm() == false) {
				event.preventDefault();
			}
		};
	}

	else if (title.startsWith('New Award Category') == true) {
		document.getElementById('data').onsubmit = function(event){
			if (validateAwardCatForm() == false) {
				event.preventDefault();
			}
		};
	}

	else if (title == 'Add Publication') {
		document.getElementById('data').onsubmit = function(event){
			if (validatePubForm() == false) {
				event.preventDefault();
			}
		};
	}

	else if (title == 'Add Variant Title') {
		document.getElementById('data').onsubmit = function(event){
			if (validateVariantTitleForm() == false) {
				event.preventDefault();
			}
		};
	}

	else if (title == 'Import/Export Contents') {
		document.getElementById('data').onsubmit = function(event){
			if (validatePubForm() == false) {
				event.preventDefault();
			}
		};
	}

	else if (title == 'Clone Publication') {
		document.getElementById('data').onsubmit = function(event){
			if (validatePubForm() == false) {
				event.preventDefault();
			}
		};
	}

	else if (title == 'Author Editor') {
		document.getElementById('data').onsubmit = function(event){
			if (validateAuthorForm() == false) {
				event.preventDefault();
			}
		};
	}

	else if (title == 'Award Category Editor') {
		document.getElementById('data').onsubmit = function(event){
			if (validateAwardCatForm() == false) {
				event.preventDefault();
			}
		};
	}

	else if (title == 'Award Type Editor') {
		document.getElementById('data').onsubmit = function(event){
			if (validateAwardTypeForm() == false) {
				event.preventDefault();
			}
		};
	}

	else if (title == 'Publication Editor') {
		document.getElementById('data').onsubmit = function(event){
			if (validatePubForm() == false) {
				event.preventDefault();
			}
		};
	}

	else if (title == 'Publisher Editor') {
		document.getElementById('data').onsubmit = function(event){
			if (validatePublisherForm() == false) {
				event.preventDefault();
			}
		};
	}

	else if (title == 'Publication Series Editor') {
		document.getElementById('data').onsubmit = function(event){
			if (validatePubSeriesForm() == false) {
				event.preventDefault();
			}
		};
	}

	else if (title == 'Series Editor') {
		document.getElementById('data').onsubmit = function(event){
			if (validateSeriesForm() == false) {
				event.preventDefault();
			}
		};
	}

	else if (title == 'Title Editor') {
		document.getElementById('data').onsubmit = function(event){
			if (validateTitleForm() == false) {
				event.preventDefault();
			}
		};
	}

	else if (title == 'Make Variant Title') {
		document.getElementById('data').onsubmit = function(event){
			if (validateParentTitle() == false) {
				event.preventDefault();
			}
		};
		document.getElementById('data2').onsubmit = function(event){
			if (validateVariantTitleForm() == false) {
				event.preventDefault();
			}
		};
	}

	else if (title.startsWith('New ') == true) {
		document.getElementById('data').onsubmit = function(event){
			if (validatePubForm() == false) {
				event.preventDefault();
			}
		};
	}
}

function setPageFocus(title)	{
	// Set focus on the first active field in edit forms
	var focus_field = 'searchform_arg';
	// For Add Pub and Clone Pub, focus on the Pub Year field since the first two fields are read-only
	if (title == 'Add Publication') {
		focus_field = 'pub_year';
	}
	else if (title == 'Clone Publication') {
		focus_field = 'pub_year';
	}
	else if (title.startsWith('Import Content')) {
		focus_field = 'ExportFrom';
	}
	else if (title.startsWith('Export Content')) {
		focus_field = 'ExportTo';
	}
	else if (title.startsWith('New Award Category for')) {
		focus_field = 'award_cat_name';
	}
	else if (title.startsWith('New ')) {
		focus_field = 'pub_title';
	}
	else if (title.startsWith('Make/Remove a Pseudonym')) {
		focus_field = 'ParentName';
	}
	else if (title == 'Title Editor') {
		focus_field = 'title_title';
	}
	else if (title == 'Author Editor') {
		focus_field = 'author_canonical';
	}
	else if (title == 'Award Editor') {
		focus_field = 'award_title';
	}
	else if (title == 'Award Editor for a Title') {
		focus_field = 'award_year';
	}
	else if (title == 'Award Type Editor') {
		focus_field = 'award_type_short_name';
	}
	else if (title == 'Add New Award Type') {
		focus_field = 'award_type_short_name';
	}
	else if (title == 'Publication Editor') {
		focus_field = 'pub_title';
	}
	else if (title == 'Publisher Editor') {
		focus_field = 'publisher_name';
	}
	else if (title == 'Publication Series Editor') {
		focus_field = 'pub_series_name';
	}
	else if (title == 'Series Editor') {
		focus_field = 'series_name';
	}
	else if (title == 'Tag Editor') {
		focus_field = 'tag_name1';
	}
	else if (title == 'Link Review') {
		focus_field = 'Parent';
	}
	else if (title == 'Make Variant Title') {
		focus_field = 'Parent';
	}
	else if (title == 'Add Variant Title') {
		focus_field = 'title_title';
	}
	else if (title == 'Link Award') {
		focus_field = 'title_id';
	}
	if (document.getElementById(focus_field)) {
		document.getElementById(focus_field).focus();
	}
	// By default set focus to the search box
	else {
		document.getElementById('searchform_arg').focus();
	}
}