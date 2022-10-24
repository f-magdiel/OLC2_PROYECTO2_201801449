import React,{useState,useEffect} from "react";

function ReporteError(){
    const [informacion,setInformacion] = useState([]);

    useEffect(()=>{
        
        console.log("se efectua")
        console.log(informacion)
    })

    const getErrores = async(event)=>{
        
        console.log("obtener simbolos")
        event.preventDefault()
        const res = await fetch('http://localhost:7000/getTablaErrores',{
            method:'get',
            headers:{
                'Content-Type':'application/json'
            }
        })
        
        const data = await res.json();
        setInformacion(data.simb)
        //console.log(data.sim)
        
       
      
       
       
    }

    return(
        <div>
                   <table class="table table-dark table-sm" >
  <thead>
    <tr>
      <th scope="col">Fila</th>
      <th scope="col">Columna</th>
      <th scope="col">Ámbito</th>
      <th scope="col">Tipo</th>
      <th scope="col">Descripción</th>
      <th scope="col">Fecha</th>
    </tr>
  </thead>
  <tbody>
  {informacion.map(user=>(
                      <tr>
                      <td>{user[0]}</td>
                      <td>{user[1]}</td>
                      <td>{user[2]}</td>
                      <td>{user[3]}</td>
                      <td>{user[4]}</td>
                      <td>{user[5]}</td>
                      
                  </tr>
                  ))

                  }
    
    
  </tbody>
</table>
<button type="submit" class="btn btn-primary" onClick={getErrores} >Reporte Errores</button>
        </div>
    )
}

export default ReporteError;