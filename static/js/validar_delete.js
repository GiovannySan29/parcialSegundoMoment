const btnDeleteU = document.querySelectorAll('.btn-delete')
  if(btnDeleteU){
      const btnDelete =Array.from(btnDeleteU);
      btnDelete.forEach((btn) =>{
            btn.addEventListener('click', (e) => {
            if(!confirm('Esta seguro que desea eliminar la propiedad?')){
            e.preventDefault();
            }
          });
      });
}