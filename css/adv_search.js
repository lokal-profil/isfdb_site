/*     Version: $Revision: 19 $
      Date: $Date: 2017-10-31 19:26:25 -0400 (Tue, 31 Oct 2017) $ */

function PubSelectors(selector_number, new_value) {
	// Create a handle for the search value field
	var element = document.getElementById('pubterm_'+selector_number);
	// Retrieve the current value of the field
	// var element_value = element.value;
	// Get the parent element's object
	var parent = document.getElementById('pub_selectors_'+selector_number);
	if (new_value == "pub_ptype") {
		parent.removeChild(element);
		var element = document.createElement('select');
		element.name = 'TERM_'+selector_number;
		element.id = 'pubterm_'+selector_number;
		var pub_formats = PubFormats();
		for (var i = 0; i < pub_formats.length; i++) {
			var option = document.createElement("option");
			option.value = pub_formats[i];
			option.text = pub_formats[i];
			element.appendChild(option);
		}
		parent.appendChild(element);
	}
	else {
		// If we are switching from a text input field to another text input field,
		// don't change the field value
		if (element.type == 'text') {
			return true;
		}
		parent.removeChild(element);
		var element = document.createElement('input');
		element.type = 'text';
		element.name = 'TERM_'+selector_number;
		element.size = 50;
		element.id = 'pubterm_'+selector_number;
		parent.appendChild(element);
	}
	return true;
}

function ChangeToSelect(value_type) {
	return true;
}