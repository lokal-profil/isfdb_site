/*     Version: $Revision: 19 $
      (C) COPYRIGHT 2018   Ahasuerus
         ALL RIGHTS RESERVED
      Date: $Date: 2017-10-31 19:26:25 -0400 (Tue, 31 Oct 2017) $ */

document.addEventListener('DOMContentLoaded', function() {
	// Set focus on the first active field in the form
	var title = document.title;
	var focus_field = '';
	// For Add Pub and Clone Pub, focus on the Pub Year field since the first two fields are read-only
	if (title == 'Add Publication') {
		focus_field = 'pub_year';
	}
	else if (title == 'Clone Publication') {
		focus_field = 'pub_year';
	}
	else if (title.startsWith('Import Content') == true) {
		focus_field = 'ExportFrom';
	}
	else if (title.startsWith('Export Content') == true) {
		focus_field = 'ExportTo';
	}
	else if (title.startsWith('New Award Category for') == true) {
		focus_field = 'award_cat_name';
	}
	else if ((title.startsWith('New ') == true) && (title != 'New Publication Submission')) {
		focus_field = 'pub_title';
	}
	else if (title.startsWith('Make/Remove a Pseudonym') == true) {
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
	// If this is a bibliographic (i.e. non-editing) page, set focus to the search box
	else {
		focus_field = 'searchform_arg';
	}
	document.getElementById(focus_field).focus();
});
