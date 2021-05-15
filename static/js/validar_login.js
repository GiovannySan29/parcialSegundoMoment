function Login(){
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;
    const vpassword = new RegExp(/^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,14}$/);

    if (username.length == 0  || username== "") {
        alert('Digite el campo Usuario');
        return false;
        }
    if (!vpassword.test(password)){
        alert('El campo password no tiene los caracteres requeridos'); 
        alert('Debe contener una mayuscula y un numero y minimo 6 letras '); 
        return false;
    }
}