

function showData(response){
	//$('#result').html(data);
	$('#result').html(response);
}

function handleClick(e){
		$.ajax('/',{
			type:'GET',
			data:{
				fmt:'json'
				},
				success: showData
			});
	}

$(document).ready(function(){
	//$('#getitButton').on('click', handleClick);
	handleClick();
	});