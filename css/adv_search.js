/*     Version: $Revision: 19 $
      Date: $Date: 2017-10-31 19:26:25 -0400 (Tue, 31 Oct 2017) $ */

function YesNo() {
	var formats = ["Yes", "No"];
	return formats;
}

function PubFormats()	{
	return GetValidValues('Formats');
}

function PubTypes()	{
	return GetValidValues('PubTypes');
}

function TitleTypes()	{
	return GetValidValues('TitleTypes');
}

function StoryLengths()	{
	return GetValidValues('StoryLengths');
}

function AllLanguages()	{
	return GetValidValues('AllLanguages');
}

function GetValidValues(select_name)	{
	var field = document.getElementById(select_name);
	var field_values = [];
	var i;
	var len = field.options.length;
	for (i = 0; i < len; i++) {
		field_values.push(field.options[i].value);
	}
	return field_values;
}

function CreateDropDown(parent, old_element, element_id, selector_number, values) {
	parent.removeChild(old_element);
	var new_element = document.createElement('select');
	new_element.name = 'TERM_'+selector_number;
	new_element.id = element_id+'_'+selector_number;
	for (var i = 0; i < values.length; i++) {
		var option = document.createElement("option");
		option.value = values[i];
		option.text = values[i];
		new_element.appendChild(option);
	}
	parent.appendChild(new_element);
}

function Selectors(selector_number, new_value, selectors_id, value_id) {
	// Create a handle for the search value field
	var element = document.getElementById(value_id+'_'+selector_number);
	// Get the parent element's object
	var parent = document.getElementById(selectors_id+'_'+selector_number);
	var values = "";
	switch(new_value) {
	case "pub_ptype":
		values = PubFormats();
		break;
	case "pub_ctype":
		values = PubTypes();
		break;
	case "title_ttype":
		values = TitleTypes();
		break;
	case "title_storylen":
		values = StoryLengths();
		break;
	case "title_jvn":
		values = YesNo();
		break;
	case "title_nvz":
		values = YesNo();
		break;
	case "title_non_genre":
		values = YesNo();
		break;
	case "title_graphic":
		values = YesNo();
		break;
	case "title_language":
		values = AllLanguages();
		break;
	case "author_language":
		values = AllLanguages();
		break;
	default:
		values = "";
		break;
	}
	if (values != "") {
		CreateDropDown(parent, element, value_id, selector_number, values);
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
		element.id = value_id+'_'+selector_number;
		parent.appendChild(element);
	}
	return true;
}
