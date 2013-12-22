$(document).ready(function(){
	target_ele = null
	$("#main_content").click(function(event){
		user_email = $(event.target);
		if(user_email.is("button")){
			target_ele = user_email
			$("#new_user").val(event.target.id);
			$("#adding_new_user").show()
		}
	});
	$("#subscribe").click(function(){
		user = $("#selected_user").val();
		plugins = $("#selected_plugin").val();
		$.post("/plugin", {"user":user, "plugin":plugins}, function(data){
			bootbox.alert("Subscribed");
			console.log(data);
		});
	});
	$("#create_new_user").click(function(){
		user_email = $("#new_user").val();
		target_ele.hide()
		ph_num = $("#ph_num").val();
		$.post("/plugin", {"user":user_email, "ph_num":ph_num}, function(data){
			$("#adding_new_user").hide()
			ph_num = $("#ph_num").val("");
			bootbox.alert("User details updated");
			console.log(data);
		});
	});
	$.get("/plugin?user=all&type=json", function(data){
		$("#users").html(data);
		str = $("#select_user").html();
		str += construct_input(data, "radio", "user")
		$("#select_user").html(str);
		register_change_func()
	});
	$.get("/plugin?plugin=plugin&type=json", function(data){
		$("#plugins").html(data);
		str = $("#select_plugin").html();
		str += construct_input(data, "checkbox", "plugins")
		$("#select_plugin").html(str);
		register_checkbox_click()
	});
	$.get("/plugin?plugin=app&type=json", function(data){
		$("#plugins").html(data);
		str = $("#select_app").html();
		str += construct_input(data, "checkbox", "plugins")
		$("#select_app").html(str);
		register_checkbox_click()
	});
	function register_change_func(){
		$('input:radio[name=user]').change(function(){
			$("input[name=plugins]").each(function(i, ele){
				ele.checked = false
			});
			user = $(this).val();
			$("#selected_user").val(user);
			$.get("/plugin?type=json&user=" + user, function(data){
				data = $.parseJSON(data)
				for(p in data){
					p = data[p]
					p = $.trim(p)
					if(!p) continue;
					$("input[name=plugins]").each(function(i, ele){
						if((ele.value == p) && (!ele.checked)){
							ele.click()
						}
					});
				}
			});
		});
	}
	function register_checkbox_click(){
		$('input:checkbox[name=plugins]').change(function() {
			str = ""
			$("input[name=plugins]").each(function(i, ele){
				if(ele.checked){
					str += str ? "," + ele.value : ele.value;
				}
				$("#selected_plugin").val(str);
			});
		});
	}
	function construct_input(data, type, what){
		elements = $.parseJSON(data); //.split(",")
		str = "<form id='"+ what + "_selection'>"
		for(element in elements){
			element = elements[element]
			element = $.trim(element);
			if(element == "") continue;
			str += "<input type='" + type + "' name='"+ what  +"' value='" + element + "'/> " + element + "</br>"
		}
		str += "</form>"
		return str
	}
});
