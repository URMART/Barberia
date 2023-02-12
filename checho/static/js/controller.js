

function validar(url) {

    return confirm("Seguro que quiere eliminar ?") ? location.href = url : console.log("no se elimino");

}

function buscarCliente(url) {
    dato = $('#dato').val();
    resultado = $('#respuesta');
    token = $('input[name="csrfmiddlewaretoken"]').val();
    console.log("Token:" + token);
    $.ajax({
        url: url,
        type: 'post',
        data: { "dato": dato, "csrfmiddlewaretoken": token },
        //dataType: 'json',
        success: function (respuesta) {
            resultado.html(respuesta);
        },
        error: function (error) {
            console.log("Error" + error);
        }
    });
}

function checksAgenda(idlink, idcheckbox){
    idlink.blur();

    if(idcheckbox.checked){
        idcheckbox.checked = false;
    }
    else{
        idcheckbox.checked = true ;
    }


}

function checksAgenda2(idlink, idcheckbox){
    idlink.blur();

    if(idcheckbox.checked){
        idcheckbox.checked = false;
    }
    else{
        idcheckbox.checked = true ;
    }


}





